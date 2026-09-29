# Contributing — Contribuer

## 🇬🇧 English

### Contributions welcome

auto-yes watches what programs print in a Linux terminal and answers `1` + Enter when a recognised confirmation
menu appears, while the terminal stays fully interactive. It is small (Expect scripts and a common Tcl file), and
every change can make it answer something it should not: bug reports, new terminal setups, ideas and pull requests
are welcome, reviewed with that in mind.

- Quick feedback on an idea or a bug: open an [issue](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues).
  Attach the relevant lines of `auto-yes --journal` when auto-yes answered (or did not answer) a prompt.
- Security problems: do **not** open an issue, follow [`SECURITY.md`](SECURITY.md).

### Contribution workflow

The project uses the fork-and-pull model.

1. In your fork, create a branch with a meaningful name.
2. Make your change, meeting the [quality standards](#quality-standards) below.
3. Open a pull request against `main`.
4. A maintainer reviews it. Address every comment; amend your commits and force-push your branch rather than
   stacking "fix review" commits.
5. Once approved, a maintainer merges it. Your commits keep your authorship.

Do not change the version: it comes from the first line of `packaging/changelog`, and releases (changelog,
packages, release notes) are made by a maintainer.

### Request for comments

To get feedback on a direction before writing the whole thing, open a pull request whose title starts with `[RFC]`,
based on the current code. Write down in the pull request what was concluded.

### Quality standards

The repository is written in **French**: comments, documentation, messages and commit messages. If French is a
barrier, write in English and a maintainer will translate — the content matters more than the language.

Before opening a pull request (Debian/Ubuntu: `sudo apt install expect lintian`):

```bash
python3 -m unittest discover -s tests -v   # pseudo-terminal tests, Expect required
packaging/build-deb.sh                     # → dist/auto-yes_<version>_all.deb
lintian --fail-on error dist/*.deb
```

Your contribution must meet these standards:

- **One logical change per commit**, with a descriptive message (title ≤ 72 characters, then the why).
- **Every commit passes the test suite.** A fix or a new behaviour comes with a test in `tests/test_auto_yes.py`
  that **fails without your change**; a test that cannot fail is not a test.
- **auto-yes answers only what a pattern matches, and only `1` + Enter.** A change to matching, to the quiet-screen
  delay (`AUTO_YES_CALME`) or to the pause comes with tests on both sides: the real menu gets its answer, and the
  sentence alone, text that scrolls past and a paused shell get nothing.
- **Shipped patterns stay narrow.** A pattern added to `etc/patterns.conf` targets a complete menu (question *and*
  numbered choice), never an isolated sentence, and comes with its two tests (menu answered, sentence alone
  ignored). Tcl regexp: `\s` or `\y` for boundaries, never `\b` (a backspace in Tcl).
- **The terminal stays fully interactive**: typing, Ctrl-C, window resizing, colours. The resize tests must keep
  passing.
- **Documentation follows the code.** A new option or variable goes into the manual page (`man/`), into
  `auto-yes --help` and into the README, which exists in 19 languages (`README.md` and `docs/readme/`).
- **Comments explain why**, especially where a decision looks arbitrary.
- **No personal data** in tracked files or in the examples: no home paths (`/home/<name>`), e-mail addresses or
  tokens; check what a journal excerpt contains before sharing it.
- **Explain your pull request**: the reasoning behind each change and the testing done (distribution, shell,
  terminal emulator, Expect version).
- **You answer for every line you submit**, whatever tools helped you write it.

### Developer Certificate of Origin

auto-yes is released under the [MIT licence](LICENSE). To make sure every contribution is correctly attributed and
licensed, each commit must carry a `Signed-off-by` line, by which you agree to the Developer Certificate of Origin
1.1 (<https://developercertificate.org/>):

```
Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the
    best of my knowledge, is covered under an appropriate open
    source license and I have the right under that license to
    submit that work with modifications, whether created in whole
    or in part by me, under the same open source license (unless
    I am permitted to submit under a different license), as
    indicated in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including
    all personal information I submit with it, including my
    sign-off) is maintained indefinitely and may be redistributed
    consistent with this project or the open source license(s)
    involved.
```

Use `git commit -s`. A stable pseudonym is accepted, as long as it identifies you consistently across your
contributions. Forgot it? `git commit --amend -s`.

---

## 🇫🇷 Français

### Les contributions sont les bienvenues

auto-yes surveille ce qu'affichent les programmes dans un terminal Linux et répond `1` puis Entrée quand un menu de
confirmation reconnu apparaît, le terminal restant pleinement interactif. Il est petit (scripts Expect et un fichier
Tcl commun), et chaque changement peut le faire répondre à ce qu'il ne devrait pas : rapports de bogue, nouvelles
configurations de terminal, idées et demandes de fusion sont les bienvenus, relus dans cet esprit.

- Avis rapide sur une idée ou un bogue : ouvrez un [ticket](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues).
  Joignez les lignes utiles de `auto-yes --journal` quand auto-yes a répondu (ou pas) à une demande.
- Problème de sécurité : n'ouvrez **pas** de ticket, suivez [`SECURITY.md`](SECURITY.md).

### Déroulement

Le projet suit le modèle « fork and pull ».

1. Dans votre fork, créez une branche au nom parlant.
2. Faites votre changement en respectant les [exigences de qualité](#exigences-de-qualité) ci-dessous.
3. Ouvrez une demande de fusion (pull request) vers `main`.
4. Une personne de l'équipe la relit. Répondez à chaque remarque ; modifiez vos commits et repoussez votre branche
   (push forcé) plutôt que d'empiler des commits « correction de relecture ».
5. Une fois acceptée, elle est fusionnée par l'équipe. Vos commits gardent leur auteur.

Ne changez pas la version : elle vient de la première ligne de `packaging/changelog`, et les versions (changelog,
paquets, notes de version) sont faites par l'équipe.

### Demande de commentaires

Pour un avis sur une direction avant de tout écrire, ouvrez une demande de fusion dont le titre commence par `[RFC]`,
bâtie sur le code actuel. Notez dans la demande ce qui a été conclu.

### Exigences de qualité

Le dépôt est rédigé **en français** : commentaires, documentation, messages et messages de commit. Si le français
vous bloque, écrivez en anglais : l'équipe traduira — le fond compte plus que la langue.

Avant d'ouvrir une demande (Debian/Ubuntu : `sudo apt install expect lintian`) :

```bash
python3 -m unittest discover -s tests -v   # essais en pseudo-terminal, Expect requis
packaging/build-deb.sh                     # → dist/auto-yes_<version>_all.deb
lintian --fail-on error dist/*.deb
```

Votre contribution doit respecter ces règles :

- **Un changement logique par commit**, avec un message parlant (titre ≤ 72 caractères, puis le pourquoi).
- **Chaque commit passe la suite de tests.** Un correctif ou un comportement neuf arrive avec un test dans
  `tests/test_auto_yes.py` qui **échoue sans votre changement** ; un test qui ne peut pas échouer n'est pas un test.
- **auto-yes ne répond qu'à ce qu'un motif reconnaît, et seulement `1` puis Entrée.** Un changement de la
  reconnaissance, du délai d'écran calme (`AUTO_YES_CALME`) ou de la pause arrive avec des tests des deux côtés : le
  vrai menu reçoit sa réponse, et la phrase seule, un texte qui défile et un shell en pause ne reçoivent rien.
- **Les motifs livrés restent étroits.** Un motif ajouté à `etc/patterns.conf` vise un menu complet (question *et*
  choix numéroté), jamais une phrase isolée, et arrive avec ses deux tests (menu confirmé, phrase seule ignorée).
  Regexp Tcl : `\s` ou `\y` pour les limites, jamais `\b` (un retour arrière en Tcl).
- **Le terminal reste pleinement interactif** : frappe, Ctrl-C, redimensionnement, couleurs. Les tests de
  redimensionnement doivent continuer de passer.
- **La documentation suit le code.** Une option ou une variable neuve entre dans la page de manuel (`man/`), dans
  `auto-yes --help` et dans le README, qui existe en 19 langues (`README.md` et `docs/readme/`).
- **Les commentaires expliquent le pourquoi**, surtout là où une décision paraît arbitraire.
- **Aucune donnée personnelle** dans les fichiers suivis ni dans les exemples : ni chemin personnel (`/home/<nom>`),
  ni courriel, ni jeton ; relisez un extrait de journal avant de le partager.
- **Expliquez votre demande** : la raison de chaque changement et les essais faits (distribution, shell, émulateur
  de terminal, version d'Expect).
- **Vous répondez de chaque ligne soumise**, quels que soient les outils qui vous ont aidé à l'écrire.

### Certificat d'origine du développeur

auto-yes est publié sous [licence MIT](LICENSE). Pour que chaque contribution soit correctement attribuée et placée
sous licence, chaque commit porte une ligne `Signed-off-by`, par laquelle vous acceptez le Developer Certificate of
Origin 1.1 (<https://developercertificate.org/>), reproduit en anglais dans la section ci-dessus : ce texte fait foi
dans sa langue d'origine.

Utilisez `git commit -s`. Un pseudonyme stable est accepté, pourvu qu'il vous identifie de façon constante d'une
contribution à l'autre. Oubli ? `git commit --amend -s`.
