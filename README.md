<p align="center">
  <img src="docs/images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — répondre « 1 » tout seul aux demandes de confirmation

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![Licence MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-soutenir-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

Dans un terminal Linux, **auto-yes** surveille ce qu'affichent les programmes et, dès qu'un menu de confirmation reconnu apparaît (par défaut « Do you want to proceed? » suivi de « 1. Yes »), tape **1** puis Entrée à votre place. Le terminal reste pleinement interactif : frappe, Ctrl-C, redimensionnement, couleurs.

<div align="center">

**🇫🇷 Français** · [🇬🇧 English](docs/readme/README.en.md) · [🇪🇸 Español](docs/readme/README.es.md) · [🇩🇪 Deutsch](docs/readme/README.de.md) · [🇮🇹 Italiano](docs/readme/README.it.md) · [🇧🇷 Português](docs/readme/README.pt-BR.md) · [🇳🇱 Nederlands](docs/readme/README.nl.md) · [🇵🇱 Polski](docs/readme/README.pl.md) · [🇷🇺 Русский](docs/readme/README.ru.md) · [🇺🇦 Українська](docs/readme/README.uk.md) · [🇹🇷 Türkçe](docs/readme/README.tr.md) · [🇸🇦 العربية](docs/readme/README.ar.md) · [🇮🇳 हिन्दी](docs/readme/README.hi.md) · [🇨🇳 简体中文](docs/readme/README.zh-CN.md) · [🇹🇼 繁體中文](docs/readme/README.zh-TW.md) · [🇯🇵 日本語](docs/readme/README.ja.md) · [🇰🇷 한국어](docs/readme/README.ko.md) · [🇻🇳 Tiếng Việt](docs/readme/README.vi.md) · [🇮🇩 Bahasa Indonesia](docs/readme/README.id.md)

</div>

<p align="center"><img src="docs/images/demo.svg" alt="auto-yes en action" width="760"><br><em>Le menu apparaît, auto-yes répond « 1 », la commande continue.</em></p>

> ⚠️ **À utiliser en connaissance de cause.** auto-yes confirme **n'importe quelle** demande qui correspond à un motif configuré, y compris celles d'une commande destructrice (suppression de paquets, outils de disque) ou d'un autre programme qui demande votre accord. Gardez des motifs étroits.

---

## Sommaire

- [Ce que fait le projet](#projet)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Motifs](#motifs)
- [Comment ça marche](#fonctionnement)
- [Dépannage](#depannage)
- [Organisation du dépôt](#depot)
- [Construire le paquet](#deb)
- [Licence](#licence)
- [Soutenir le projet](#soutien)

---

<a id="projet"></a>

## Ce que fait le projet

| Commande | Rôle |
|---|---|
| `auto-yes <commande> [arguments…]` | lance **une** commande et répond à ses demandes de confirmation |
| `auto-yes-shell` | remplace le shell de connexion : **toutes** les commandes tapées dans ce terminal en profitent, sans préfixe |
| `auto-yes-configurer-gnome-terminal` | branche `auto-yes-shell` sur le profil GNOME Terminal par défaut (`--revert` pour revenir en arrière) |

- **Terminal intact** : `spawn` + `interact` d'Expect ; tout ce que vous tapez passe, seul le motif déclenche un envoi.
- **Redimensionnement relayé** : quand la fenêtre change de taille, le shell et les programmes le savent (édition de l'historique, `less`, `vim`, `htop` restent justes).
- **Motifs modifiables sans réinstaller** : `/etc/auto-yes/patterns.conf`, relu à chaque nouveau terminal.
- **Pas de double emballage** : un terminal déjà sous auto-yes qui en relance un autre ne s'emballe pas deux fois (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Installation

### Paquet Debian / Ubuntu

Téléchargez le `.deb` de la [dernière release](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest), puis :

```bash
sudo apt install ./auto-yes_*_all.deb
```

Seule dépendance : `expect` (≥ 5.45).

### Depuis les sources

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Utilisation

### Une seule commande

```bash
auto-yes apt install paquet
auto-yes ./script-interactif.sh --option
```

### Tout un terminal

**Méthode recommandée — `~/.bashrc`** (garde le dossier de départ, par exemple avec *Ouvrir dans un terminal* du gestionnaire de fichiers) ; à placer à la fin du fichier :

```bash
# auto-yes dans tout terminal interactif (pas de double emballage, shells non interactifs exclus)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Autre méthode — profil GNOME Terminal** (à lancer en tant que vous-même, jamais avec `sudo`) :

```bash
auto-yes-configurer-gnome-terminal           # nouvelles fenêtres et onglets → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # revenir en arrière
```

Cette méthode ne touche ni les terminaux déjà ouverts, ni `gnome-terminal -- <commande>`, ni les autres émulateurs.

<a id="motifs"></a>

## Motifs

`/etc/auto-yes/patterns.conf` : une expression régulière Tcl (`interact -re`) par ligne ; les lignes vides et celles qui commencent par `#` sont ignorées. Motif livré :

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Il exige la question **et**, sur la ligne suivante, le choix `1.` d'un menu numéroté : la phrase seule (affichée par `cat`, `echo`, un journal) ne déclenche rien.

| Règle | Pourquoi |
|---|---|
| Viser le menu complet, pas une phrase isolée | un texte qui cite la phrase ne doit pas déclencher de réponse |
| `\s` ou `\y` pour les limites, jamais `\b` | en Tcl, `\b` est un retour arrière, pas une limite de mot |
| `(?i)` en tête pour ignorer la casse | les programmes varient « Proceed » / « proceed » |
| Tester avec `AUTO_YES_PATTERNS=fichier auto-yes …` | la variable remplace `/etc/auto-yes/patterns.conf` pour un essai |

<a id="fonctionnement"></a>

## Comment ça marche

1. `auto-yes-shell` lit les motifs, pose `AUTO_YES_ACTIVE=1`, puis lance `$SHELL -l` dans un pseudo-terminal (`spawn -noecho`).
2. `interact -o -nobuffer -re <motif> { send "1\r" }` recopie tout entre votre terminal et le shell ; quand la sortie du programme correspond à un motif, Expect envoie `1` et Entrée.
3. Un `trap … WINCH` recopie la taille de la fenêtre (`stty rows/columns`) sur le pseudo-terminal du shell et lui envoie `SIGWINCH`.

<a id="depannage"></a>

## Dépannage

| Symptôme | Cause et remède |
|---|---|
| En éditant une commande rappelée par ↑/↓, la ligne se décale ou disparaît | versions ≤ 1.1 : la taille de la fenêtre n'était pas relayée, bash restait à 80 colonnes. Corrigé en 1.2 ; ouvrez un nouveau terminal après la mise à jour. `stty size` doit afficher la taille réelle. |
| Un « 1 » apparaît alors que personne ne l'a demandé | le texte affiché correspond à un motif (par exemple un programme qui affiche un menu de confirmation cité, ou le code d'un motif). Resserrez le motif, ou lancez ce programme hors d'auto-yes (`AUTO_YES_ACTIVE=1 bash`). |
| Rien n'est répondu | vérifiez le motif avec `AUTO_YES_PATTERNS` ; un menu dessiné par séquences de curseur (sans vrais retours à la ligne) ne correspond pas à `\n`. |
| Le terminal s'ouvre à la racine au lieu du dossier courant | méthode « profil GNOME Terminal » : passez à la méthode `~/.bashrc`. |
| Désactiver pour une session | `AUTO_YES_ACTIVE=1 bash` ouvre un shell sans auto-yes. |

<a id="depot"></a>

## Organisation du dépôt

| Chemin | Contenu |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | scripts Expect |
| `bin/auto-yes-configurer-gnome-terminal` | branchement sur le profil GNOME Terminal |
| `etc/patterns.conf` | motifs livrés (`/etc/auto-yes/patterns.conf`, fichier de configuration conservé aux mises à jour) |
| `packaging/` | `build-deb.sh`, `control`, `changelog`, `copyright`, scripts du paquet |
| `tests/test_auto_yes.py` | essais en pseudo-terminal : redimensionnement, menu reconnu, phrase seule ignorée |
| `docs/readme/` | ce README en 18 autres langues |

<a id="deb"></a>

## Construire le paquet

```bash
python3 -m unittest discover -s tests -v   # essais (expect requis)
packaging/build-deb.sh                     # → dist/auto-yes_<version>_all.deb
```

La version vient de la première ligne de `packaging/changelog`.

<a id="licence"></a>

## Licence

[MIT](LICENSE).

<a id="soutien"></a>

## Soutenir le projet

Si ce projet vous rend service, un café aide à le maintenir :

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Offrir%20un%20café&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Rapports de bugs et idées : [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Failles de sécurité : [SECURITY.md](SECURITY.md).
