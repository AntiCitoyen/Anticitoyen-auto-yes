<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — automatisch mit „1" auf Bestätigungsabfragen antworten

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![Lizenz MIT](https://img.shields.io/badge/lizenz-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-unterstützen-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

In einem Linux-Terminal beobachtet **auto-yes**, was Programme anzeigen, und tippt, sobald ein erkanntes Bestätigungsmenü erscheint (standardmäßig „Do you want to proceed?" gefolgt von „1. Yes"), an Ihrer Stelle **1** und dann Enter. Das Terminal bleibt vollständig interaktiv: Tastatureingaben, Strg-C, Größenänderung, Farben.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · **🇩🇪 Deutsch** · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes in Aktion" width="760"><br><em>Das Menü erscheint, auto-yes antwortet „1", der Befehl läuft weiter.</em></p>

> ⚠️ **Mit Bedacht verwenden.** auto-yes bestätigt **jede** Anfrage, die einem konfigurierten Muster entspricht, auch die eines destruktiven Befehls (Paketentfernung, Festplatten-Tools) oder eines anderen Programms, das um Ihre Zustimmung bittet. Halten Sie die Muster eng gefasst.

---

## Inhalt

- [Was das Projekt macht](#projet)
- [Installation](#installation)
- [Verwendung](#utilisation)
- [Muster](#motifs)
- [So funktioniert es](#fonctionnement)
- [Fehlerbehebung](#depannage)
- [Aufbau des Repositorys](#depot)
- [Paket bauen](#deb)
- [Lizenz](#licence)
- [Projekt unterstützen](#soutien)

---

<a id="projet"></a>

## Was das Projekt macht

| Befehl | Rolle |
|---|---|
| `auto-yes <befehl> [argumente…]` | startet **einen** Befehl und beantwortet dessen Bestätigungsabfragen |
| `auto-yes-shell` | ersetzt die Login-Shell: **alle** in diesem Terminal getippten Befehle profitieren davon, ohne Präfix |
| `auto-yes-configurer-gnome-terminal` | verbindet `auto-yes-shell` mit dem GNOME-Terminal-Standardprofil (`--revert`, um es rückgängig zu machen) |
| `auto-yes --pause` / `--reprise` | setzt das automatische Antworten in **allen** Terminals aus / stellt es wieder her, auch in bereits geöffneten |
| `auto-yes --etat` / `--journal [N]` | aktueller Status; die letzten N protokollierten Antworten |

- **Terminal bleibt unangetastet**: `spawn` + `interact` von Expect; alles, was Sie tippen, wird durchgereicht, nur das Muster löst einen Versand aus.
- **Ruhiger Bildschirm**: die Antwort wird nur gesendet, wenn 300 ms nach dem Menü nichts angezeigt wird; eine in durchlaufendem Text zitierte Frage wird ignoriert.
- **Protokoll**: jedes erkannte Muster wird protokolliert (Datum, Antwort oder Grund der Enthaltung, Programm im Vordergrund, Text) in `~/.local/state/auto-yes/journal.log`.
- **Größenänderung weitergeleitet**: wenn sich die Fenstergröße ändert, wissen Shell und Programme davon (Verlaufsbearbeitung, `less`, `vim`, `htop` bleiben korrekt).
- **Muster änderbar ohne Neuinstallation**: `/etc/auto-yes/patterns.conf`, bei jedem neuen Terminal neu eingelesen.
- **Keine doppelte Umhüllung**: ein bereits unter auto-yes laufendes Terminal, das ein weiteres startet, umhüllt sich nicht zweimal (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Installation

### Debian-/Ubuntu-Paket

Laden Sie das `.deb` von der [neuesten Release](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest) herunter, dann:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Abhängigkeiten: `expect` (≥ 5.45) und `procps`.

### Fedora, openSUSE… (RPM) und Arch Linux

Dieselbe Release stellt `auto-yes-<version>-1.noarch.rpm` (`sudo dnf install ./auto-yes-*.noarch.rpm`), das `.src.rpm`, das Arch-Paket (`sudo pacman -U auto-yes-*.pkg.tar.zst`) sowie die AUR-Dateien (`aur-<version>.tar.gz`: `PKGBUILD` und `.SRCINFO`) bereit.

### Aus dem Quellcode

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Verwendung

### Ein einzelner Befehl

```bash
auto-yes apt install paket
auto-yes ./interaktives-skript.sh --option
```

### Ein ganzes Terminal

**Empfohlene Methode — `~/.bashrc`** (behält den Startordner bei, zum Beispiel mit *Im Terminal öffnen* des Dateimanagers); ans Ende der Datei setzen:

```bash
# auto-yes in jedem interaktiven Terminal (keine doppelte Umhüllung, nicht-interaktive Shells ausgeschlossen)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Andere Methode — GNOME-Terminal-Profil** (als Sie selbst ausführen, niemals mit `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # neue Fenster und Tabs → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # rückgängig machen
```

Diese Methode betrifft weder bereits geöffnete Terminals noch `gnome-terminal -- <befehl>` noch andere Emulatoren.

<a id="motifs"></a>

## Muster

`/etc/auto-yes/patterns.conf`: ein Tcl-regulärer-Ausdruck (`interact -re`) pro Zeile; leere Zeilen und solche, die mit `#` beginnen, werden ignoriert. Mitgeliefertes Muster:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Es erfordert die Frage **und**, in der folgenden Zeile, die Auswahl `1.` eines nummerierten Menüs: der Satz allein (angezeigt von `cat`, `echo`, einem Log) löst nichts aus.

| Regel | Warum |
|---|---|
| Auf das vollständige Menü zielen, nicht auf einen isolierten Satz | ein Text, der den Satz zitiert, darf keine Antwort auslösen |
| `\s` oder `\y` für Grenzen, niemals `\b` | in Tcl ist `\b` ein Rückschritt, keine Wortgrenze |
| `(?i)` am Anfang, um Groß-/Kleinschreibung zu ignorieren | Programme variieren zwischen „Proceed" / „proceed" |
| Testen mit `AUTO_YES_PATTERNS=datei auto-yes …` | die Variable ersetzt `/etc/auto-yes/patterns.conf` für einen Test |

### Umgebungsvariablen

| Variable | Rolle | Standard |
|---|---|---|
| `AUTO_YES_PATTERNS` | Musterdatei | `/etc/auto-yes/patterns.conf` |
| `AUTO_YES_CALME` | erforderliche Stille nach dem Menü, in Millisekunden (`0`: sofortige Antwort) | `300` |
| `AUTO_YES_JOURNAL` | Protokolldatei (leer: nichts wird protokolliert) | `~/.local/state/auto-yes/journal.log` |
| `AUTO_YES_ETAT` | Statusverzeichnis (Pause-Flag) | `~/.local/state/auto-yes` |

Vollständige Hilfe: `man auto-yes`.

<a id="fonctionnement"></a>

## So funktioniert es

1. `auto-yes-shell` liest die Muster, setzt `AUTO_YES_ACTIVE=1`, startet dann `$SHELL -l` in einem Pseudo-Terminal (`spawn -noecho`).
2. `interact -o -nobuffer -re <muster>` kopiert alles zwischen Ihrem Terminal und der Shell; wenn die Ausgabe des Programms einem Muster entspricht, prüft auto-yes, dass die Pause nicht aktiv ist und der Bildschirm `AUTO_YES_CALME` ms ruhig geblieben ist, sendet dann `1` und Enter und protokolliert alles.
3. Ein `trap … WINCH` kopiert die Fenstergröße (`stty rows/columns`) auf das Pseudo-Terminal der Shell und sendet ihr `SIGWINCH`.

<a id="depannage"></a>

## Fehlerbehebung

| Symptom | Ursache und Abhilfe |
|---|---|
| Beim Bearbeiten eines mit ↑/↓ abgerufenen Befehls verschiebt sich die Zeile oder verschwindet | Versionen ≤ 1.1: die Fenstergröße wurde nicht weitergeleitet, bash blieb bei 80 Spalten. Behoben in 1.2; öffnen Sie nach dem Update ein neues Terminal. `stty size` sollte die tatsächliche Größe anzeigen. |
| Eine „1" erscheint, obwohl niemand danach gefragt hat | der angezeigte Text entspricht einem Muster, und der Bildschirm blieb danach ruhig (Versionen ≤ 1.2: keine Wartezeit). `auto-yes --journal` zeigt, welches Programm und welcher Text; schränken Sie das Muster ein, erhöhen Sie `AUTO_YES_CALME`, oder nutzen Sie `auto-yes --pause` für die Dauer des Vorgangs. |
| Nichts wird beantwortet | prüfen Sie das Muster mit `AUTO_YES_PATTERNS`; ein mit Cursor-Sequenzen gezeichnetes Menü (ohne echte Zeilenumbrüche) entspricht nicht `\n`. |
| Das Terminal öffnet sich im Wurzelverzeichnis statt im aktuellen Ordner | Methode „GNOME-Terminal-Profil": wechseln Sie zur `~/.bashrc`-Methode. |
| Ein echtes Menü wird nicht bestätigt, obwohl es erkannt wird | das Programm zeigt weiterhin etwas an (Animation, Uhr): das Protokoll zeigt `ignoré:défilement`. Senken Sie `AUTO_YES_CALME` oder setzen Sie es für dieses Programm auf `0`. |
| Überall vorübergehend deaktivieren | `auto-yes --pause` (danach `--reprise`); oder `AUTO_YES_ACTIVE=1 bash` für eine Shell ohne auto-yes. |

<a id="depot"></a>

## Aufbau des Repositorys

| Pfad | Inhalt |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | Expect-Skripte |
| `bin/auto-yes-configurer-gnome-terminal` | Anbindung an das GNOME-Terminal-Profil |
| `share/auto-yes/commun.tcl` | gemeinsamer Code: Muster, ruhiger Bildschirm, Protokoll, Pause, Fenstergröße |
| `man/` | Handbuchseite `auto-yes(1)` |
| `etc/patterns.conf` | mitgelieferte Muster (`/etc/auto-yes/patterns.conf`, Konfigurationsdatei bleibt bei Updates erhalten) |
| `packaging/` | `install.sh` (gemeinsam), `build-deb.sh`, `control`, `changelog`, `copyright`, Paketskripte; `rpm/auto-yes.spec`, `aur/PKGBUILD` |
| `tests/test_auto_yes.py` | Tests im Pseudo-Terminal: Größenänderung, erkanntes Menü, isolierter Satz und durchlaufender Text ignoriert, Protokoll, Pause |
| `docs/readme/` | dieses README in 18 weiteren Sprachen |

<a id="deb"></a>

## Paket bauen

```bash
python3 -m unittest discover -s tests -v   # Tests (expect erforderlich)
packaging/build-deb.sh                     # → dist/auto-yes_<version>_all.deb
```

Die Version stammt aus der ersten Zeile von `packaging/changelog`. Bei jeder veröffentlichten Release erstellt und fügt `.github/workflows/release.yml` die RPM- und Arch-Pakete sowie die AUR-Dateien hinzu.

<a id="licence"></a>

## Lizenz

[MIT](../../LICENSE).

<a id="soutien"></a>

## Projekt unterstützen

Wenn Ihnen dieses Projekt nützt, hilft ein Kaffee bei der Pflege:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Kaffee%20spendieren&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Fehlerberichte und Ideen: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Sicherheitslücken: [SECURITY.md](../../SECURITY.md).
