<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — tự động trả lời «1» cho các yêu cầu xác nhận

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![Giấy phép MIT](https://img.shields.io/badge/giấy%20phép-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ủng%20hộ-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

Trong một terminal Linux, **auto-yes** theo dõi những gì các chương trình hiển thị và, ngay khi xuất hiện một menu xác nhận được nhận diện (mặc định là «Do you want to proceed?» tiếp theo là «1. Yes»), nó gõ **1** rồi Enter thay cho bạn. Terminal vẫn giữ được tính tương tác hoàn toàn: gõ phím, Ctrl-C, thay đổi kích thước, màu sắc.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · **🇻🇳 Tiếng Việt** · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes đang hoạt động" width="760"><br><em>Menu xuất hiện, auto-yes trả lời «1», lệnh tiếp tục chạy.</em></p>

> ⚠️ **Hãy sử dụng có hiểu biết.** auto-yes xác nhận **bất kỳ** yêu cầu nào khớp với một mẫu đã cấu hình, kể cả yêu cầu từ một lệnh mang tính phá hủy (gỡ bỏ gói, công cụ ổ đĩa) hoặc từ một chương trình khác đang xin sự đồng ý của bạn. Hãy giữ các mẫu thật hẹp.

---

## Mục lục

- [Dự án làm gì](#projet)
- [Cài đặt](#installation)
- [Sử dụng](#utilisation)
- [Các mẫu](#motifs)
- [Cách hoạt động](#fonctionnement)
- [Khắc phục sự cố](#depannage)
- [Cấu trúc kho lưu trữ](#depot)
- [Xây dựng gói](#deb)
- [Giấy phép](#licence)
- [Ủng hộ dự án](#soutien)

---

<a id="projet"></a>

## Dự án làm gì

| Lệnh | Vai trò |
|---|---|
| `auto-yes <lệnh> [tham số…]` | khởi chạy **một** lệnh và trả lời các yêu cầu xác nhận của nó |
| `auto-yes-shell` | thay thế shell đăng nhập: **tất cả** các lệnh được gõ trong terminal này đều được hưởng lợi, không cần tiền tố |
| `auto-yes-configurer-gnome-terminal` | kết nối `auto-yes-shell` với hồ sơ mặc định của GNOME Terminal (`--revert` để hoàn tác) |

- **Terminal được giữ nguyên**: `spawn` + `interact` của Expect; mọi thứ bạn gõ đều được truyền qua, chỉ có mẫu mới kích hoạt việc gửi.
- **Việc thay đổi kích thước được chuyển tiếp**: khi cửa sổ đổi kích thước, shell và các chương trình đều biết điều đó (chỉnh sửa lịch sử, `less`, `vim`, `htop` vẫn chính xác).
- **Các mẫu có thể sửa mà không cần cài lại**: `/etc/auto-yes/patterns.conf`, được đọc lại mỗi khi mở terminal mới.
- **Không bọc kép**: một terminal đã chạy dưới auto-yes mà khởi động một terminal khác sẽ không tự bọc mình hai lần (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Cài đặt

### Gói Debian / Ubuntu

Tải tệp `.deb` từ [bản phát hành mới nhất](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest), sau đó:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Phụ thuộc duy nhất: `expect` (≥ 5.45).

### Từ mã nguồn

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Sử dụng

### Một lệnh duy nhất

```bash
auto-yes apt install gói
auto-yes ./script-tuong-tac.sh --tuy-chon
```

### Toàn bộ một terminal

**Phương pháp khuyến nghị — `~/.bashrc`** (giữ nguyên thư mục xuất phát, ví dụ khi dùng *Mở trong terminal* của trình quản lý tệp); đặt ở cuối tệp:

```bash
# auto-yes trong mọi terminal tương tác (không bọc kép, loại trừ các shell không tương tác)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Phương pháp khác — hồ sơ GNOME Terminal** (chạy với tư cách chính bạn, không bao giờ dùng `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # cửa sổ và thẻ mới → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # hoàn tác
```

Phương pháp này không ảnh hưởng đến các terminal đã mở sẵn, cũng không ảnh hưởng đến `gnome-terminal -- <lệnh>`, cũng như các trình giả lập khác.

<a id="motifs"></a>

## Các mẫu

`/etc/auto-yes/patterns.conf`: mỗi dòng một biểu thức chính quy Tcl (`interact -re`); các dòng trống và dòng bắt đầu bằng `#` sẽ bị bỏ qua. Mẫu đi kèm:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Nó đòi hỏi câu hỏi **và**, ở dòng tiếp theo, lựa chọn `1.` của một menu được đánh số: chỉ riêng câu văn (được hiển thị bởi `cat`, `echo`, một nhật ký) sẽ không kích hoạt gì cả.

| Quy tắc | Vì sao |
|---|---|
| Nhắm vào toàn bộ menu, không phải một câu bị cô lập | một văn bản trích dẫn câu đó không được kích hoạt phản hồi |
| Dùng `\s` hoặc `\y` cho ranh giới, không bao giờ dùng `\b` | trong Tcl, `\b` là phím lùi, không phải ranh giới từ |
| Đặt `(?i)` ở đầu để bỏ qua chữ hoa/thường | các chương trình dùng khác nhau «Proceed» / «proceed» |
| Kiểm thử với `AUTO_YES_PATTERNS=tệp auto-yes …` | biến này thay thế `/etc/auto-yes/patterns.conf` để thử nghiệm |

<a id="fonctionnement"></a>

## Cách hoạt động

1. `auto-yes-shell` đọc các mẫu, đặt `AUTO_YES_ACTIVE=1`, sau đó khởi chạy `$SHELL -l` trong một pseudo-terminal (`spawn -noecho`).
2. `interact -o -nobuffer -re <mẫu> { send "1\r" }` sao chép mọi thứ giữa terminal của bạn và shell; khi đầu ra của chương trình khớp với một mẫu, Expect gửi `1` và Enter.
3. Một `trap … WINCH` sao chép kích thước cửa sổ (`stty rows/columns`) sang pseudo-terminal của shell và gửi cho nó `SIGWINCH`.

<a id="depannage"></a>

## Khắc phục sự cố

| Triệu chứng | Nguyên nhân và cách khắc phục |
|---|---|
| Khi chỉnh sửa một lệnh được gọi lại bằng ↑/↓, dòng bị lệch hoặc biến mất | các phiên bản ≤ 1.1: kích thước cửa sổ không được chuyển tiếp, bash vẫn ở mức 80 cột. Đã sửa trong 1.2; hãy mở một terminal mới sau khi cập nhật. `stty size` phải hiển thị kích thước thực. |
| Xuất hiện một «1» dù không ai yêu cầu | văn bản hiển thị khớp với một mẫu (ví dụ một chương trình hiển thị một menu xác nhận được trích dẫn, hoặc mã của chính một mẫu). Hãy thu hẹp mẫu, hoặc chạy chương trình đó bên ngoài auto-yes (`AUTO_YES_ACTIVE=1 bash`). |
| Không có gì được trả lời | kiểm tra mẫu bằng `AUTO_YES_PATTERNS`; một menu được vẽ bằng các chuỗi con trỏ (không có ký tự xuống dòng thực sự) sẽ không khớp với `\n`. |
| Terminal mở ở thư mục gốc thay vì thư mục hiện tại | phương pháp «hồ sơ GNOME Terminal»: hãy chuyển sang phương pháp `~/.bashrc`. |
| Vô hiệu hóa cho một phiên | `AUTO_YES_ACTIVE=1 bash` mở một shell không có auto-yes. |

<a id="depot"></a>

## Cấu trúc kho lưu trữ

| Đường dẫn | Nội dung |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | các script Expect |
| `bin/auto-yes-configurer-gnome-terminal` | kết nối với hồ sơ GNOME Terminal |
| `etc/patterns.conf` | các mẫu đi kèm (`/etc/auto-yes/patterns.conf`, tệp cấu hình được giữ nguyên qua các bản cập nhật) |
| `packaging/` | `build-deb.sh`, `control`, `changelog`, `copyright`, các script đóng gói |
| `tests/test_auto_yes.py` | các bài kiểm thử trong pseudo-terminal: thay đổi kích thước, menu được nhận diện, câu bị cô lập bị bỏ qua |
| `docs/readme/` | README này bằng 18 ngôn ngữ khác |

<a id="deb"></a>

## Xây dựng gói

```bash
python3 -m unittest discover -s tests -v   # kiểm thử (cần expect)
packaging/build-deb.sh                     # → dist/auto-yes_<phiên bản>_all.deb
```

Phiên bản được lấy từ dòng đầu tiên của `packaging/changelog`.

<a id="licence"></a>

## Giấy phép

[MIT](../../LICENSE).

<a id="soutien"></a>

## Ủng hộ dự án

Nếu dự án này hữu ích với bạn, một ly cà phê sẽ giúp duy trì nó:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Mời%20tôi%20một%20ly%20cà%20phê&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Báo cáo lỗi và ý tưởng: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Lỗ hổng bảo mật: [SECURITY.md](../../SECURITY.md).
