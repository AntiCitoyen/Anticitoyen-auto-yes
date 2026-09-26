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
| `auto-yes --pause` / `--reprise` | suspends / restores automatic answering in **all** terminals, even ones already open |
| `auto-yes --etat` / `--journal [N]` | current state; last N logged answers |

- **Terminal left intact**: Expect's `spawn` + `interact`; everything you type passes through, only the pattern triggers a send.
- **Quiet screen**: the answer is only sent if nothing is displayed 300ms after the menu; a question quoted inside scrolling text is ignored.
- **Log**: each recognized pattern is logged (date, answer or reason for abstention, foreground program, text) in `~/.local/state/auto-yes/journal.log`.
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

Dependencies: `expect` (≥ 5.45) and `procps`.

### Fedora, openSUSE… (RPM) and Arch Linux

The same release provides `auto-yes-<version>-1.noarch.rpm` (`sudo dnf install ./auto-yes-*.noarch.rpm`), the `.src.rpm`, the Arch package (`sudo pacman -U auto-yes-*.pkg.tar.zst`) and the AUR files (`aur-<version>.tar.gz`: `PKGBUILD` and `.SRCINFO`).

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

### Environment variables

| Variable | Role | Default |
|---|---|---|
| `AUTO_YES_PATTERNS` | patterns file | `/etc/auto-yes/patterns.conf` |
| `AUTO_YES_CALME` | quiet time required after the menu, in milliseconds (`0`: immediate answer) | `300` |
| `AUTO_YES_JOURNAL` | log file (empty: nothing logged) | `~/.local/state/auto-yes/journal.log` |
| `AUTO_YES_ETAT` | state directory (pause flag) | `~/.local/state/auto-yes` |

Full help: `man auto-yes`.

<a id="fonctionnement"></a>

## How it works

1. `auto-yes-shell` reads the patterns, sets `AUTO_YES_ACTIVE=1`, then launches `$SHELL -l` in a pseudo-terminal (`spawn -noecho`).
2. `interact -o -nobuffer -re <motif>` copies everything between your terminal and the shell; when the program's output matches a pattern, auto-yes checks that pause is not active and that the screen has stayed quiet for `AUTO_YES_CALME` ms, then sends `1` and Enter, and logs the whole thing.
3. A `trap … WINCH` copies the window size (`stty rows/columns`) onto the shell's pseudo-terminal and sends it `SIGWINCH`.

<a id="depannage"></a>

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| While editing a command recalled with ↑/↓, the line shifts or disappears | versions ≤ 1.1: the window size wasn't relayed, bash stayed at 80 columns. Fixed in 1.2; open a new terminal after updating. `stty size` should show the real size. |
| A "1" appears when nobody asked for it | the displayed text matches a pattern and the screen then stayed quiet (versions ≤ 1.2: no such wait). `auto-yes --journal` shows which program and text; tighten the pattern, increase `AUTO_YES_CALME`, or `auto-yes --pause` for the duration of the operation. |
| Nothing gets answered | check the pattern with `AUTO_YES_PATTERNS`; a menu drawn with cursor sequences (without real line breaks) doesn't match `\n`. |
| The terminal opens at root instead of the current folder | "GNOME Terminal profile" method: switch to the `~/.bashrc` method. |
| A real menu isn't confirmed even though it's recognized | the program keeps displaying output (animation, clock): the log shows `ignoré:défilement`. Lower `AUTO_YES_CALME` or set it to `0` for that program. |
| Disable everywhere for a while | `auto-yes --pause` (then `--reprise`); or `AUTO_YES_ACTIVE=1 bash` for a shell without auto-yes. |

<a id="depot"></a>

## Repository layout

| Path | Content |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | Expect scripts |
| `bin/auto-yes-configurer-gnome-terminal` | wiring into the GNOME Terminal profile |
| `share/auto-yes/commun.tcl` | common code: patterns, quiet screen, log, pause, window size |
| `man/` | man page `auto-yes(1)` |
| `etc/patterns.conf` | shipped patterns (`/etc/auto-yes/patterns.conf`, configuration file preserved across updates) |
| `packaging/` | `install.sh` (shared), `build-deb.sh`, `control`, `changelog`, `copyright`, packaging scripts; `rpm/auto-yes.spec`, `aur/PKGBUILD` |
| `tests/test_auto_yes.py` | pseudo-terminal tests: resizing, recognized menu, standalone phrase and scrolling text ignored, log, pause |
| `docs/readme/` | this README in 18 other languages |

<a id="deb"></a>

## Building the package

```bash
python3 -m unittest discover -s tests -v   # tests (expect required)
packaging/build-deb.sh                     # → dist/auto-yes_<version>_all.deb
```

The version comes from the first line of `packaging/changelog`. On every published release, `.github/workflows/release.yml` builds and attaches the RPM, Arch packages and AUR files.

<a id="licence"></a>

## License

[MIT](../../LICENSE).

<a id="soutien"></a>

## Support the project

If this project is useful to you, a coffee helps maintain it:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Bug reports and ideas: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Security vulnerabilities: [SECURITY.md](../../SECURITY.md).
