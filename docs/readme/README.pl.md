<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — automatyczna odpowiedź „1" na prośby o potwierdzenie

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![Licencja MIT](https://img.shields.io/badge/licencja-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-wesprzyj-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

W terminalu Linux **auto-yes** obserwuje to, co wyświetlają programy, i gdy tylko pojawi się rozpoznane menu potwierdzenia (domyślnie „Do you want to proceed?" a następnie „1. Yes"), wpisuje za Ciebie **1**, a potem Enter. Terminal pozostaje w pełni interaktywny: pisanie, Ctrl-C, zmiana rozmiaru, kolory.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · **🇵🇱 Polski** · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes w akcji" width="760"><br><em>Menu się pojawia, auto-yes odpowiada „1", polecenie jest kontynuowane.</em></p>

> ⚠️ **Używaj ze świadomością.** auto-yes potwierdza **każde** żądanie odpowiadające skonfigurowanemu wzorcowi, w tym żądanie polecenia destrukcyjnego (usuwanie pakietów, narzędzia dyskowe) lub innego programu proszącego o Twoją zgodę. Utrzymuj wzorce wąskie.

---

## Spis treści

- [Co robi projekt](#projet)
- [Instalacja](#installation)
- [Użycie](#utilisation)
- [Wzorce](#motifs)
- [Jak to działa](#fonctionnement)
- [Rozwiązywanie problemów](#depannage)
- [Struktura repozytorium](#depot)
- [Budowanie pakietu](#deb)
- [Licencja](#licence)
- [Wesprzyj projekt](#soutien)

---

<a id="projet"></a>

## Co robi projekt

| Polecenie | Rola |
|---|---|
| `auto-yes <polecenie> [argumenty…]` | uruchamia **jedno** polecenie i odpowiada na jego prośby o potwierdzenie |
| `auto-yes-shell` | zastępuje powłokę logowania: **wszystkie** polecenia wpisywane w tym terminalu korzystają z tego, bez przedrostka |
| `auto-yes-configurer-gnome-terminal` | podłącza `auto-yes-shell` do domyślnego profilu GNOME Terminal (`--revert`, aby cofnąć) |
| `auto-yes --pause` / `--reprise` | wstrzymuje / przywraca automatyczne odpowiadanie we **wszystkich** terminalach, nawet już otwartych |
| `auto-yes --etat` / `--journal [N]` | aktualny stan; N ostatnich zanotowanych odpowiedzi |

- **Terminal nienaruszony**: `spawn` + `interact` z Expect; wszystko, co wpisujesz, jest przekazywane, tylko wzorzec wyzwala wysyłkę.
- **Cichy ekran**: odpowiedź jest wysyłana tylko wtedy, gdy nic się nie wyświetla przez 300 ms po menu; pytanie zacytowane w przewijającym się tekście jest ignorowane.
- **Dziennik**: każdy rozpoznany wzorzec jest zapisywany (data, odpowiedź lub powód wstrzymania, program na pierwszym planie, tekst) w `~/.local/state/auto-yes/journal.log`.
- **Zmiana rozmiaru przekazywana**: gdy okno zmienia rozmiar, powłoka i programy o tym wiedzą (edycja historii, `less`, `vim`, `htop` pozostają poprawne).
- **Wzorce modyfikowalne bez ponownej instalacji**: `/etc/auto-yes/patterns.conf`, wczytywany ponownie przy każdym nowym terminalu.
- **Bez podwójnego opakowania**: terminal już działający pod auto-yes, który uruchamia kolejny, nie opakowuje się dwukrotnie (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Instalacja

### Pakiet Debian / Ubuntu

Pobierz plik `.deb` z [ostatniego wydania](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest), a następnie:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Zależności: `expect` (≥ 5.45) i `procps`.

### Fedora, openSUSE… (RPM) i Arch Linux

To samo wydanie zawiera `auto-yes-<wersja>-1.noarch.rpm` (`sudo dnf install ./auto-yes-*.noarch.rpm`), plik `.src.rpm`, pakiet Arch (`sudo pacman -U auto-yes-*.pkg.tar.zst`) oraz pliki AUR (`aur-<wersja>.tar.gz`: `PKGBUILD` i `.SRCINFO`).

### Ze źródeł

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Użycie

### Pojedyncze polecenie

```bash
auto-yes apt install pakiet
auto-yes ./skrypt-interaktywny.sh --opcja
```

### Cały terminal

**Zalecana metoda — `~/.bashrc`** (zachowuje folder początkowy, na przykład dzięki *Otwórz w terminalu* menedżera plików); umieść na końcu pliku:

```bash
# auto-yes w każdym interaktywnym terminalu (bez podwójnego opakowania, powłoki nieinteraktywne wykluczone)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Inna metoda — profil GNOME Terminal** (uruchom jako Ty sam, nigdy z `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # nowe okna i karty → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # cofnij
```

Ta metoda nie dotyka ani już otwartych terminali, ani `gnome-terminal -- <polecenie>`, ani innych emulatorów.

<a id="motifs"></a>

## Wzorce

`/etc/auto-yes/patterns.conf`: jedno wyrażenie regularne Tcl (`interact -re`) na linię; puste linie i te zaczynające się od `#` są ignorowane. Dostarczony wzorzec:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Wymaga pytania **oraz**, w następnej linii, opcji `1.` z ponumerowanego menu: samo zdanie (wyświetlone przez `cat`, `echo`, dziennik) niczego nie wyzwala.

| Zasada | Dlaczego |
|---|---|
| Celować w całe menu, nie w izolowane zdanie | tekst cytujący zdanie nie powinien wyzwalać odpowiedzi |
| `\s` lub `\y` na granice, nigdy `\b` | w Tcl `\b` to backspace, a nie granica słowa |
| `(?i)` na początku, by ignorować wielkość liter | programy różnią się między „Proceed" / „proceed" |
| Testuj za pomocą `AUTO_YES_PATTERNS=plik auto-yes …` | zmienna zastępuje `/etc/auto-yes/patterns.conf` do próby |

### Zmienne środowiskowe

| Zmienna | Rola | Domyślnie |
|---|---|---|
| `AUTO_YES_PATTERNS` | plik wzorców | `/etc/auto-yes/patterns.conf` |
| `AUTO_YES_CALME` | wymagana cisza po menu, w milisekundach (`0`: natychmiastowa odpowiedź) | `300` |
| `AUTO_YES_JOURNAL` | plik dziennika (pusty: nic nie jest zapisywane) | `~/.local/state/auto-yes/journal.log` |
| `AUTO_YES_ETAT` | katalog stanu (flaga pauzy) | `~/.local/state/auto-yes` |

Pełna pomoc: `man auto-yes`.

<a id="fonctionnement"></a>

## Jak to działa

1. `auto-yes-shell` czyta wzorce, ustawia `AUTO_YES_ACTIVE=1`, a następnie uruchamia `$SHELL -l` w pseudoterminalu (`spawn -noecho`).
2. `interact -o -nobuffer -re <wzorzec>` kopiuje wszystko między Twoim terminalem a powłoką; gdy wyjście programu pasuje do wzorca, auto-yes sprawdza, czy pauza nie jest aktywna i czy ekran pozostaje cichy przez `AUTO_YES_CALME` ms, a następnie wysyła `1` i Enter, i zapisuje to wszystko w dzienniku.
3. `trap … WINCH` kopiuje rozmiar okna (`stty rows/columns`) do pseudoterminalu powłoki i wysyła jej `SIGWINCH`.

<a id="depannage"></a>

## Rozwiązywanie problemów

| Objaw | Przyczyna i rozwiązanie |
|---|---|
| Podczas edycji polecenia przywołanego strzałkami ↑/↓ linia przesuwa się lub znika | wersje ≤ 1.1: rozmiar okna nie był przekazywany, bash pozostawał przy 80 kolumnach. Naprawione w 1.2; otwórz nowy terminal po aktualizacji. `stty size` powinno pokazywać rzeczywisty rozmiar. |
| Pojawia się „1", choć nikt o to nie prosił | wyświetlony tekst pasuje do wzorca, a ekran pozostał potem cichy (wersje ≤ 1.2: brak oczekiwania). `auto-yes --journal` pokazuje, który program i jaki tekst; zawęź wzorzec, zwiększ `AUTO_YES_CALME`, albo użyj `auto-yes --pause` na czas operacji. |
| Nic nie jest odpowiadane | sprawdź wzorzec za pomocą `AUTO_YES_PATTERNS`; menu narysowane sekwencjami kursora (bez prawdziwych znaków nowej linii) nie pasuje do `\n`. |
| Terminal otwiera się w katalogu głównym zamiast w bieżącym folderze | metoda „profil GNOME Terminal": przejdź na metodę `~/.bashrc`. |
| Prawdziwe menu nie jest potwierdzane, mimo że jest rozpoznane | program nadal coś wyświetla (animacja, zegar): dziennik pokazuje `ignoré:défilement`. Zmniejsz `AUTO_YES_CALME` albo ustaw `0` dla tego programu. |
| Wyłączyć wszędzie na chwilę | `auto-yes --pause` (a potem `--reprise`); albo `AUTO_YES_ACTIVE=1 bash` dla powłoki bez auto-yes. |

<a id="depot"></a>

## Struktura repozytorium

| Ścieżka | Zawartość |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | skrypty Expect |
| `bin/auto-yes-configurer-gnome-terminal` | podłączenie do profilu GNOME Terminal |
| `share/auto-yes/commun.tcl` | wspólny kod: wzorce, cichy ekran, dziennik, pauza, rozmiar okna |
| `man/` | strona podręcznika `auto-yes(1)` |
| `etc/patterns.conf` | dostarczone wzorce (`/etc/auto-yes/patterns.conf`, plik konfiguracyjny zachowywany przy aktualizacjach) |
| `packaging/` | `install.sh` (wspólny), `build-deb.sh`, `control`, `changelog`, `copyright`, skrypty pakietu; `rpm/auto-yes.spec`, `aur/PKGBUILD` |
| `tests/test_auto_yes.py` | testy w pseudoterminalu: zmiana rozmiaru, rozpoznane menu, ignorowanie samodzielnej frazy i przewijającego się tekstu, dziennik, pauza |
| `docs/readme/` | ten README w 18 innych językach |

<a id="deb"></a>

## Budowanie pakietu

```bash
python3 -m unittest discover -s tests -v   # testy (wymaga expect)
packaging/build-deb.sh                     # → dist/auto-yes_<wersja>_all.deb
```

Wersja pochodzi z pierwszej linii `packaging/changelog`. Przy każdym opublikowanym wydaniu `.github/workflows/release.yml` buduje i dołącza pakiety RPM, Arch oraz pliki AUR.

<a id="licence"></a>

## Licencja

[MIT](../../LICENSE).

<a id="soutien"></a>

## Wesprzyj projekt

Jeśli ten projekt Ci się przydaje, kawa pomaga go utrzymać:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Postaw%20kawę&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Zgłoszenia błędów i pomysły: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Luki bezpieczeństwa: [SECURITY.md](../../SECURITY.md).
