<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — automatisch «1» antwoorden op bevestigingsvragen

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![Licentie MIT](https://img.shields.io/badge/licentie-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-steun-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

In een Linux-terminal houdt **auto-yes** in de gaten wat programma's weergeven en zodra een herkend bevestigingsmenu verschijnt (standaard "Do you want to proceed?" gevolgd door "1. Yes"), typt het **1** en daarna Enter in uw plaats. De terminal blijft volledig interactief: typen, Ctrl-C, formaat wijzigen, kleuren.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · **🇳🇱 Nederlands** · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes in actie" width="760"><br><em>Het menu verschijnt, auto-yes antwoordt "1", het commando gaat door.</em></p>

> ⚠️ **Met kennis van zaken gebruiken.** auto-yes bevestigt **elk** verzoek dat overeenkomt met een geconfigureerd patroon, ook dat van een destructief commando (pakketten verwijderen, schijftools) of een ander programma dat om uw toestemming vraagt. Houd patronen nauw.

---

## Inhoudsopgave

- [Wat het project doet](#projet)
- [Installatie](#installation)
- [Gebruik](#utilisation)
- [Patronen](#motifs)
- [Hoe het werkt](#fonctionnement)
- [Probleemoplossing](#depannage)
- [Structuur van de repository](#depot)
- [Het pakket bouwen](#deb)
- [Licentie](#licence)
- [Het project steunen](#soutien)

---

<a id="projet"></a>

## Wat het project doet

| Commando | Rol |
|---|---|
| `auto-yes <commando> [argumenten…]` | start **één** commando en beantwoordt de bevestigingsvragen ervan |
| `auto-yes-shell` | vervangt de login-shell: **alle** commando's die in deze terminal worden getypt, profiteren ervan, zonder voorvoegsel |
| `auto-yes-configurer-gnome-terminal` | koppelt `auto-yes-shell` aan het standaardprofiel van GNOME Terminal (`--revert` om terug te draaien) |
| `auto-yes --pause` / `--reprise` | schorst / herstelt het automatisch beantwoorden in **alle** terminals, ook reeds geopende |
| `auto-yes --etat` / `--journal [N]` | huidige status; laatste N genoteerde antwoorden |

- **Terminal blijft intact**: `spawn` + `interact` van Expect; alles wat u typt gaat door, alleen het patroon activeert een verzending.
- **Rustig scherm**: het antwoord wordt alleen verstuurd als er 300 ms na het menu niets wordt weergegeven; een vraag die geciteerd wordt in doorlopende tekst wordt genegeerd.
- **Logboek**: elk herkend patroon wordt genoteerd (datum, antwoord of reden van onthouding, programma op de voorgrond, tekst) in `~/.local/state/auto-yes/journal.log`.
- **Formaatwijziging doorgegeven**: wanneer het venster van formaat verandert, weten de shell en de programma's dit (geschiedenis bewerken, `less`, `vim`, `htop` blijven correct).
- **Patronen aanpasbaar zonder herinstallatie**: `/etc/auto-yes/patterns.conf`, opnieuw ingelezen bij elke nieuwe terminal.
- **Geen dubbele inwikkeling**: een terminal die al onder auto-yes draait en er nog een start, wikkelt zichzelf niet twee keer in (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Installatie

### Debian-/Ubuntu-pakket

Download de `.deb` van de [laatste release](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest), daarna:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Afhankelijkheden: `expect` (≥ 5.45) en `procps`.

### Fedora, openSUSE… (RPM) en Arch Linux

Dezelfde release levert `auto-yes-<versie>-1.noarch.rpm` (`sudo dnf install ./auto-yes-*.noarch.rpm`), de `.src.rpm`, het Arch-pakket (`sudo pacman -U auto-yes-*.pkg.tar.zst`) en de AUR-bestanden (`aur-<versie>.tar.gz`: `PKGBUILD` en `.SRCINFO`).

### Vanuit de broncode

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Gebruik

### Eén enkel commando

```bash
auto-yes apt install pakket
auto-yes ./interactief-script.sh --optie
```

### Een hele terminal

**Aanbevolen methode — `~/.bashrc`** (behoudt de startmap, bijvoorbeeld met *Openen in terminal* van de bestandsbeheerder); helemaal onderaan het bestand plaatsen:

```bash
# auto-yes in elke interactieve terminal (geen dubbele inwikkeling, niet-interactieve shells uitgesloten)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Andere methode — GNOME Terminal-profiel** (start als uzelf, nooit met `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # nieuwe vensters en tabbladen → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # terugdraaien
```

Deze methode raakt noch reeds geopende terminals, noch `gnome-terminal -- <commando>`, noch andere emulatoren.

<a id="motifs"></a>

## Patronen

`/etc/auto-yes/patterns.conf`: één Tcl-reguliere expressie (`interact -re`) per regel; lege regels en regels die beginnen met `#` worden genegeerd. Meegeleverd patroon:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Het vereist de vraag **en**, op de volgende regel, de keuze `1.` van een genummerd menu: de zin alleen (weergegeven door `cat`, `echo`, een logboek) activeert niets.

| Regel | Waarom |
|---|---|
| Richten op het volledige menu, niet op een geïsoleerde zin | tekst die de zin citeert mag geen reactie activeren |
| `\s` of `\y` voor grenzen, nooit `\b` | in Tcl is `\b` een backspace, geen woordgrens |
| `(?i)` aan het begin om hoofdletters te negeren | programma's variëren tussen "Proceed" / "proceed" |
| Testen met `AUTO_YES_PATTERNS=bestand auto-yes …` | de variabele vervangt `/etc/auto-yes/patterns.conf` voor een test |

### Omgevingsvariabelen

| Variabele | Rol | Standaard |
|---|---|---|
| `AUTO_YES_PATTERNS` | patronenbestand | `/etc/auto-yes/patterns.conf` |
| `AUTO_YES_CALME` | vereiste stilte na het menu, in milliseconden (`0`: onmiddellijk antwoord) | `300` |
| `AUTO_YES_JOURNAL` | logboekbestand (leeg: er wordt niets genoteerd) | `~/.local/state/auto-yes/journal.log` |
| `AUTO_YES_ETAT` | statusmap (pauzevlag) | `~/.local/state/auto-yes` |

Volledige hulp: `man auto-yes`.

<a id="fonctionnement"></a>

## Hoe het werkt

1. `auto-yes-shell` leest de patronen, stelt `AUTO_YES_ACTIVE=1` in, en start dan `$SHELL -l` in een pseudoterminal (`spawn -noecho`).
2. `interact -o -nobuffer -re <patroon>` kopieert alles tussen uw terminal en de shell; wanneer de uitvoer van het programma overeenkomt met een patroon, controleert auto-yes of de pauze niet actief is en of het scherm `AUTO_YES_CALME` ms rustig is gebleven, stuurt dan `1` en Enter, en noteert alles in het logboek.
3. Een `trap … WINCH` kopieert de venstergrootte (`stty rows/columns`) naar de pseudoterminal van de shell en stuurt hem `SIGWINCH`.

<a id="depannage"></a>

## Probleemoplossing

| Symptoom | Oorzaak en oplossing |
|---|---|
| Bij het bewerken van een met ↑/↓ opgeroepen commando verschuift of verdwijnt de regel | versies ≤ 1.1: de venstergrootte werd niet doorgegeven, bash bleef op 80 kolommen. Opgelost in 1.2; open een nieuwe terminal na de update. `stty size` moet de werkelijke grootte tonen. |
| Er verschijnt een "1" terwijl niemand erom heeft gevraagd | de weergegeven tekst komt overeen met een patroon en het scherm is daarna rustig gebleven (versies ≤ 1.2: geen wachttijd). `auto-yes --journal` toont welk programma en welke tekst; vernauw het patroon, verhoog `AUTO_YES_CALME`, of gebruik `auto-yes --pause` voor de duur van de bewerking. |
| Er wordt niets beantwoord | controleer het patroon met `AUTO_YES_PATTERNS`; een menu getekend met cursorreeksen (zonder echte regeleinden) komt niet overeen met `\n`. |
| De terminal opent in de root in plaats van de huidige map | methode "GNOME Terminal-profiel": schakel over naar de `~/.bashrc`-methode. |
| Een echt menu wordt niet bevestigd terwijl het wel wordt herkend | het programma blijft iets weergeven (animatie, klok): het logboek vermeldt `ignoré:défilement`. Verlaag `AUTO_YES_CALME` of zet het op `0` voor dat programma. |
| Overal tijdelijk uitschakelen | `auto-yes --pause` (daarna `--reprise`); of `AUTO_YES_ACTIVE=1 bash` voor een shell zonder auto-yes. |

<a id="depot"></a>

## Structuur van de repository

| Pad | Inhoud |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | Expect-scripts |
| `bin/auto-yes-configurer-gnome-terminal` | koppeling met het GNOME Terminal-profiel |
| `share/auto-yes/commun.tcl` | gedeelde code: patronen, rustig scherm, logboek, pauze, venstergrootte |
| `man/` | man-pagina `auto-yes(1)` |
| `etc/patterns.conf` | meegeleverde patronen (`/etc/auto-yes/patterns.conf`, configuratiebestand blijft behouden bij updates) |
| `packaging/` | `install.sh` (gedeeld), `build-deb.sh`, `control`, `changelog`, `copyright`, pakketscripts; `rpm/auto-yes.spec`, `aur/PKGBUILD` |
| `tests/test_auto_yes.py` | tests in pseudoterminal: formaatwijziging, herkend menu, geïsoleerde zin en doorlopende tekst genegeerd, logboek, pauze |
| `docs/readme/` | deze README in 18 andere talen |

<a id="deb"></a>

## Het pakket bouwen

```bash
python3 -m unittest discover -s tests -v   # tests (expect vereist)
packaging/build-deb.sh                     # → dist/auto-yes_<versie>_all.deb
```

De versie komt uit de eerste regel van `packaging/changelog`. Bij elke gepubliceerde release bouwt en voegt `.github/workflows/release.yml` de RPM- en Arch-pakketten en de AUR-bestanden toe.

<a id="licence"></a>

## Licentie

[MIT](../../LICENSE).

<a id="soutien"></a>

## Het project steunen

Als dit project u van dienst is, helpt een kopje koffie om het te onderhouden:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Trakteer%20een%20koffie&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Bugmeldingen en ideeën: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Beveiligingslekken: [SECURITY.md](../../SECURITY.md).
