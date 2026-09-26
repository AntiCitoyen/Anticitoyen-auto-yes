<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — पुष्टिकरण अनुरोधों का अपने आप «1» उत्तर देना

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![लाइसेंस MIT](https://img.shields.io/badge/लाइसेंस-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-समर्थन-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

Linux टर्मिनल में, **auto-yes** यह देखता रहता है कि प्रोग्राम क्या दिखा रहे हैं, और जैसे ही कोई पहचाना गया पुष्टिकरण मेनू आता है (डिफ़ॉल्ट रूप से «Do you want to proceed?» उसके बाद «1. Yes»), आपकी जगह **1** और फिर एंटर टाइप कर देता है। टर्मिनल पूरी तरह इंटरैक्टिव बना रहता है: टाइपिंग, Ctrl-C, आकार बदलना, रंग।

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · **🇮🇳 हिन्दी** · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="क्रियान्वयन में auto-yes" width="760"><br><em>मेनू आता है, auto-yes «1» का जवाब देता है, कमांड जारी रहता है।</em></p>

> ⚠️ **जानकारी के साथ उपयोग करें।** auto-yes किसी भी कॉन्फ़िगर किए गए पैटर्न से मेल खाने वाले **किसी भी** अनुरोध की पुष्टि करता है, जिसमें किसी विनाशकारी कमांड (पैकेज हटाना, डिस्क टूल) या आपकी सहमति माँगने वाले किसी अन्य प्रोग्राम का अनुरोध भी शामिल है। पैटर्न को संकीर्ण रखें।

---

## विषय-सूची

- [परियोजना क्या करती है](#projet)
- [इंस्टॉलेशन](#installation)
- [उपयोग](#utilisation)
- [पैटर्न](#motifs)
- [यह कैसे काम करता है](#fonctionnement)
- [समस्या निवारण](#depannage)
- [रिपॉज़िटरी संरचना](#depot)
- [पैकेज बनाना](#deb)
- [लाइसेंस](#licence)
- [परियोजना का समर्थन करें](#soutien)

---

<a id="projet"></a>

## परियोजना क्या करती है

| कमांड | भूमिका |
|---|---|
| `auto-yes <कमांड> [तर्क…]` | **एक** कमांड चलाता है और उसके पुष्टिकरण अनुरोधों का उत्तर देता है |
| `auto-yes-shell` | लॉगिन शेल की जगह लेता है: इस टर्मिनल में टाइप किए गए **सभी** कमांड बिना किसी उपसर्ग के इसका लाभ उठाते हैं |
| `auto-yes-configurer-gnome-terminal` | `auto-yes-shell` को डिफ़ॉल्ट GNOME Terminal प्रोफ़ाइल से जोड़ता है (वापस लौटने के लिए `--revert`) |

- **टर्मिनल अक्षुण्ण**: Expect का `spawn` + `interact`; आप जो कुछ भी टाइप करते हैं वह गुज़रता है, केवल पैटर्न ही भेजने को ट्रिगर करता है।
- **आकार परिवर्तन रिले किया गया**: जब विंडो का आकार बदलता है, तो शेल और प्रोग्राम को इसका पता चलता है (इतिहास संपादन, `less`, `vim`, `htop` सही बने रहते हैं)।
- **पुनः इंस्टॉल किए बिना संशोधित करने योग्य पैटर्न**: `/etc/auto-yes/patterns.conf`, हर नए टर्मिनल पर फिर से पढ़ा जाता है।
- **कोई दोहरी रैपिंग नहीं**: पहले से auto-yes के अंतर्गत चल रहा टर्मिनल जो कोई और टर्मिनल शुरू करता है, वह खुद को दो बार नहीं लपेटता (`AUTO_YES_ACTIVE`)।

<a id="installation"></a>

## इंस्टॉलेशन

### Debian / Ubuntu पैकेज

[नवीनतम रिलीज़](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest) से `.deb` डाउनलोड करें, फिर:

```bash
sudo apt install ./auto-yes_*_all.deb
```

केवल निर्भरता: `expect` (≥ 5.45)।

### स्रोत से

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## उपयोग

### एक ही कमांड

```bash
auto-yes apt install पैकेज
auto-yes ./इंटरैक्टिव-स्क्रिप्ट.sh --विकल्प
```

### पूरा एक टर्मिनल

**अनुशंसित तरीका — `~/.bashrc`** (प्रारंभिक फ़ोल्डर बनाए रखता है, उदाहरण के लिए फ़ाइल प्रबंधक के *टर्मिनल में खोलें* के साथ); इसे फ़ाइल के अंत में रखें:

```bash
# हर इंटरैक्टिव टर्मिनल में auto-yes (कोई दोहरी रैपिंग नहीं, गैर-इंटरैक्टिव शेल शामिल नहीं)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**दूसरा तरीका — GNOME Terminal प्रोफ़ाइल** (स्वयं के रूप में चलाएँ, कभी `sudo` के साथ नहीं):

```bash
auto-yes-configurer-gnome-terminal           # नई विंडो और टैब → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # वापस लौटें
```

यह तरीका न तो पहले से खुले टर्मिनलों को, न `gnome-terminal -- <कमांड>` को, और न ही अन्य एमुलेटरों को छूता है।

<a id="motifs"></a>

## पैटर्न

`/etc/auto-yes/patterns.conf`: प्रति पंक्ति एक Tcl रेगुलर एक्सप्रेशन (`interact -re`); खाली पंक्तियाँ और `#` से शुरू होने वाली पंक्तियाँ अनदेखी की जाती हैं। दिया गया पैटर्न:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

इसके लिए प्रश्न **और**, अगली पंक्ति में, क्रमांकित मेनू का विकल्प `1.` आवश्यक है: अकेला वाक्य (`cat`, `echo`, किसी लॉग द्वारा प्रदर्शित) कुछ भी ट्रिगर नहीं करता।

| नियम | क्यों |
|---|---|
| पूरे मेनू को लक्षित करें, किसी अलग वाक्य को नहीं | जो टेक्स्ट वाक्य को उद्धृत करता है उसे उत्तर ट्रिगर नहीं करना चाहिए |
| सीमाओं के लिए `\s` या `\y`, कभी `\b` नहीं | Tcl में, `\b` एक बैकस्पेस है, शब्द सीमा नहीं |
| केस को अनदेखा करने के लिए शुरुआत में `(?i)` | प्रोग्राम «Proceed» / «proceed» के बीच बदलते हैं |
| `AUTO_YES_PATTERNS=फ़ाइल auto-yes …` से परीक्षण करें | यह वेरिएबल परीक्षण के लिए `/etc/auto-yes/patterns.conf` की जगह लेता है |

<a id="fonctionnement"></a>

## यह कैसे काम करता है

1. `auto-yes-shell` पैटर्न पढ़ता है, `AUTO_YES_ACTIVE=1` सेट करता है, फिर एक स्यूडो-टर्मिनल (`spawn -noecho`) में `$SHELL -l` चलाता है।
2. `interact -o -nobuffer -re <पैटर्न> { send "1\r" }` आपके टर्मिनल और शेल के बीच सब कुछ कॉपी करता है; जब प्रोग्राम का आउटपुट किसी पैटर्न से मेल खाता है, तो Expect `1` और एंटर भेजता है।
3. एक `trap … WINCH` विंडो का आकार (`stty rows/columns`) शेल के स्यूडो-टर्मिनल पर कॉपी करता है और उसे `SIGWINCH` भेजता है।

<a id="depannage"></a>

## समस्या निवारण

| लक्षण | कारण और समाधान |
|---|---|
| ↑/↓ से याद की गई किसी कमांड को संपादित करते समय, पंक्ति खिसक जाती है या गायब हो जाती है | संस्करण ≤ 1.1: विंडो का आकार रिले नहीं किया जाता था, bash 80 कॉलम पर बना रहता था। 1.2 में ठीक किया गया; अपडेट के बाद नया टर्मिनल खोलें। `stty size` को वास्तविक आकार दिखाना चाहिए। |
| बिना किसी के पूछे «1» दिखाई देता है | प्रदर्शित टेक्स्ट किसी पैटर्न से मेल खाता है (उदाहरण के लिए कोई प्रोग्राम जो उद्धृत पुष्टिकरण मेनू दिखाता है, या स्वयं किसी पैटर्न का कोड)। पैटर्न को संकीर्ण करें, या उस प्रोग्राम को auto-yes के बाहर चलाएँ (`AUTO_YES_ACTIVE=1 bash`)। |
| कुछ भी उत्तर नहीं दिया जाता | `AUTO_YES_PATTERNS` से पैटर्न जाँचें; कर्सर अनुक्रमों (बिना वास्तविक लाइन ब्रेक के) से बना मेनू `\n` से मेल नहीं खाता। |
| टर्मिनल वर्तमान फ़ोल्डर के बजाय रूट में खुलता है | «GNOME Terminal प्रोफ़ाइल» तरीका: `~/.bashrc` तरीके पर स्विच करें। |
| एक सत्र के लिए निष्क्रिय करना | `AUTO_YES_ACTIVE=1 bash` auto-yes के बिना एक शेल खोलता है। |

<a id="depot"></a>

## रिपॉज़िटरी संरचना

| पथ | सामग्री |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | Expect स्क्रिप्ट |
| `bin/auto-yes-configurer-gnome-terminal` | GNOME Terminal प्रोफ़ाइल से जुड़ाव |
| `etc/patterns.conf` | दिए गए पैटर्न (`/etc/auto-yes/patterns.conf`, कॉन्फ़िगरेशन फ़ाइल अपडेट के दौरान संरक्षित रहती है) |
| `packaging/` | `build-deb.sh`, `control`, `changelog`, `copyright`, पैकेज स्क्रिप्ट |
| `tests/test_auto_yes.py` | स्यूडो-टर्मिनल में परीक्षण: आकार परिवर्तन, पहचाना गया मेनू, अलग वाक्य अनदेखा किया गया |
| `docs/readme/` | यह README 18 अन्य भाषाओं में |

<a id="deb"></a>

## पैकेज बनाना

```bash
python3 -m unittest discover -s tests -v   # परीक्षण (expect आवश्यक)
packaging/build-deb.sh                     # → dist/auto-yes_<संस्करण>_all.deb
```

संस्करण `packaging/changelog` की पहली पंक्ति से आता है।

<a id="licence"></a>

## लाइसेंस

[MIT](../../LICENSE)।

<a id="soutien"></a>

## परियोजना का समर्थन करें

यदि यह परियोजना आपके लिए उपयोगी है, तो एक कॉफ़ी इसे बनाए रखने में मदद करती है:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=मुझे%20एक%20कॉफ़ी%20पिलाएँ&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

बग रिपोर्ट और विचार: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues)। सुरक्षा खामियाँ: [SECURITY.md](../../SECURITY.md)।
