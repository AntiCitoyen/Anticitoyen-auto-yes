<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — يجيب «1» تلقائياً على طلبات التأكيد

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![رخصة MIT](https://img.shields.io/badge/رخصة-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ادعم-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

في طرفية لينكس، يراقب **auto-yes** ما تعرضه البرامج، وبمجرد ظهور قائمة تأكيد معروفة (افتراضياً «Do you want to proceed?» متبوعة بـ «1. Yes»)، يكتب **1** ثم Enter بدلاً منكم. تبقى الطرفية تفاعلية بالكامل: الكتابة، Ctrl-C، تغيير الحجم، الألوان.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · **🇸🇦 العربية** · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes قيد التشغيل" width="760"><br><em>تظهر القائمة، يجيب auto-yes بـ «1»، ويتابع الأمر.</em></p>

> ⚠️ **استخدموه بوعي.** يؤكد auto-yes **أي** طلب يطابق نمطاً مُعدّاً، بما في ذلك طلب أمر مدمّر (إزالة حزم، أدوات أقراص) أو برنامج آخر يطلب موافقتكم. حافظوا على أنماط ضيقة.

---

## المحتويات

- [ما يفعله المشروع](#projet)
- [التثبيت](#installation)
- [الاستخدام](#utilisation)
- [الأنماط](#motifs)
- [كيف يعمل](#fonctionnement)
- [استكشاف الأخطاء وإصلاحها](#depannage)
- [تنظيم المستودع](#depot)
- [بناء الحزمة](#deb)
- [الرخصة](#licence)
- [دعم المشروع](#soutien)

---

<a id="projet"></a>

## ما يفعله المشروع

| الأمر | الدور |
|---|---|
| `auto-yes <أمر> [وسائط…]` | يشغّل **أمراً واحداً** ويجيب على طلبات تأكيده |
| `auto-yes-shell` | يستبدل صدفة تسجيل الدخول: **جميع** الأوامر المكتوبة في هذه الطرفية تستفيد منه، دون بادئة |
| `auto-yes-configurer-gnome-terminal` | يربط `auto-yes-shell` بملف تعريف GNOME Terminal الافتراضي (`--revert` للتراجع) |

- **طرفية سليمة**: `spawn` + `interact` من Expect؛ كل ما تكتبونه يمر، والنمط وحده يُطلق إرسالاً.
- **تغيير الحجم مُرحَّل**: عند تغيير حجم النافذة، تعلم الصدفة والبرامج بذلك (تحرير السجل، `less`، `vim`، `htop` تبقى صحيحة).
- **أنماط قابلة للتعديل دون إعادة تثبيت**: `/etc/auto-yes/patterns.conf`، تُقرأ من جديد مع كل طرفية جديدة.
- **لا تغليف مزدوج**: طرفية تعمل بالفعل تحت auto-yes وتعيد تشغيل طرفية أخرى لا تُغلَّف مرتين (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## التثبيت

### حزمة Debian / Ubuntu

نزّلوا ملف `.deb` من [آخر إصدار](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)، ثم:

```bash
sudo apt install ./auto-yes_*_all.deb
```

الاعتماد الوحيد: `expect` (≥ 5.45).

### من المصدر

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## الاستخدام

### أمر واحد فقط

```bash
auto-yes apt install حزمة
auto-yes ./سكربت-تفاعلي.sh --خيار
```

### طرفية كاملة

**الطريقة الموصى بها — `~/.bashrc`** (تحافظ على مجلد الانطلاق، مثلاً باستخدام *فتح في الطرفية* من مدير الملفات)؛ ضعوها في نهاية الملف:

```bash
# auto-yes في كل طرفية تفاعلية (لا تغليف مزدوج، الصدفات غير التفاعلية مستبعدة)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**طريقة أخرى — ملف تعريف GNOME Terminal** (شغّلوها بحسابكم، أبداً بـ `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # النوافذ والألسنة الجديدة → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # التراجع
```

لا تمس هذه الطريقة الطرفيات المفتوحة بالفعل، ولا `gnome-terminal -- <أمر>`، ولا المحاكيات الأخرى.

<a id="motifs"></a>

## الأنماط

`/etc/auto-yes/patterns.conf`: تعبير نمطي واحد بلغة Tcl (`interact -re`) لكل سطر؛ تُتجاهل الأسطر الفارغة وتلك التي تبدأ بـ `#`. النمط المرفق:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

يتطلب السؤال **و**، في السطر التالي، خيار `1.` من قائمة مرقّمة: الجملة وحدها (المعروضة بواسطة `cat`، `echo`، سجل) لا تُطلق شيئاً.

| القاعدة | السبب |
|---|---|
| استهداف القائمة الكاملة، لا جملة معزولة | نص يقتبس الجملة يجب ألا يُطلق رداً |
| `\s` أو `\y` للحدود، أبداً `\b` | في Tcl، `\b` مسافة رجوع، وليس حد كلمة |
| `(?i)` في البداية لتجاهل حالة الأحرف | البرامج تتنوع بين «Proceed» / «proceed» |
| اختبروا بـ `AUTO_YES_PATTERNS=ملف auto-yes …` | المتغير يستبدل `/etc/auto-yes/patterns.conf` من أجل تجربة |

<a id="fonctionnement"></a>

## كيف يعمل

1. يقرأ `auto-yes-shell` الأنماط، يضبط `AUTO_YES_ACTIVE=1`، ثم يشغّل `$SHELL -l` في طرفية زائفة (`spawn -noecho`).
2. `interact -o -nobuffer -re <نمط> { send "1\r" }` ينسخ كل شيء بين طرفيتكم والصدفة؛ عندما يطابق خرج البرنامج نمطاً، يرسل Expect `1` ثم Enter.
3. `trap … WINCH` ينسخ حجم النافذة (`stty rows/columns`) إلى الطرفية الزائفة للصدفة ويرسل لها `SIGWINCH`.

<a id="depannage"></a>

## استكشاف الأخطاء وإصلاحها

| العرض | السبب والحل |
|---|---|
| عند تحرير أمر تم استدعاؤه بـ ↑/↓، ينزاح السطر أو يختفي | الإصدارات ≤ 1.1: لم يكن حجم النافذة يُرحَّل، وكانت bash تبقى عند 80 عموداً. أُصلح في 1.2؛ افتحوا طرفية جديدة بعد التحديث. يجب أن يُظهر `stty size` الحجم الحقيقي. |
| يظهر «1» دون أن يطلبه أحد | النص المعروض يطابق نمطاً (مثلاً برنامج يعرض قائمة تأكيد مقتبسة، أو شفرة نمط بحد ذاته). ضيّقوا النمط، أو شغّلوا هذا البرنامج خارج auto-yes (`AUTO_YES_ACTIVE=1 bash`). |
| لا يُجاب على شيء | تحققوا من النمط بـ `AUTO_YES_PATTERNS`؛ قائمة مرسومة بتسلسلات المؤشر (دون فواصل أسطر حقيقية) لا تطابق `\n`. |
| تُفتح الطرفية في الجذر بدلاً من المجلد الحالي | طريقة «ملف تعريف GNOME Terminal»: انتقلوا إلى طريقة `~/.bashrc`. |
| التعطيل لجلسة واحدة | `AUTO_YES_ACTIVE=1 bash` يفتح صدفة دون auto-yes. |

<a id="depot"></a>

## تنظيم المستودع

| المسار | المحتوى |
|---|---|
| `bin/auto-yes`، `bin/auto-yes-shell` | سكربتات Expect |
| `bin/auto-yes-configurer-gnome-terminal` | الربط بملف تعريف GNOME Terminal |
| `etc/patterns.conf` | الأنماط المرفقة (`/etc/auto-yes/patterns.conf`، ملف إعداد يُحفظ عبر التحديثات) |
| `packaging/` | `build-deb.sh`، `control`، `changelog`، `copyright`، سكربتات الحزمة |
| `tests/test_auto_yes.py` | اختبارات في طرفية زائفة: تغيير الحجم، قائمة معروفة، تجاهل جملة معزولة |
| `docs/readme/` | هذا الملف بـ 18 لغة أخرى |

<a id="deb"></a>

## بناء الحزمة

```bash
python3 -m unittest discover -s tests -v   # اختبارات (يتطلب expect)
packaging/build-deb.sh                     # → dist/auto-yes_<إصدار>_all.deb
```

يأتي الإصدار من السطر الأول في `packaging/changelog`.

<a id="licence"></a>

## الرخصة

[MIT](../../LICENSE).

<a id="soutien"></a>

## دعم المشروع

إذا كان هذا المشروع مفيداً لكم، فإن فنجان قهوة يساعد في صيانته:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=قدّم%20لي%20قهوة&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

تقارير الأخطاء والأفكار: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). الثغرات الأمنية: [SECURITY.md](../../SECURITY.md).
