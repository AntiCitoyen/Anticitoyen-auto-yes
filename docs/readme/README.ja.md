<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — 確認プロンプトに自動で「1」と答える

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![ライセンス MIT](https://img.shields.io/badge/ライセンス-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-応援する-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

Linux のターミナルで、**auto-yes** はプログラムが表示する内容を監視し、認識された確認メニュー（デフォルトでは「Do you want to proceed?」に続く「1. Yes」）が現れるとすぐに、あなたの代わりに **1** を入力して Enter を押します。ターミナルは完全にインタラクティブなまま維持されます：入力、Ctrl-C、リサイズ、色。

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · **🇯🇵 日本語** · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="動作中の auto-yes" width="760"><br><em>メニューが現れ、auto-yes が「1」と答え、コマンドが続行される。</em></p>

> ⚠️ **理解したうえで使用してください。** auto-yes は、設定されたパターンに一致する**あらゆる**要求を確認してしまいます。これには、破壊的なコマンド（パッケージの削除、ディスクツール）や、同意を求める他のプログラムからの要求も含まれます。パターンは狭く保ってください。

---

## 目次

- [プロジェクトの機能](#projet)
- [インストール](#installation)
- [使い方](#utilisation)
- [パターン](#motifs)
- [仕組み](#fonctionnement)
- [トラブルシューティング](#depannage)
- [リポジトリの構成](#depot)
- [パッケージの構築](#deb)
- [ライセンス](#licence)
- [プロジェクトを応援する](#soutien)

---

<a id="projet"></a>

## プロジェクトの機能

| コマンド | 役割 |
|---|---|
| `auto-yes <コマンド> [引数…]` | **1つの**コマンドを起動し、その確認プロンプトに答える |
| `auto-yes-shell` | ログインシェルを置き換える：このターミナルで入力された**すべての**コマンドが、接頭辞なしでその恩恵を受ける |
| `auto-yes-configurer-gnome-terminal` | `auto-yes-shell` を GNOME Terminal のデフォルトプロファイルに接続する（元に戻すには `--revert`） |
| `auto-yes --pause` / `--reprise` | すでに開いているものも含め、**すべての**ターミナルで自動応答を一時停止／再開する |
| `auto-yes --etat` / `--journal [N]` | 現在の状態；記録された直近 N 件の応答 |

- **ターミナルはそのまま**：Expect の `spawn` + `interact`；入力した内容はすべてそのまま通過し、パターンだけが送信の引き金になる。
- **画面の静止**：メニューの後 300ms の間何も表示されなければ応答が送信される；スクロールするテキストの中に引用された質問は無視される。
- **ログ**：認識された各パターンは、日付、応答またはその見送りの理由、前面のプログラム、テキストとともに `~/.local/state/auto-yes/journal.log` に記録される。
- **リサイズが中継される**：ウィンドウのサイズが変わると、シェルとプログラムがそれを認識する（履歴の編集、`less`、`vim`、`htop` は正しく表示され続ける）。
- **再インストール不要でパターンを変更可能**：`/etc/auto-yes/patterns.conf`、新しいターミナルを開くたびに再読み込みされる。
- **二重ラップなし**：すでに auto-yes 下で動作しているターミナルが別のターミナルを再起動しても、二重にラップされない（`AUTO_YES_ACTIVE`）。

<a id="installation"></a>

## インストール

### Debian / Ubuntu パッケージ

[最新のリリース](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)から `.deb` をダウンロードし、次を実行します。

```bash
sudo apt install ./auto-yes_*_all.deb
```

依存関係：`expect`（≥ 5.45）と `procps`。

### Fedora、openSUSE…（RPM）と Arch Linux

同じリリースには `auto-yes-<version>-1.noarch.rpm`（`sudo dnf install ./auto-yes-*.noarch.rpm`）、`.src.rpm`、Arch パッケージ（`sudo pacman -U auto-yes-*.pkg.tar.zst`）、および AUR ファイル（`aur-<version>.tar.gz`：`PKGBUILD` と `.SRCINFO`）が含まれています。

### ソースから

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## 使い方

### 単一のコマンド

```bash
auto-yes apt install パッケージ
auto-yes ./対話式スクリプト.sh --オプション
```

### ターミナル全体

**推奨方法 — `~/.bashrc`**（開始フォルダを保持する。例えばファイルマネージャーの*ターミナルで開く*を使う場合）；ファイルの末尾に追加します。

```bash
# インタラクティブなすべてのターミナルで auto-yes を有効化（二重ラップなし、非インタラクティブシェルは除外）
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**別の方法 — GNOME Terminal プロファイル**（自分自身として実行し、`sudo` では絶対に実行しない）：

```bash
auto-yes-configurer-gnome-terminal           # 新しいウィンドウとタブ → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # 元に戻す
```

この方法は、すでに開いているターミナル、`gnome-terminal -- <コマンド>`、他のエミュレーターのいずれにも影響しません。

<a id="motifs"></a>

## パターン

`/etc/auto-yes/patterns.conf`：1行につき1つの Tcl 正規表現（`interact -re`）；空行と `#` で始まる行は無視されます。付属のパターン：

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

これは質問文**と**、次の行にある番号付きメニューの選択肢 `1.` を要求します。文だけ（`cat`、`echo`、ログによって表示されるもの）では何も引き起こしません。

| ルール | 理由 |
|---|---|
| 孤立した文ではなく、メニュー全体を対象にする | その文を引用しているテキストが応答を引き起こしてはならない |
| 境界には `\s` または `\y` を使い、`\b` は絶対に使わない | Tcl では `\b` はバックスペースであり、単語境界ではない |
| 大文字小文字を無視するために先頭に `(?i)` を付ける | プログラムによって「Proceed」/「proceed」の表記が異なる |
| `AUTO_YES_PATTERNS=ファイル auto-yes …` でテストする | この変数は、試験のために `/etc/auto-yes/patterns.conf` を置き換える |

### 環境変数

| 変数 | 役割 | 既定値 |
|---|---|---|
| `AUTO_YES_PATTERNS` | パターンファイル | `/etc/auto-yes/patterns.conf` |
| `AUTO_YES_CALME` | メニューの後に必要な静止時間（ミリ秒、`0`：即座に応答） | `300` |
| `AUTO_YES_JOURNAL` | ログファイル（空：何も記録されない） | `~/.local/state/auto-yes/journal.log` |
| `AUTO_YES_ETAT` | 状態フォルダ（一時停止フラグ） | `~/.local/state/auto-yes` |

完全なヘルプ：`man auto-yes`。

<a id="fonctionnement"></a>

## 仕組み

1. `auto-yes-shell` がパターンを読み込み、`AUTO_YES_ACTIVE=1` を設定し、疑似端末（`spawn -noecho`）内で `$SHELL -l` を起動する。
2. `interact -o -nobuffer -re <パターン>` が、あなたのターミナルとシェルの間のすべてをコピーする；プログラムの出力がパターンに一致すると、auto-yes は一時停止が有効でないこと、そして画面が `AUTO_YES_CALME` ミリ秒間静止していたことを確認したうえで `1` と Enter を送信し、その一部始終をログに記録する。
3. `trap … WINCH` がウィンドウサイズ（`stty rows/columns`）をシェルの疑似端末にコピーし、`SIGWINCH` を送信する。

<a id="depannage"></a>

## トラブルシューティング

| 症状 | 原因と対処法 |
|---|---|
| ↑/↓ で呼び出したコマンドを編集すると、行がずれたり消えたりする | バージョン 1.1 以下：ウィンドウサイズが中継されておらず、bash が 80 列のままだった。1.2 で修正済み；更新後に新しいターミナルを開いてください。`stty size` が実際のサイズを表示するはずです。 |
| 誰も要求していないのに「1」が現れる | 表示されたテキストがパターンに一致し、その後画面が静止した場合に送信される（バージョン 1.2 以下：待機なし）。`auto-yes --journal` でどのプログラムとテキストかを確認できる；パターンを狭める、`AUTO_YES_CALME` を増やす、またはその操作の間だけ `auto-yes --pause` してください。 |
| 何も応答されない | `AUTO_YES_PATTERNS` でパターンを確認してください；カーソルシーケンスで描画されたメニュー（実際の改行がないもの）は `\n` に一致しません。 |
| 現在のフォルダではなくルートでターミナルが開く | 「GNOME Terminal プロファイル」方式：`~/.bashrc` 方式に切り替えてください。 |
| 実際のメニューが認識されているのに確認されない | プログラムが表示を続けている（アニメーション、時計）：ログには `ignoré:défilement` と記録される。`AUTO_YES_CALME` を下げるか、そのプログラムについては `0` に設定してください。 |
| どこでもしばらく無効にする | `auto-yes --pause`（その後 `--reprise`）；または auto-yes なしのシェルには `AUTO_YES_ACTIVE=1 bash`。 |

<a id="depot"></a>

## リポジトリの構成

| パス | 内容 |
|---|---|
| `bin/auto-yes`、`bin/auto-yes-shell` | Expect スクリプト |
| `bin/auto-yes-configurer-gnome-terminal` | GNOME Terminal プロファイルへの接続 |
| `share/auto-yes/commun.tcl` | 共通コード：パターン、画面の静止、ログ、一時停止、ウィンドウサイズ |
| `man/` | `auto-yes(1)` のマニュアルページ |
| `etc/patterns.conf` | 付属のパターン（`/etc/auto-yes/patterns.conf`、更新時にも保持される設定ファイル） |
| `packaging/` | `install.sh`（共通）、`build-deb.sh`、`control`、`changelog`、`copyright`、パッケージスクリプト；`rpm/auto-yes.spec`、`aur/PKGBUILD` |
| `tests/test_auto_yes.py` | 疑似端末でのテスト：リサイズ、メニューの認識、孤立した文とスクロールするテキストの無視、ログ、一時停止 |
| `docs/readme/` | この README の他18言語版 |

<a id="deb"></a>

## パッケージの構築

```bash
python3 -m unittest discover -s tests -v   # テスト（expect が必要）
packaging/build-deb.sh                     # → dist/auto-yes_<バージョン>_all.deb
```

バージョンは `packaging/changelog` の最初の行から取得されます。各リリースが公開されるたびに、`.github/workflows/release.yml` が RPM、Arch パッケージ、AUR ファイルをビルドして添付します。

<a id="licence"></a>

## ライセンス

[MIT](../../LICENSE)。

<a id="soutien"></a>

## プロジェクトを応援する

このプロジェクトがお役に立ったなら、コーヒー1杯が維持の助けになります。

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=コーヒーをおごる&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

バグ報告とアイデア：[Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues)。セキュリティ上の脆弱性：[SECURITY.md](../../SECURITY.md)。
