<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — самостійно відповідає «1» на запити підтвердження

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![Ліцензія MIT](https://img.shields.io/badge/ліцензія-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-підтримати-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

У терміналі Linux **auto-yes** стежить за тим, що виводять програми, і щойно з'являється розпізнане меню підтвердження (за замовчуванням «Do you want to proceed?» з наступним «1. Yes»), вводить замість вас **1**, а потім Enter. Термінал залишається повністю інтерактивним: набір тексту, Ctrl-C, зміна розміру, кольори.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · **🇺🇦 Українська** · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes у дії" width="760"><br><em>З'являється меню, auto-yes відповідає «1», команда продовжується.</em></p>

> ⚠️ **Використовуйте свідомо.** auto-yes підтверджує **будь-який** запит, що відповідає налаштованому шаблону, зокрема запит деструктивної команди (видалення пакунків, дискові утиліти) або іншої програми, що просить вашої згоди. Тримайте шаблони вузькими.

---

## Зміст

- [Що робить проєкт](#projet)
- [Встановлення](#installation)
- [Використання](#utilisation)
- [Шаблони](#motifs)
- [Як це працює](#fonctionnement)
- [Усунення несправностей](#depannage)
- [Структура репозиторію](#depot)
- [Збірка пакунка](#deb)
- [Ліцензія](#licence)
- [Підтримати проєкт](#soutien)

---

<a id="projet"></a>

## Що робить проєкт

| Команда | Роль |
|---|---|
| `auto-yes <команда> [аргументи…]` | запускає **одну** команду і відповідає на її запити підтвердження |
| `auto-yes-shell` | замінює login-оболонку: **всі** команди, введені в цьому терміналі, отримують вигоду без префікса |
| `auto-yes-configurer-gnome-terminal` | підключає `auto-yes-shell` до типового профілю GNOME Terminal (`--revert` для відкату) |
| `auto-yes --pause` / `--reprise` | призупиняє / відновлює відповіді в **усіх** терміналах, навіть уже відкритих |
| `auto-yes --etat` / `--journal [N]` | поточний стан; N останніх записаних відповідей |

- **Термінал залишається незмінним**: `spawn` + `interact` з Expect; усе, що ви вводите, проходить, лише шаблон запускає надсилання.
- **Тихий екран**: відповідь надсилається, лише якщо нічого не виводиться протягом 300 мс після меню; питання, процитоване в тексті, що прокручується, ігнорується.
- **Журнал**: кожен розпізнаний шаблон записується (дата, відповідь або причина утримання, програма на передньому плані, текст) у `~/.local/state/auto-yes/journal.log`.
- **Зміна розміру передається**: коли вікно змінює розмір, оболонка і програми про це знають (редагування історії, `less`, `vim`, `htop` лишаються коректними).
- **Шаблони змінюються без перевстановлення**: `/etc/auto-yes/patterns.conf`, перечитується при кожному новому терміналі.
- **Без подвійного обгортання**: термінал, що вже працює під auto-yes і запускає ще один, не обгортається двічі (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Встановлення

### Пакунок Debian / Ubuntu

Завантажте `.deb` з [останнього релізу](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest), потім:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Залежності: `expect` (≥ 5.45) і `procps`.

### Fedora, openSUSE… (RPM) і Arch Linux

Той самий реліз містить `auto-yes-<версія>-1.noarch.rpm` (`sudo dnf install ./auto-yes-*.noarch.rpm`), `.src.rpm`, пакунок Arch (`sudo pacman -U auto-yes-*.pkg.tar.zst`) і файли AUR (`aur-<версія>.tar.gz`: `PKGBUILD` і `.SRCINFO`).

### З вихідного коду

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Використання

### Одна команда

```bash
auto-yes apt install пакунок
auto-yes ./інтерактивний-скрипт.sh --опція
```

### Цілий термінал

**Рекомендований спосіб — `~/.bashrc`** (зберігає початкову теку, наприклад через *Відкрити в терміналі* файлового менеджера); додайте в кінець файлу:

```bash
# auto-yes у кожному інтерактивному терміналі (без подвійного обгортання, неінтерактивні оболонки виключено)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Інший спосіб — профіль GNOME Terminal** (запускайте від свого імені, ніколи з `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # нові вікна і вкладки → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # відкотити
```

Цей спосіб не зачіпає ні вже відкриті термінали, ні `gnome-terminal -- <команда>`, ні інші емулятори.

<a id="motifs"></a>

## Шаблони

`/etc/auto-yes/patterns.conf`: один регулярний вираз Tcl (`interact -re`) на рядок; порожні рядки та ті, що починаються з `#`, ігноруються. Наданий шаблон:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Він вимагає питання **та**, на наступному рядку, вибір `1.` з пронумерованого меню: сама фраза (виведена `cat`, `echo`, журналом) нічого не запускає.

| Правило | Чому |
|---|---|
| Цілитися в повне меню, а не в ізольовану фразу | текст, що цитує фразу, не повинен запускати відповідь |
| `\s` або `\y` для меж, ніколи `\b` | у Tcl `\b` — це backspace, а не межа слова |
| `(?i)` на початку, щоб ігнорувати регістр | програми варіюють «Proceed» / «proceed» |
| Тестувати з `AUTO_YES_PATTERNS=файл auto-yes …` | змінна замінює `/etc/auto-yes/patterns.conf` для проби |

### Змінні середовища

| Variable | Роль | За замовчуванням |
|---|---|---|
| `AUTO_YES_PATTERNS` | файл шаблонів | `/etc/auto-yes/patterns.conf` |
| `AUTO_YES_CALME` | тиша, яка потрібна після меню, у мілісекундах (`0`: негайна відповідь) | `300` |
| `AUTO_YES_JOURNAL` | файл журналу (порожньо: нічого не записується) | `~/.local/state/auto-yes/journal.log` |
| `AUTO_YES_ETAT` | тека стану (прапорець паузи) | `~/.local/state/auto-yes` |

Повна довідка: `man auto-yes`.

<a id="fonctionnement"></a>

## Як це працює

1. `auto-yes-shell` читає шаблони, встановлює `AUTO_YES_ACTIVE=1`, потім запускає `$SHELL -l` у псевдотерміналі (`spawn -noecho`).
2. `interact -o -nobuffer -re <шаблон>` копіює все між вашим терміналом і оболонкою; коли вивід програми відповідає шаблону, auto-yes перевіряє, що пауза не активна і що екран залишається тихим `AUTO_YES_CALME` мс, потім надсилає `1` і Enter, і записує все в журнал.
3. `trap … WINCH` копіює розмір вікна (`stty rows/columns`) у псевдотермінал оболонки і надсилає їй `SIGWINCH`.

<a id="depannage"></a>

## Усунення несправностей

| Симптом | Причина і рішення |
|---|---|
| Під час редагування команди, викликаної ↑/↓, рядок зміщується або зникає | версії ≤ 1.1: розмір вікна не передавався, bash залишався на 80 стовпцях. Виправлено в 1.2; відкрийте новий термінал після оновлення. `stty size` має показувати реальний розмір. |
| З'являється «1», хоча ніхто його не запитував | показаний текст відповідає шаблону, і після цього екран залишався тихим (версії ≤ 1.2: жодного очікування). `auto-yes --journal` показує, яка програма і який текст; звузьте шаблон, збільшіть `AUTO_YES_CALME`, або `auto-yes --pause` на час операції. |
| Нічого не відповідається | перевірте шаблон за допомогою `AUTO_YES_PATTERNS`; меню, намальоване послідовностями курсора (без справжніх переносів рядків), не відповідає `\n`. |
| Термінал відкривається в корені замість поточної теки | спосіб «профіль GNOME Terminal»: перейдіть на спосіб `~/.bashrc`. |
| Справжнє меню не підтверджується, хоча воно розпізнане | програма продовжує щось виводити (анімація, годинник): журнал показує `ignoré:défilement`. Зменшіть `AUTO_YES_CALME` або встановіть `0` для цієї програми. |
| Вимкнути всюди на якийсь час | `auto-yes --pause` (потім `--reprise`); або `AUTO_YES_ACTIVE=1 bash` для оболонки без auto-yes. |

<a id="depot"></a>

## Структура репозиторію

| Шлях | Вміст |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | скрипти Expect |
| `bin/auto-yes-configurer-gnome-terminal` | підключення до профілю GNOME Terminal |
| `share/auto-yes/commun.tcl` | спільний код: шаблони, тихий екран, журнал, пауза, розмір вікна |
| `man/` | сторінка довідки `auto-yes(1)` |
| `etc/patterns.conf` | надані шаблони (`/etc/auto-yes/patterns.conf`, конфігураційний файл зберігається при оновленнях) |
| `packaging/` | `install.sh` (спільний), `build-deb.sh`, `control`, `changelog`, `copyright`, скрипти пакунка; `rpm/auto-yes.spec`, `aur/PKGBUILD` |
| `tests/test_auto_yes.py` | тести в псевдотерміналі: зміна розміру, розпізнане меню, ізольована фраза та текст, що прокручується, ігноруються, журнал, пауза |
| `docs/readme/` | цей README ще 18 мовами |

<a id="deb"></a>

## Збірка пакунка

```bash
python3 -m unittest discover -s tests -v   # тести (потрібен expect)
packaging/build-deb.sh                     # → dist/auto-yes_<версія>_all.deb
```

Версія береться з першого рядка `packaging/changelog`. З кожним опублікованим релізом `.github/workflows/release.yml` збирає та додає пакунки RPM, Arch і файли AUR.

<a id="licence"></a>

## Ліцензія

[MIT](../../LICENSE).

<a id="soutien"></a>

## Підтримати проєкт

Якщо цей проєкт вам корисний, кава допоможе його підтримувати:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Пригостити%20кавою&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Звіти про помилки та ідеї: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Вразливості безпеки: [SECURITY.md](../../SECURITY.md).
