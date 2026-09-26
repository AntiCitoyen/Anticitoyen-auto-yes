<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — автоматически отвечает «1» на запросы подтверждения

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![Лицензия MIT](https://img.shields.io/badge/лицензия-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-поддержать-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

В терминале Linux **auto-yes** следит за тем, что выводят программы, и как только появляется распознанное меню подтверждения (по умолчанию «Do you want to proceed?» с последующим «1. Yes»), вводит за вас **1**, а затем Enter. Терминал остаётся полностью интерактивным: набор текста, Ctrl-C, изменение размера, цвета.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · **🇷🇺 Русский** · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes в действии" width="760"><br><em>Появляется меню, auto-yes отвечает «1», команда продолжается.</em></p>

> ⚠️ **Используйте осознанно.** auto-yes подтверждает **любой** запрос, соответствующий настроенному шаблону, включая запрос деструктивной команды (удаление пакетов, дисковые утилиты) или другой программы, запрашивающей ваше согласие. Держите шаблоны узкими.

---

## Содержание

- [Что делает проект](#projet)
- [Установка](#installation)
- [Использование](#utilisation)
- [Шаблоны](#motifs)
- [Как это работает](#fonctionnement)
- [Устранение неполадок](#depannage)
- [Структура репозитория](#depot)
- [Сборка пакета](#deb)
- [Лицензия](#licence)
- [Поддержать проект](#soutien)

---

<a id="projet"></a>

## Что делает проект

| Команда | Роль |
|---|---|
| `auto-yes <команда> [аргументы…]` | запускает **одну** команду и отвечает на её запросы подтверждения |
| `auto-yes-shell` | заменяет login-оболочку: **все** команды, набранные в этом терминале, получают выгоду без префикса |
| `auto-yes-configurer-gnome-terminal` | подключает `auto-yes-shell` к профилю GNOME Terminal по умолчанию (`--revert` для отката) |
| `auto-yes --pause` / `--reprise` | приостанавливает / восстанавливает автоматические ответы во **всех** терминалах, даже уже открытых |
| `auto-yes --etat` / `--journal [N]` | текущее состояние; N последних зафиксированных ответов |

- **Терминал остаётся нетронутым**: `spawn` + `interact` из Expect; всё, что вы вводите, проходит, только шаблон вызывает отправку.
- **Тихий экран**: ответ отправляется только если ничего не выводится в течение 300 мс после меню; вопрос, процитированный в прокручивающемся тексте, игнорируется.
- **Журнал**: каждый распознанный шаблон записывается (дата, ответ или причина воздержания, программа на переднем плане, текст) в `~/.local/state/auto-yes/journal.log`.
- **Изменение размера передаётся**: когда окно меняет размер, оболочка и программы об этом узнают (редактирование истории, `less`, `vim`, `htop` остаются корректными).
- **Шаблоны изменяются без переустановки**: `/etc/auto-yes/patterns.conf`, перечитывается при каждом новом терминале.
- **Без двойной обёртки**: терминал, уже работающий под auto-yes, который запускает ещё один, не оборачивается дважды (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Установка

### Пакет Debian / Ubuntu

Скачайте `.deb` из [последнего релиза](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest), затем:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Зависимости: `expect` (≥ 5.45) и `procps`.

### Fedora, openSUSE… (RPM) и Arch Linux

Тот же релиз включает `auto-yes-<версия>-1.noarch.rpm` (`sudo dnf install ./auto-yes-*.noarch.rpm`), `.src.rpm`, пакет Arch (`sudo pacman -U auto-yes-*.pkg.tar.zst`) и файлы AUR (`aur-<версия>.tar.gz`: `PKGBUILD` и `.SRCINFO`).

### Из исходников

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Использование

### Одна команда

```bash
auto-yes apt install пакет
auto-yes ./интерактивный-скрипт.sh --опция
```

### Целый терминал

**Рекомендуемый способ — `~/.bashrc`** (сохраняет начальную папку, например с *Открыть в терминале* из файлового менеджера); поместите в конец файла:

```bash
# auto-yes в каждом интерактивном терминале (без двойной обёртки, неинтерактивные оболочки исключены)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Другой способ — профиль GNOME Terminal** (запускать от своего имени, никогда с `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # новые окна и вкладки → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # откатить
```

Этот способ не затрагивает ни уже открытые терминалы, ни `gnome-terminal -- <команда>`, ни другие эмуляторы.

<a id="motifs"></a>

## Шаблоны

`/etc/auto-yes/patterns.conf`: одно регулярное выражение Tcl (`interact -re`) на строку; пустые строки и начинающиеся с `#` игнорируются. Поставляемый шаблон:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Он требует вопрос **и**, на следующей строке, выбор `1.` из пронумерованного меню: одна лишь фраза (выведенная `cat`, `echo`, журналом) ничего не вызывает.

| Правило | Почему |
|---|---|
| Нацеливаться на полное меню, а не на изолированную фразу | текст, цитирующий фразу, не должен вызывать ответ |
| `\s` или `\y` для границ, никогда `\b` | в Tcl `\b` — это backspace, а не граница слова |
| `(?i)` в начале, чтобы игнорировать регистр | программы варьируют «Proceed» / «proceed» |
| Тестировать с `AUTO_YES_PATTERNS=файл auto-yes …` | переменная заменяет `/etc/auto-yes/patterns.conf` для пробы |

### Переменные окружения

| Переменная | Роль | По умолчанию |
|---|---|---|
| `AUTO_YES_PATTERNS` | файл шаблонов | `/etc/auto-yes/patterns.conf` |
| `AUTO_YES_CALME` | требуемая тишина после меню, в миллисекундах (`0`: немедленный ответ) | `300` |
| `AUTO_YES_JOURNAL` | файл журнала (пусто: ничего не записывается) | `~/.local/state/auto-yes/journal.log` |
| `AUTO_YES_ETAT` | каталог состояния (флаг паузы) | `~/.local/state/auto-yes` |

Полная справка: `man auto-yes`.

<a id="fonctionnement"></a>

## Как это работает

1. `auto-yes-shell` читает шаблоны, устанавливает `AUTO_YES_ACTIVE=1`, затем запускает `$SHELL -l` в псевдотерминале (`spawn -noecho`).
2. `interact -o -nobuffer -re <шаблон>` копирует всё между вашим терминалом и оболочкой; когда вывод программы соответствует шаблону, auto-yes проверяет, что пауза не активна и что экран остаётся тихим `AUTO_YES_CALME` мс, затем отправляет `1` и Enter, и записывает всё в журнал.
3. `trap … WINCH` копирует размер окна (`stty rows/columns`) в псевдотерминал оболочки и посылает ей `SIGWINCH`.

<a id="depannage"></a>

## Устранение неполадок

| Симптом | Причина и решение |
|---|---|
| При редактировании команды, вызванной ↑/↓, строка смещается или исчезает | версии ≤ 1.1: размер окна не передавался, bash оставался на 80 столбцах. Исправлено в 1.2; откройте новый терминал после обновления. `stty size` должна показывать реальный размер. |
| Появляется «1», хотя никто его не запрашивал | отображаемый текст соответствует шаблону, и после этого экран оставался тихим (версии ≤ 1.2: ожидания не было). `auto-yes --journal` показывает, какая программа и какой текст; сузьте шаблон, увеличьте `AUTO_YES_CALME`, либо используйте `auto-yes --pause` на время операции. |
| Ничего не отвечается | проверьте шаблон с `AUTO_YES_PATTERNS`; меню, нарисованное последовательностями курсора (без настоящих переводов строк), не соответствует `\n`. |
| Терминал открывается в корне вместо текущей папки | способ «профиль GNOME Terminal»: перейдите на способ `~/.bashrc`. |
| Настоящее меню не подтверждается, хотя распознано | программа продолжает что-то выводить (анимация, часы): журнал показывает `ignoré:défilement`. Уменьшите `AUTO_YES_CALME` либо поставьте `0` для этой программы. |
| Отключить везде на время | `auto-yes --pause` (затем `--reprise`); либо `AUTO_YES_ACTIVE=1 bash` для оболочки без auto-yes. |

<a id="depot"></a>

## Структура репозитория

| Путь | Содержимое |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | скрипты Expect |
| `bin/auto-yes-configurer-gnome-terminal` | подключение к профилю GNOME Terminal |
| `share/auto-yes/commun.tcl` | общий код: шаблоны, тихий экран, журнал, пауза, размер окна |
| `man/` | страница руководства `auto-yes(1)` |
| `etc/patterns.conf` | поставляемые шаблоны (`/etc/auto-yes/patterns.conf`, конфигурационный файл сохраняется при обновлениях) |
| `packaging/` | `install.sh` (общий), `build-deb.sh`, `control`, `changelog`, `copyright`, скрипты пакета; `rpm/auto-yes.spec`, `aur/PKGBUILD` |
| `tests/test_auto_yes.py` | тесты в псевдотерминале: изменение размера, распознанное меню, игнорирование изолированной фразы и прокручивающегося текста, журнал, пауза |
| `docs/readme/` | этот README на 18 других языках |

<a id="deb"></a>

## Сборка пакета

```bash
python3 -m unittest discover -s tests -v   # тесты (требуется expect)
packaging/build-deb.sh                     # → dist/auto-yes_<версия>_all.deb
```

Версия берётся из первой строки `packaging/changelog`. При каждом опубликованном релизе `.github/workflows/release.yml` собирает и прикрепляет пакеты RPM, Arch и файлы AUR.

<a id="licence"></a>

## Лицензия

[MIT](../../LICENSE).

<a id="soutien"></a>

## Поддержать проект

Если этот проект вам полезен, чашка кофе поможет его поддерживать:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Угостить%20кофе&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Отчёты об ошибках и идеи: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Уязвимости безопасности: [SECURITY.md](../../SECURITY.md).
