<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — rispondere «1» da solo alle richieste di conferma

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![Licenza MIT](https://img.shields.io/badge/licenza-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-sostieni-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

In un terminale Linux, **auto-yes** sorveglia ciò che i programmi visualizzano e, non appena appare un menu di conferma riconosciuto (di default «Do you want to proceed?» seguito da «1. Yes»), digita **1** e poi Invio al posto vostro. Il terminale resta pienamente interattivo: digitazione, Ctrl-C, ridimensionamento, colori.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · **🇮🇹 Italiano** · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes in azione" width="760"><br><em>Il menu appare, auto-yes risponde «1», il comando continua.</em></p>

> ⚠️ **Da usare con cognizione di causa.** auto-yes conferma **qualsiasi** richiesta che corrisponda a un motivo configurato, compresa quella di un comando distruttivo (rimozione di pacchetti, strumenti disco) o di un altro programma che chiede il vostro consenso. Mantenete i motivi ristretti.

---

## Sommario

- [Cosa fa il progetto](#projet)
- [Installazione](#installation)
- [Utilizzo](#utilisation)
- [Motivi](#motifs)
- [Come funziona](#fonctionnement)
- [Risoluzione dei problemi](#depannage)
- [Organizzazione del repository](#depot)
- [Costruire il pacchetto](#deb)
- [Licenza](#licence)
- [Sostenere il progetto](#soutien)

---

<a id="projet"></a>

## Cosa fa il progetto

| Comando | Ruolo |
|---|---|
| `auto-yes <comando> [argomenti…]` | avvia **un** comando e risponde alle sue richieste di conferma |
| `auto-yes-shell` | sostituisce la shell di login: **tutti** i comandi digitati in quel terminale ne beneficiano, senza prefisso |
| `auto-yes-configurer-gnome-terminal` | collega `auto-yes-shell` al profilo predefinito di GNOME Terminal (`--revert` per tornare indietro) |
| `auto-yes --pause` / `--reprise` | sospende / ripristina le risposte in **tutti** i terminali, anche quelli già aperti |
| `auto-yes --etat` / `--journal [N]` | stato attuale; ultime N risposte registrate |

- **Terminale intatto**: `spawn` + `interact` di Expect; tutto ciò che digitate passa, solo il motivo attiva un invio.
- **Schermo silenzioso**: la risposta viene inviata solo se nulla viene visualizzato 300 ms dopo il menu; una domanda citata in un testo che scorre viene ignorata.
- **Registro**: ogni motivo riconosciuto viene registrato (data, risposta o motivo dell'astensione, programma in primo piano, testo) in `~/.local/state/auto-yes/journal.log`.
- **Ridimensionamento trasmesso**: quando la finestra cambia dimensione, la shell e i programmi lo sanno (modifica della cronologia, `less`, `vim`, `htop` restano corretti).
- **Motivi modificabili senza reinstallare**: `/etc/auto-yes/patterns.conf`, riletto a ogni nuovo terminale.
- **Nessun doppio incapsulamento**: un terminale già sotto auto-yes che ne rilancia un altro non si incapsula due volte (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Installazione

### Pacchetto Debian / Ubuntu

Scaricate il `.deb` dall'[ultima release](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest), poi:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Dipendenze: `expect` (≥ 5.45) e `procps`.

### Fedora, openSUSE… (RPM) e Arch Linux

La stessa release fornisce `auto-yes-<version>-1.noarch.rpm` (`sudo dnf install ./auto-yes-*.noarch.rpm`), il `.src.rpm`, il pacchetto Arch (`sudo pacman -U auto-yes-*.pkg.tar.zst`) e i file AUR (`aur-<version>.tar.gz`: `PKGBUILD` e `.SRCINFO`).

### Dai sorgenti

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Utilizzo

### Un solo comando

```bash
auto-yes apt install pacchetto
auto-yes ./script-interattivo.sh --opzione
```

### Un intero terminale

**Metodo consigliato — `~/.bashrc`** (mantiene la cartella di partenza, ad esempio con *Apri nel terminale* del gestore file); da inserire alla fine del file:

```bash
# auto-yes in ogni terminale interattivo (nessun doppio incapsulamento, shell non interattive escluse)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Altro metodo — profilo GNOME Terminal** (da avviare come voi stessi, mai con `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # nuove finestre e schede → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # tornare indietro
```

Questo metodo non tocca né i terminali già aperti, né `gnome-terminal -- <comando>`, né altri emulatori.

<a id="motifs"></a>

## Motivi

`/etc/auto-yes/patterns.conf`: un'espressione regolare Tcl (`interact -re`) per riga; le righe vuote e quelle che iniziano con `#` sono ignorate. Motivo fornito:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Richiede la domanda **e**, sulla riga successiva, la scelta `1.` di un menu numerato: la frase da sola (mostrata da `cat`, `echo`, un log) non attiva nulla.

| Regola | Perché |
|---|---|
| Puntare al menu completo, non a una frase isolata | un testo che cita la frase non deve attivare una risposta |
| `\s` o `\y` per i limiti, mai `\b` | in Tcl, `\b` è un backspace, non un limite di parola |
| `(?i)` all'inizio per ignorare maiuscole/minuscole | i programmi variano tra «Proceed» / «proceed» |
| Testare con `AUTO_YES_PATTERNS=file auto-yes …` | la variabile sostituisce `/etc/auto-yes/patterns.conf` per una prova |

### Variabili d'ambiente

| Variabile | Ruolo | Predefinito |
|---|---|---|
| `AUTO_YES_PATTERNS` | file dei motivi | `/etc/auto-yes/patterns.conf` |
| `AUTO_YES_CALME` | silenzio richiesto dopo il menu, in millisecondi (`0`: risposta immediata) | `300` |
| `AUTO_YES_JOURNAL` | file di registro (vuoto: nulla viene registrato) | `~/.local/state/auto-yes/journal.log` |
| `AUTO_YES_ETAT` | cartella di stato (flag di pausa) | `~/.local/state/auto-yes` |

Guida completa: `man auto-yes`.

<a id="fonctionnement"></a>

## Come funziona

1. `auto-yes-shell` legge i motivi, imposta `AUTO_YES_ACTIVE=1`, poi avvia `$SHELL -l` in uno pseudo-terminale (`spawn -noecho`).
2. `interact -o -nobuffer -re <motivo>` copia tutto tra il vostro terminale e la shell; quando l'output del programma corrisponde a un motivo, auto-yes verifica che la pausa non sia attiva e che lo schermo sia rimasto silenzioso per `AUTO_YES_CALME` ms, quindi invia `1` e Invio, e registra il tutto nel log.
3. Un `trap … WINCH` copia la dimensione della finestra (`stty rows/columns`) sullo pseudo-terminale della shell e le invia `SIGWINCH`.

<a id="depannage"></a>

## Risoluzione dei problemi

| Sintomo | Causa e rimedio |
|---|---|
| Modificando un comando richiamato con ↑/↓, la riga si sposta o scompare | versioni ≤ 1.1: la dimensione della finestra non veniva trasmessa, bash restava a 80 colonne. Corretto nella 1.2; aprite un nuovo terminale dopo l'aggiornamento. `stty size` deve mostrare la dimensione reale. |
| Appare un «1» senza che nessuno lo abbia richiesto | il testo visualizzato corrisponde a un motivo e lo schermo è rimasto silenzioso in seguito (versioni ≤ 1.2: nessuna attesa). `auto-yes --journal` mostra quale programma e quale testo; restringete il motivo, aumentate `AUTO_YES_CALME`, oppure usate `auto-yes --pause` per la durata dell'operazione. |
| Non viene data alcuna risposta | verificate il motivo con `AUTO_YES_PATTERNS`; un menu disegnato con sequenze del cursore (senza veri a capo) non corrisponde a `\n`. |
| Il terminale si apre nella radice invece che nella cartella corrente | metodo «profilo GNOME Terminal»: passate al metodo `~/.bashrc`. |
| Un vero menu non viene confermato benché sia riconosciuto | il programma continua a visualizzare output (animazione, orologio): il registro indica `ignoré:défilement`. Abbassate `AUTO_YES_CALME` o impostatelo a `0` per quel programma. |
| Disattivare ovunque per un momento | `auto-yes --pause` (poi `--reprise`); oppure `AUTO_YES_ACTIVE=1 bash` per una shell senza auto-yes. |

<a id="depot"></a>

## Organizzazione del repository

| Percorso | Contenuto |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | script Expect |
| `bin/auto-yes-configurer-gnome-terminal` | collegamento al profilo GNOME Terminal |
| `share/auto-yes/commun.tcl` | codice comune: motivi, schermo silenzioso, registro, pausa, dimensione finestra |
| `man/` | pagina di manuale `auto-yes(1)` |
| `etc/patterns.conf` | motivi forniti (`/etc/auto-yes/patterns.conf`, file di configurazione conservato negli aggiornamenti) |
| `packaging/` | `install.sh` (comune), `build-deb.sh`, `control`, `changelog`, `copyright`, script del pacchetto; `rpm/auto-yes.spec`, `aur/PKGBUILD` |
| `tests/test_auto_yes.py` | test in pseudo-terminale: ridimensionamento, menu riconosciuto, frase isolata e testo che scorre ignorati, registro, pausa |
| `docs/readme/` | questo README in altre 18 lingue |

<a id="deb"></a>

## Costruire il pacchetto

```bash
python3 -m unittest discover -s tests -v   # test (richiede expect)
packaging/build-deb.sh                     # → dist/auto-yes_<versione>_all.deb
```

La versione proviene dalla prima riga di `packaging/changelog`. A ogni release pubblicata, `.github/workflows/release.yml` costruisce e allega i pacchetti RPM, Arch e i file AUR.

<a id="licence"></a>

## Licenza

[MIT](../../LICENSE).

<a id="soutien"></a>

## Sostenere il progetto

Se questo progetto vi è utile, un caffè aiuta a mantenerlo:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Offrimi%20un%20caffè&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Segnalazioni di bug e idee: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Falle di sicurezza: [SECURITY.md](../../SECURITY.md).
