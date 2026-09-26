# Security policy / Politique de sécurité

## 🇬🇧 English

### Supported versions

Only the latest release receives security fixes. Please update first (the
[Releases](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest) page) and check that the problem is still there.

| Version | Supported |
|---|---|
| latest release | ✅ |
| older releases | ❌ |

### Reporting a vulnerability

**Please do not open a public issue.** Use GitHub's private reporting instead:
[Report a vulnerability](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/security/advisories/new)
(tab *Security → Report a vulnerability*).

Please include the version, your distribution and terminal, the steps to reproduce, and what an
attacker could achieve. You can write in English or French.

What to expect: an acknowledgement within 7 days, an assessment within 14 days, and for a confirmed
issue a fixed release as soon as possible, published with a GitHub security advisory crediting you
(unless you prefer not to be named).

### Scope

In scope: everything in this repository, in particular:

- how patterns are read from `/etc/auto-yes/patterns.conf` (and `AUTO_YES_PATTERNS`) and matched;
- anything that makes auto-yes answer a prompt that no configured pattern matches, or send anything
  other than `1` + Enter;
- the GNOME Terminal profile helper and the package maintainer scripts.

Out of scope, by design: a configured pattern answering a prompt you did not expect (auto-yes
confirms **every** prompt matching your patterns — keep them narrow), text displayed by a program
that matches a pattern, physical access to the computer, and vulnerabilities in Expect, Tcl, bash or
the terminal emulator — please report those upstream.

---

## 🇫🇷 Français

### Versions prises en charge

Seule la dernière version reçoit les correctifs de sécurité. Mettez d'abord à jour (page
[Releases](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)) et vérifiez que le problème persiste.

| Version | Prise en charge |
|---|---|
| dernière version | ✅ |
| versions antérieures | ❌ |

### Signaler une faille

**N'ouvrez pas de ticket public.** Utilisez le signalement privé de GitHub :
[Signaler une faille](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/security/advisories/new)
(onglet *Security → Report a vulnerability*).

Indiquez la version, votre distribution et votre terminal, les étapes pour reproduire, et ce qu'un
attaquant pourrait obtenir. En français ou en anglais.

À quoi vous attendre : un accusé de réception sous 7 jours, une évaluation sous 14 jours, et pour une
faille confirmée une version corrigée au plus vite, publiée avec un avis de sécurité GitHub qui vous
cite (sauf si vous préférez rester anonyme).

### Périmètre

Dans le périmètre : tout ce dépôt, en particulier :

- la lecture des motifs depuis `/etc/auto-yes/patterns.conf` (et `AUTO_YES_PATTERNS`) et leur
  correspondance ;
- tout ce qui ferait répondre auto-yes à une demande qu'aucun motif configuré ne reconnaît, ou
  envoyer autre chose que `1` + Entrée ;
- l'assistant de profil GNOME Terminal et les scripts du paquet.

Hors périmètre, par conception : un motif configuré qui répond à une demande inattendue (auto-yes
confirme **toute** demande qui correspond à vos motifs — gardez-les étroits), un texte affiché par un
programme qui correspond à un motif, l'accès physique à l'ordinateur, et les failles d'Expect, Tcl,
bash ou de l'émulateur de terminal — à signaler à leurs auteurs.
