<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — menjawab «1» secara otomatis untuk permintaan konfirmasi

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![Lisensi MIT](https://img.shields.io/badge/lisensi-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-dukung-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

Di terminal Linux, **auto-yes** mengamati apa yang ditampilkan program dan, segera setelah menu konfirmasi yang dikenali muncul (secara default «Do you want to proceed?» diikuti «1. Yes»), ia mengetik **1** lalu Enter untuk Anda. Terminal tetap sepenuhnya interaktif: pengetikan, Ctrl-C, pengubahan ukuran, warna.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · **🇮🇩 Bahasa Indonesia**

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes sedang beraksi" width="760"><br><em>Menu muncul, auto-yes menjawab «1», perintah berlanjut.</em></p>

> ⚠️ **Gunakan dengan penuh kesadaran.** auto-yes mengonfirmasi **permintaan apa pun** yang cocok dengan pola yang dikonfigurasi, termasuk permintaan dari perintah yang bersifat merusak (menghapus paket, alat disk) atau program lain yang meminta persetujuan Anda. Jagalah agar pola tetap sempit.

---

## Daftar Isi

- [Apa yang dilakukan proyek ini](#projet)
- [Instalasi](#installation)
- [Penggunaan](#utilisation)
- [Pola](#motifs)
- [Cara kerjanya](#fonctionnement)
- [Pemecahan masalah](#depannage)
- [Struktur repositori](#depot)
- [Membangun paket](#deb)
- [Lisensi](#licence)
- [Dukung proyek ini](#soutien)

---

<a id="projet"></a>

## Apa yang dilakukan proyek ini

| Perintah | Peran |
|---|---|
| `auto-yes <perintah> [argumen…]` | menjalankan **satu** perintah dan menjawab permintaan konfirmasinya |
| `auto-yes-shell` | menggantikan shell login: **semua** perintah yang diketik di terminal ini mendapatkan manfaat, tanpa awalan |
| `auto-yes-configurer-gnome-terminal` | menghubungkan `auto-yes-shell` ke profil GNOME Terminal bawaan (`--revert` untuk kembali) |

- **Terminal tetap utuh**: `spawn` + `interact` dari Expect; semua yang Anda ketik diteruskan, hanya pola yang memicu pengiriman.
- **Pengubahan ukuran diteruskan**: saat jendela berubah ukuran, shell dan program mengetahuinya (pengeditan riwayat, `less`, `vim`, `htop` tetap akurat).
- **Pola dapat diubah tanpa instal ulang**: `/etc/auto-yes/patterns.conf`, dibaca ulang setiap kali terminal baru dibuka.
- **Tidak ada pembungkusan ganda**: terminal yang sudah berjalan di bawah auto-yes dan menjalankan terminal lain tidak akan membungkus dirinya dua kali (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Instalasi

### Paket Debian / Ubuntu

Unduh `.deb` dari [rilis terbaru](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest), lalu:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Satu-satunya dependensi: `expect` (≥ 5.45).

### Dari sumber

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Penggunaan

### Satu perintah

```bash
auto-yes apt install paket
auto-yes ./skrip-interaktif.sh --opsi
```

### Seluruh terminal

**Metode yang disarankan — `~/.bashrc`** (mempertahankan folder awal, misalnya dengan *Buka di Terminal* dari pengelola berkas); letakkan di akhir berkas:

```bash
# auto-yes di setiap terminal interaktif (tanpa pembungkusan ganda, shell non-interaktif dikecualikan)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Metode lain — profil GNOME Terminal** (jalankan sebagai diri Anda sendiri, jangan pernah dengan `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # jendela dan tab baru → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # kembalikan
```

Metode ini tidak memengaruhi terminal yang sudah terbuka, `gnome-terminal -- <perintah>`, maupun emulator lainnya.

<a id="motifs"></a>

## Pola

`/etc/auto-yes/patterns.conf`: satu ekspresi reguler Tcl (`interact -re`) per baris; baris kosong dan yang diawali `#` diabaikan. Pola bawaan:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Pola ini membutuhkan pertanyaan **dan**, pada baris berikutnya, pilihan `1.` dari menu bernomor: kalimat itu sendiri (ditampilkan oleh `cat`, `echo`, sebuah log) tidak memicu apa pun.

| Aturan | Alasan |
|---|---|
| Menargetkan menu lengkap, bukan kalimat yang berdiri sendiri | teks yang mengutip kalimat tersebut tidak boleh memicu respons |
| Gunakan `\s` atau `\y` untuk batas, jangan pernah `\b` | di Tcl, `\b` adalah backspace, bukan batas kata |
| `(?i)` di awal untuk mengabaikan huruf besar/kecil | program bervariasi antara «Proceed» / «proceed» |
| Uji dengan `AUTO_YES_PATTERNS=berkas auto-yes …` | variabel ini menggantikan `/etc/auto-yes/patterns.conf` untuk sebuah percobaan |

<a id="fonctionnement"></a>

## Cara kerjanya

1. `auto-yes-shell` membaca pola, menetapkan `AUTO_YES_ACTIVE=1`, lalu menjalankan `$SHELL -l` dalam pseudo-terminal (`spawn -noecho`).
2. `interact -o -nobuffer -re <pola> { send "1\r" }` menyalin semua yang terjadi antara terminal Anda dan shell; ketika keluaran program cocok dengan sebuah pola, Expect mengirimkan `1` dan Enter.
3. `trap … WINCH` menyalin ukuran jendela (`stty rows/columns`) ke pseudo-terminal shell dan mengirimkan `SIGWINCH` kepadanya.

<a id="depannage"></a>

## Pemecahan masalah

| Gejala | Penyebab dan solusi |
|---|---|
| Saat mengedit perintah yang dipanggil kembali dengan ↑/↓, baris bergeser atau menghilang | versi ≤ 1.1: ukuran jendela tidak diteruskan, bash tetap pada 80 kolom. Diperbaiki di 1.2; buka terminal baru setelah pembaruan. `stty size` seharusnya menampilkan ukuran sebenarnya. |
| Sebuah «1» muncul padahal tidak ada yang memintanya | teks yang ditampilkan cocok dengan sebuah pola (misalnya program yang menampilkan menu konfirmasi yang dikutip, atau kode dari pola itu sendiri). Persempit polanya, atau jalankan program tersebut di luar auto-yes (`AUTO_YES_ACTIVE=1 bash`). |
| Tidak ada yang dijawab | periksa pola dengan `AUTO_YES_PATTERNS`; menu yang digambar dengan urutan kursor (tanpa jeda baris sungguhan) tidak cocok dengan `\n`. |
| Terminal terbuka di direktori root, bukan folder saat ini | metode «profil GNOME Terminal»: beralihlah ke metode `~/.bashrc`. |
| Menonaktifkan untuk satu sesi | `AUTO_YES_ACTIVE=1 bash` membuka shell tanpa auto-yes. |

<a id="depot"></a>

## Struktur repositori

| Jalur | Isi |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | skrip Expect |
| `bin/auto-yes-configurer-gnome-terminal` | penghubung ke profil GNOME Terminal |
| `etc/patterns.conf` | pola bawaan (`/etc/auto-yes/patterns.conf`, berkas konfigurasi tetap dipertahankan saat pembaruan) |
| `packaging/` | `build-deb.sh`, `control`, `changelog`, `copyright`, skrip paket |
| `tests/test_auto_yes.py` | pengujian dalam pseudo-terminal: pengubahan ukuran, menu yang dikenali, kalimat berdiri sendiri diabaikan |
| `docs/readme/` | README ini dalam 18 bahasa lainnya |

<a id="deb"></a>

## Membangun paket

```bash
python3 -m unittest discover -s tests -v   # pengujian (memerlukan expect)
packaging/build-deb.sh                     # → dist/auto-yes_<versi>_all.deb
```

Versi diambil dari baris pertama `packaging/changelog`.

<a id="licence"></a>

## Lisensi

[MIT](../../LICENSE).

<a id="soutien"></a>

## Dukung proyek ini

Jika proyek ini berguna bagi Anda, secangkir kopi membantu memeliharanya:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Traktir%20saya%20kopi&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Laporan bug dan ide: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Kerentanan keamanan: [SECURITY.md](../../SECURITY.md).
