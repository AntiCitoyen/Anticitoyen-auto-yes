<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — onay isteklerine kendi kendine «1» yanıtı verir

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![MIT Lisansı](https://img.shields.io/badge/lisans-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-destekle-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

Bir Linux terminalinde **auto-yes**, programların ekrana yazdıklarını izler ve tanınan bir onay menüsü belirir belirmez (varsayılan olarak «Do you want to proceed?» ardından «1. Yes»), sizin yerinize **1** yazıp Enter'a basar. Terminal tamamen etkileşimli kalır: yazma, Ctrl-C, yeniden boyutlandırma, renkler.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · **🇹🇷 Türkçe** · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="eylem hâlinde auto-yes" width="760"><br><em>Menü belirir, auto-yes «1» yanıtını verir, komut devam eder.</em></p>

> ⚠️ **Bilinçli kullanın.** auto-yes, yapılandırılmış bir kalıba uyan **herhangi bir** isteği onaylar; bu, yıkıcı bir komuttan (paket kaldırma, disk araçları) veya onayınızı isteyen başka bir programdan gelen istekleri de kapsar. Kalıpları dar tutun.

---

## İçindekiler

- [Proje ne yapar](#projet)
- [Kurulum](#installation)
- [Kullanım](#utilisation)
- [Kalıplar](#motifs)
- [Nasıl çalışır](#fonctionnement)
- [Sorun giderme](#depannage)
- [Depo düzeni](#depot)
- [Paketi oluşturma](#deb)
- [Lisans](#licence)
- [Projeyi destekle](#soutien)

---

<a id="projet"></a>

## Proje ne yapar

| Komut | Rol |
|---|---|
| `auto-yes <komut> [argümanlar…]` | **tek** bir komut başlatır ve onay isteklerini yanıtlar |
| `auto-yes-shell` | login kabuğunun yerini alır: bu terminalde yazılan **tüm** komutlar önek olmadan bundan yararlanır |
| `auto-yes-configurer-gnome-terminal` | `auto-yes-shell`'i varsayılan GNOME Terminal profiline bağlar (geri almak için `--revert`) |
| `auto-yes --pause` / `--reprise` | **tüm** terminallerde, hatta zaten açık olanlarda bile yanıtlamayı askıya alır / geri getirir |
| `auto-yes --etat` / `--journal [N]` | mevcut durum; kaydedilen son N yanıt |

- **Terminal olduğu gibi kalır**: Expect'in `spawn` + `interact`'i; yazdığınız her şey geçer, yalnızca kalıp bir gönderimi tetikler.
- **Sessiz ekran**: yanıt yalnızca menüden 300 ms sonra hiçbir şey görüntülenmiyorsa gönderilir; kayan bir metin içinde alıntılanan bir soru yok sayılır.
- **Günlük**: tanınan her kalıp (tarih, yanıt veya çekimser kalma nedeni, ön plandaki program, metin) `~/.local/state/auto-yes/journal.log` dosyasına kaydedilir.
- **Yeniden boyutlandırma iletilir**: pencere boyutu değiştiğinde kabuk ve programlar bunu bilir (geçmiş düzenleme, `less`, `vim`, `htop` doğru kalır).
- **Yeniden kurmadan değiştirilebilir kalıplar**: `/etc/auto-yes/patterns.conf`, her yeni terminalde yeniden okunur.
- **Çift sarmalama yok**: zaten auto-yes altında çalışan bir terminal başka bir tane başlattığında kendini iki kez sarmalamaz (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Kurulum

### Debian / Ubuntu paketi

`.deb` dosyasını [son sürümden](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest) indirin, ardından:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Bağımlılıklar: `expect` (≥ 5.45) ve `procps`.

### Fedora, openSUSE… (RPM) ve Arch Linux

Aynı sürüm, `auto-yes-<sürüm>-1.noarch.rpm` (`sudo dnf install ./auto-yes-*.noarch.rpm`), `.src.rpm`, Arch paketini (`sudo pacman -U auto-yes-*.pkg.tar.zst`) ve AUR dosyalarını (`aur-<sürüm>.tar.gz`: `PKGBUILD` ve `.SRCINFO`) sağlar.

### Kaynak koddan

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Kullanım

### Tek bir komut

```bash
auto-yes apt install paket
auto-yes ./etkilesimli-betik.sh --secenek
```

### Tüm bir terminal

**Önerilen yöntem — `~/.bashrc`** (başlangıç klasörünü korur, örneğin dosya yöneticisinin *Terminalde Aç* özelliğiyle); dosyanın sonuna ekleyin:

```bash
# her etkileşimli terminalde auto-yes (çift sarmalama yok, etkileşimsiz kabuklar hariç)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Başka bir yöntem — GNOME Terminal profili** (kendiniz olarak çalıştırın, asla `sudo` ile değil):

```bash
auto-yes-configurer-gnome-terminal           # yeni pencereler ve sekmeler → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # geri al
```

Bu yöntem ne zaten açık terminallere, ne `gnome-terminal -- <komut>`'a, ne de diğer emülatörlere dokunur.

<a id="motifs"></a>

## Kalıplar

`/etc/auto-yes/patterns.conf`: satır başına bir Tcl düzenli ifadesi (`interact -re`); boş satırlar ve `#` ile başlayanlar yok sayılır. Birlikte gelen kalıp:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Soruyu **ve** bir sonraki satırda numaralandırılmış bir menünün `1.` seçeneğini gerektirir: tek başına cümle (`cat`, `echo`, bir günlük tarafından gösterilen) hiçbir şeyi tetiklemez.

| Kural | Neden |
|---|---|
| İzole bir cümleye değil, menünün tamamına hedeflenmek | cümleyi alıntılayan bir metin bir yanıtı tetiklememelidir |
| Sınırlar için `\s` veya `\y`, asla `\b` değil | Tcl'de `\b` bir geri silme tuşudur, sözcük sınırı değildir |
| Büyük/küçük harfi yok saymak için başa `(?i)` | programlar «Proceed» / «proceed» arasında değişir |
| `AUTO_YES_PATTERNS=dosya auto-yes …` ile test edin | değişken, bir deneme için `/etc/auto-yes/patterns.conf`'un yerini alır |

### Ortam değişkenleri

| Variable | Rol | Varsayılan |
|---|---|---|
| `AUTO_YES_PATTERNS` | kalıp dosyası | `/etc/auto-yes/patterns.conf` |
| `AUTO_YES_CALME` | menüden sonra gereken sessizlik süresi, milisaniye cinsinden (`0`: anında yanıt) | `300` |
| `AUTO_YES_JOURNAL` | günlük dosyası (boş: hiçbir şey kaydedilmez) | `~/.local/state/auto-yes/journal.log` |
| `AUTO_YES_ETAT` | durum klasörü (duraklatma bayrağı) | `~/.local/state/auto-yes` |

Tam yardım: `man auto-yes`.

<a id="fonctionnement"></a>

## Nasıl çalışır

1. `auto-yes-shell` kalıpları okur, `AUTO_YES_ACTIVE=1` ayarlar, ardından bir sözde uçbirimde (`spawn -noecho`) `$SHELL -l`'i başlatır.
2. `interact -o -nobuffer -re <kalıp>`, terminaliniz ile kabuk arasındaki her şeyi kopyalar; programın çıktısı bir kalıpla eşleştiğinde auto-yes duraklatmanın etkin olmadığını ve ekranın `AUTO_YES_CALME` ms boyunca sessiz kaldığını doğrular, ardından `1` ve Enter gönderir ve her şeyi günlüğe kaydeder.
3. Bir `trap … WINCH`, pencere boyutunu (`stty rows/columns`) kabuğun sözde uçbirimine kopyalar ve ona `SIGWINCH` gönderir.

<a id="depannage"></a>

## Sorun giderme

| Belirti | Neden ve çözüm |
|---|---|
| ↑/↓ ile çağrılan bir komutu düzenlerken satır kayıyor veya kayboluyor | sürüm ≤ 1.1: pencere boyutu iletilmiyordu, bash 80 sütunda kalıyordu. 1.2'de düzeltildi; güncellemeden sonra yeni bir terminal açın. `stty size` gerçek boyutu göstermelidir. |
| Kimse istemediği hâlde bir «1» beliriyor | görüntülenen metin bir kalıpla eşleşiyor ve ekran bundan sonra sessiz kaldı (sürüm ≤ 1.2: hiç bekleme yoktu). `auto-yes --journal`, hangi programın ve hangi metnin olduğunu gösterir; kalıbı daraltın, `AUTO_YES_CALME`'yi artırın veya işlem süresince `auto-yes --pause` kullanın. |
| Hiçbir şey yanıtlanmıyor | kalıbı `AUTO_YES_PATTERNS` ile kontrol edin; imleç dizileriyle çizilen bir menü (gerçek satır sonları olmadan) `\n` ile eşleşmez. |
| Terminal mevcut klasör yerine kökte açılıyor | «GNOME Terminal profili» yöntemi: `~/.bashrc` yöntemine geçin. |
| Tanınmasına rağmen gerçek bir menü onaylanmıyor | program görüntülemeye devam ediyor (animasyon, saat): günlük `ignoré:défilement` gösterir. `AUTO_YES_CALME`'yi düşürün veya bu program için `0` yapın. |
| Her yerde bir süreliğine devre dışı bırakma | `auto-yes --pause` (ardından `--reprise`); veya auto-yes olmayan bir kabuk için `AUTO_YES_ACTIVE=1 bash`. |

<a id="depot"></a>

## Depo düzeni

| Yol | İçerik |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | Expect betikleri |
| `bin/auto-yes-configurer-gnome-terminal` | GNOME Terminal profiline bağlama |
| `share/auto-yes/commun.tcl` | ortak kod: kalıplar, sessiz ekran, günlük, duraklatma, pencere boyutu |
| `man/` | `auto-yes(1)` kılavuz sayfası |
| `etc/patterns.conf` | birlikte gelen kalıplar (`/etc/auto-yes/patterns.conf`, güncellemelerde korunan yapılandırma dosyası) |
| `packaging/` | `install.sh` (ortak), `build-deb.sh`, `control`, `changelog`, `copyright`, paket betikleri; `rpm/auto-yes.spec`, `aur/PKGBUILD` |
| `tests/test_auto_yes.py` | sözde uçbirim testleri: yeniden boyutlandırma, tanınan menü, tek başına cümle ve kayan metin yok sayılır, günlük, duraklatma |
| `docs/readme/` | bu README'nin diğer 18 dildeki hâli |

<a id="deb"></a>

## Paketi oluşturma

```bash
python3 -m unittest discover -s tests -v   # testler (expect gerekir)
packaging/build-deb.sh                     # → dist/auto-yes_<sürüm>_all.deb
```

Sürüm, `packaging/changelog`'un ilk satırından gelir. Yayımlanan her sürümde `.github/workflows/release.yml`, RPM, Arch paketlerini ve AUR dosyalarını oluşturup ekler.

<a id="licence"></a>

## Lisans

[MIT](../../LICENSE).

<a id="soutien"></a>

## Projeyi destekle

Bu proje işinize yarıyorsa bir kahve, onu sürdürmeye yardımcı olur:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Bana%20bir%20kahve%20ısmarla&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Hata bildirimleri ve fikirler: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Güvenlik açıkları: [SECURITY.md](../../SECURITY.md).
