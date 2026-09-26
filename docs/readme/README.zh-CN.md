<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — 自动对确认请求回答「1」

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![MIT 许可证](https://img.shields.io/badge/许可证-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-支持-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

在 Linux 终端中，**auto-yes** 会监视程序显示的内容，一旦出现可识别的确认菜单（默认是「Do you want to proceed?」后接「1. Yes」），就会代替您输入 **1** 然后回车。终端保持完全交互式：打字、Ctrl-C、调整大小、颜色。

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · **🇨🇳 简体中文** · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes 运行中" width="760"><br><em>菜单出现，auto-yes 回答「1」，命令继续执行。</em></p>

> ⚠️ **请在了解风险的情况下使用。** auto-yes 会确认任何符合已配置模式的请求，**不加区分**，包括破坏性命令（删除软件包、磁盘工具）或请求您同意的其他程序。请保持模式的范围狭窄。

---

## 目录

- [项目功能](#projet)
- [安装](#installation)
- [使用方法](#utilisation)
- [模式](#motifs)
- [工作原理](#fonctionnement)
- [故障排查](#depannage)
- [仓库结构](#depot)
- [构建软件包](#deb)
- [许可证](#licence)
- [支持本项目](#soutien)

---

<a id="projet"></a>

## 项目功能

| 命令 | 作用 |
|---|---|
| `auto-yes <命令> [参数…]` | 启动**一个**命令并回答它的确认请求 |
| `auto-yes-shell` | 替换登录 shell：在该终端中输入的**所有**命令都会受益，无需前缀 |
| `auto-yes-configurer-gnome-terminal` | 将 `auto-yes-shell` 挂接到默认的 GNOME Terminal 配置文件上（`--revert` 可还原） |

- **终端保持原样**：使用 Expect 的 `spawn` + `interact`；您输入的一切都会正常传递，只有模式匹配时才会触发发送。
- **窗口大小变化被中继**：当窗口改变大小时，shell 和程序都会知道（历史记录编辑、`less`、`vim`、`htop` 保持正确）。
- **无需重新安装即可修改模式**：`/etc/auto-yes/patterns.conf`，每次打开新终端时重新读取。
- **不会重复包装**：已在 auto-yes 下运行的终端再启动另一个终端时不会被二次包装（`AUTO_YES_ACTIVE`）。

<a id="installation"></a>

## 安装

### Debian / Ubuntu 软件包

从[最新发行版](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)下载 `.deb` 文件，然后：

```bash
sudo apt install ./auto-yes_*_all.deb
```

唯一依赖：`expect`（≥ 5.45）。

### 从源码构建

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## 使用方法

### 单个命令

```bash
auto-yes apt install 软件包
auto-yes ./交互式脚本.sh --选项
```

### 整个终端

**推荐方法 — `~/.bashrc`**（保留起始文件夹，例如通过文件管理器的*在终端中打开*）；添加到文件末尾：

```bash
# 在每个交互式终端中启用 auto-yes（不重复包装，排除非交互式 shell）
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**另一种方法 — GNOME Terminal 配置文件**（以您自己的身份运行，绝不使用 `sudo`）：

```bash
auto-yes-configurer-gnome-terminal           # 新窗口和标签页 → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # 还原
```

此方法既不影响已打开的终端，也不影响 `gnome-terminal -- <命令>`，也不影响其他模拟器。

<a id="motifs"></a>

## 模式

`/etc/auto-yes/patterns.conf`：每行一个 Tcl 正则表达式（`interact -re`）；空行和以 `#` 开头的行会被忽略。内置模式：

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

它要求既有问句，**又**在下一行有编号菜单的 `1.` 选项：单独的一句话（由 `cat`、`echo`、日志显示）不会触发任何操作。

| 规则 | 原因 |
|---|---|
| 针对完整菜单，而非孤立的句子 | 引用该句子的文本不应触发响应 |
| 边界用 `\s` 或 `\y`，绝不用 `\b` | 在 Tcl 中，`\b` 是退格符，而不是单词边界 |
| 开头加 `(?i)` 以忽略大小写 | 程序在「Proceed」/「proceed」之间各不相同 |
| 使用 `AUTO_YES_PATTERNS=文件 auto-yes …` 进行测试 | 该变量会在测试时替代 `/etc/auto-yes/patterns.conf` |

<a id="fonctionnement"></a>

## 工作原理

1. `auto-yes-shell` 读取模式，设置 `AUTO_YES_ACTIVE=1`，然后在伪终端中（`spawn -noecho`）启动 `$SHELL -l`。
2. `interact -o -nobuffer -re <模式> { send "1\r" }` 会复制您的终端与 shell 之间的所有内容；当程序的输出匹配某个模式时，Expect 会发送 `1` 和回车。
3. `trap … WINCH` 会将窗口大小（`stty rows/columns`）复制到 shell 的伪终端，并向其发送 `SIGWINCH`。

<a id="depannage"></a>

## 故障排查

| 症状 | 原因与解决方法 |
|---|---|
| 编辑通过 ↑/↓ 调出的命令时，行会错位或消失 | ≤ 1.1 版本：窗口大小未被中继，bash 一直停留在 80 列。已在 1.2 中修复；更新后请打开新终端。`stty size` 应显示实际大小。 |
| 没有人请求却出现了「1」 | 显示的文本匹配了某个模式（例如某个程序显示了被引用的确认菜单，或某个模式自身的代码）。请收紧该模式，或在 auto-yes 之外运行该程序（`AUTO_YES_ACTIVE=1 bash`）。 |
| 什么都没有得到回应 | 用 `AUTO_YES_PATTERNS` 检查模式；由光标序列绘制的菜单（没有真正的换行符）不会匹配 `\n`。 |
| 终端在根目录而不是当前文件夹中打开 | 「GNOME Terminal 配置文件」方法：请改用 `~/.bashrc` 方法。 |
| 为某个会话禁用 | `AUTO_YES_ACTIVE=1 bash` 会打开一个没有 auto-yes 的 shell。 |

<a id="depot"></a>

## 仓库结构

| 路径 | 内容 |
|---|---|
| `bin/auto-yes`、`bin/auto-yes-shell` | Expect 脚本 |
| `bin/auto-yes-configurer-gnome-terminal` | 与 GNOME Terminal 配置文件的挂接 |
| `etc/patterns.conf` | 内置模式（`/etc/auto-yes/patterns.conf`，配置文件在更新时会被保留） |
| `packaging/` | `build-deb.sh`、`control`、`changelog`、`copyright`、软件包脚本 |
| `tests/test_auto_yes.py` | 伪终端测试：调整大小、识别菜单、忽略孤立句子 |
| `docs/readme/` | 本 README 的另外 18 种语言版本 |

<a id="deb"></a>

## 构建软件包

```bash
python3 -m unittest discover -s tests -v   # 测试（需要 expect）
packaging/build-deb.sh                     # → dist/auto-yes_<版本>_all.deb
```

版本号来自 `packaging/changelog` 的第一行。

<a id="licence"></a>

## 许可证

[MIT](../../LICENSE)。

<a id="soutien"></a>

## 支持本项目

如果这个项目对您有帮助，一杯咖啡有助于维护它：

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=请我喝杯咖啡&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

错误报告和建议：[Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues)。安全漏洞：[SECURITY.md](../../SECURITY.md)。
