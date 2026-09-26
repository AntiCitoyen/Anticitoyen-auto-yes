<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — automatically answer "1" to confirmation prompts

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

In a Linux terminal, **auto-yes** watches what programs display and, as soon as a recognized confirmation menu appears (by default "Do you want to proceed?" followed by "1. Yes"), types **1** then Enter for you. The terminal stays fully interactive: typing, Ctrl-C, resizing, colors.

<div align="center">

[🇫🇷 Français](../../README.md) · **🇬🇧 English** · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes in action" width="760"><br><em>The menu appears, auto-yes answers "1", the command continues.</em></p>

> ⚠️ **Use with awareness.** auto-yes confirms **any** request that matches a configured pattern, including one from a destructive command (removing packages, disk tools) or another program asking for your agreement. Keep patterns narrow.

---

## Contents

- [What the project does](#projet)
- [Installation](#installation)
- [Usage](#utilisation)
- [Patterns](#motifs)
- [How it works](#fonctionnement)
- [Troubleshooting](#depannage)
- [Repository layout](#depot)
- [Building the package](#deb)
- [License](#licence)
- [Support the project](#soutien)

---

<a id="projet"></a>

## What the project does

| Command | Role |
|---|---|
| `auto-yes <command> [arguments…]` | launches **one** command and answers its confirmation prompts |
| `auto-yes-shell` | replaces the login shell: **every** command typed in this terminal benefits, with no prefix |
| `auto-yes-configurer-gnome-terminal` | wires `auto-yes-shell` into the default GNOME Terminal profile (`--revert` to undo) |

- **Terminal left intact**: Expect's `spawn` + `interact`; everything you type passes through, only the pattern triggers a send.
- **Resizing relayed**: when the window changes size, the shell and programs know it (history editing, `less`, `vim`, `htop` stay accurate).
- **Patterns editable without reinstalling**: `/etc/auto-yes/patterns.conf`, reread on each new terminal.
- **No double wrapping**: a terminal already under auto-yes that relaunches another one doesn't wrap itself twice (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Installation

### Debian / Ubuntu package

Download the `.deb` from the [latest release](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest), then:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Only dependency: `expect` (≥ 5.45).

### From source

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Usage

### A single command

```bash
auto-yes apt install package
auto-yes ./interactive-script.sh --option
```

### An entire terminal

**Recommended method — `~/.bashrc`** (keeps the starting folder, for example with the file manager's *Open in Terminal*); add at the end of the file:

```bash
# auto-yes in every interactive terminal (no double wrapping, non-interactive shells excluded)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Other method — GNOME Terminal profile** (run as yourself, never with `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # new windows and tabs → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # revert
```

This method touches neither terminals already open, nor `gnome-terminal -- <command>`, nor other emulators.

<a id="motifs"></a>

## Patterns

`/etc/auto-yes/patterns.conf`: one Tcl regular expression per line (`interact -re`); empty lines and those starting with `#` are ignored. Shipped pattern:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

It requires the question **and**, on the following line, the `1.` choice of a numbered menu: the sentence alone (displayed by `cat`, `echo`, a log) triggers nothing.

| Rule | Why |
|---|---|
| Target the whole menu, not an isolated sentence | text that quotes the sentence must not trigger a response |
| `\s` or `\y` for boundaries, never `\b` | in Tcl, `\b` is a backspace, not a word boundary |
| `(?i)` at the start to ignore case | programs vary "Proceed" / "proceed" |
| Test with `AUTO_YES_PATTERNS=file auto-yes …` | the variable replaces `/etc/auto-yes/patterns.conf` for a trial |

<a id="fonctionnement"></a>

## How it works

1. `auto-yes-shell` reads the patterns, sets `AUTO_YES_ACTIVE=1`, then launches `$SHELL -l` in a pseudo-terminal (`spawn -noecho`).
2. `interact -o -nobuffer -re <pattern> { send "1\r" }` copies everything between your terminal and the shell; when the program's output matches a pattern, Expect sends `1` and Enter.
3. A `trap … WINCH` copies the window size (`stty rows/columns`) onto the shell's pseudo-terminal and sends it `SIGWINCH`.

<a id="depannage"></a>

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| While editing a command recalled with ↑/↓, the line shifts or disappears | versions ≤ 1.1: the window size wasn't relayed, bash stayed at 80 columns. Fixed in 1.2; open a new terminal after updating. `stty size` should show the real size. |
| A "1" appears when nobody asked for it | the displayed text matches a pattern (for example a program that displays a quoted confirmation menu, or a pattern's own code). Narrow the pattern, or run that program outside auto-yes (`AUTO_YES_ACTIVE=1 bash`). |
| Nothing gets answered | check the pattern with `AUTO_YES_PATTERNS`; a menu drawn with cursor sequences (without real line breaks) doesn't match `\n`. |
| The terminal opens at root instead of the current folder | "GNOME Terminal profile" method: switch to the `~/.bashrc` method. |
| Disable for one session | `AUTO_YES_ACTIVE=1 bash` opens a shell without auto-yes. |

<a id="depot"></a>

## Repository layout

| Path | Content |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | Expect scripts |
| `bin/auto-yes-configurer-gnome-terminal` | wiring into the GNOME Terminal profile |
| `etc/patterns.conf` | shipped patterns (`/etc/auto-yes/patterns.conf`, configuration file preserved across updates) |
| `packaging/` | `build-deb.sh`, `control`, `changelog`, `copyright`, package scripts |
| `tests/test_auto_yes.py` | pseudo-terminal tests: resizing, recognized menu, isolated sentence ignored |
| `docs/readme/` | this README in 18 other languages |

<a id="deb"></a>

## Building the package

```bash
python3 -m unittest discover -s tests -v   # tests (expect required)
packaging/build-deb.sh                     # → dist/auto-yes_<version>_all.deb
```

The version comes from the first line of `packaging/changelog`.

<a id="licence"></a>

## License

[MIT](../../LICENSE).

<a id="soutien"></a>

## Support the project

If this project is useful to you, a coffee helps maintain it:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Bug reports and ideas: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Security vulnerabilities: [SECURITY.md](../../SECURITY.md).
