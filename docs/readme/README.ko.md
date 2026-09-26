<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — 확인 요청에 자동으로 「1」이라고 답하기

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![MIT 라이선스](https://img.shields.io/badge/라이선스-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-후원하기-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

Linux 터미널에서 **auto-yes**는 프로그램이 표시하는 내용을 감시하다가, 인식된 확인 메뉴(기본값으로 「Do you want to proceed?」 뒤에 「1. Yes」)가 나타나는 즉시 여러분 대신 **1**을 입력하고 Enter를 누릅니다. 터미널은 완전히 대화형으로 유지됩니다: 입력, Ctrl-C, 크기 조절, 색상.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · **🇰🇷 한국어** · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="동작 중인 auto-yes" width="760"><br><em>메뉴가 나타나고, auto-yes가 「1」이라고 답하며, 명령이 계속됩니다.</em></p>

> ⚠️ **주의해서 사용하세요.** auto-yes는 설정된 패턴과 일치하는 **모든** 요청을 확인해 버립니다. 패키지 제거, 디스크 도구 같은 파괴적인 명령이나, 동의를 요청하는 다른 프로그램의 요청도 포함됩니다. 패턴을 좁게 유지하세요.

---

## 목차

- [프로젝트 기능](#projet)
- [설치](#installation)
- [사용법](#utilisation)
- [패턴](#motifs)
- [작동 방식](#fonctionnement)
- [문제 해결](#depannage)
- [저장소 구조](#depot)
- [패키지 빌드](#deb)
- [라이선스](#licence)
- [프로젝트 후원하기](#soutien)

---

<a id="projet"></a>

## 프로젝트 기능

| 명령 | 역할 |
|---|---|
| `auto-yes <명령> [인수…]` | **하나의** 명령을 실행하고 해당 명령의 확인 요청에 답한다 |
| `auto-yes-shell` | 로그인 셸을 대체한다: 이 터미널에서 입력되는 **모든** 명령이 접두사 없이 그 혜택을 받는다 |
| `auto-yes-configurer-gnome-terminal` | `auto-yes-shell`을 GNOME Terminal 기본 프로필에 연결한다(되돌리려면 `--revert`) |

- **터미널은 그대로 유지**: Expect의 `spawn` + `interact`; 입력하는 모든 것이 그대로 통과하며, 패턴만이 전송을 트리거한다.
- **크기 조절이 중계됨**: 창 크기가 바뀌면 셸과 프로그램이 이를 인지한다(기록 편집, `less`, `vim`, `htop`이 정확하게 유지된다).
- **재설치 없이 패턴 수정 가능**: `/etc/auto-yes/patterns.conf`, 새 터미널을 열 때마다 다시 읽힌다.
- **이중 래핑 없음**: 이미 auto-yes 아래에서 실행 중인 터미널이 또 다른 터미널을 재실행해도 두 번 감싸지지 않는다(`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## 설치

### Debian / Ubuntu 패키지

[최신 릴리스](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)에서 `.deb`를 다운로드한 다음:

```bash
sudo apt install ./auto-yes_*_all.deb
```

유일한 의존성: `expect` (≥ 5.45).

### 소스에서 빌드

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## 사용법

### 단일 명령

```bash
auto-yes apt install 패키지
auto-yes ./대화형-스크립트.sh --옵션
```

### 터미널 전체

**권장 방법 — `~/.bashrc`** (시작 폴더를 유지, 예를 들어 파일 관리자의 *터미널에서 열기* 사용); 파일 끝에 추가:

```bash
# 모든 대화형 터미널에서 auto-yes 활성화 (이중 래핑 없음, 비대화형 셸 제외)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**다른 방법 — GNOME Terminal 프로필** (자신의 계정으로 실행, 절대 `sudo`로 실행하지 말 것):

```bash
auto-yes-configurer-gnome-terminal           # 새 창과 탭 → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # 되돌리기
```

이 방법은 이미 열려 있는 터미널, `gnome-terminal -- <명령>`, 다른 에뮬레이터 어느 것에도 영향을 주지 않습니다.

<a id="motifs"></a>

## 패턴

`/etc/auto-yes/patterns.conf`: 줄마다 하나의 Tcl 정규 표현식(`interact -re`); 빈 줄과 `#`으로 시작하는 줄은 무시됩니다. 기본 제공 패턴:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

이 패턴은 질문**과**, 다음 줄에 있는 번호 매김 메뉴의 `1.` 선택지를 모두 요구합니다: 문장 하나만(`cat`, `echo`, 로그에 의해 표시된 것)으로는 아무것도 실행되지 않습니다.

| 규칙 | 이유 |
|---|---|
| 고립된 문장이 아니라 메뉴 전체를 대상으로 삼는다 | 그 문장을 인용하는 텍스트가 응답을 유발해서는 안 된다 |
| 경계에는 `\s` 또는 `\y`를 사용하고 `\b`는 절대 사용하지 않는다 | Tcl에서 `\b`는 백스페이스이지 단어 경계가 아니다 |
| 대소문자를 무시하기 위해 앞에 `(?i)`를 붙인다 | 프로그램마다 「Proceed」/「proceed」로 표기가 다르다 |
| `AUTO_YES_PATTERNS=파일 auto-yes …`로 테스트한다 | 이 변수는 테스트를 위해 `/etc/auto-yes/patterns.conf`를 대체한다 |

<a id="fonctionnement"></a>

## 작동 방식

1. `auto-yes-shell`이 패턴을 읽고 `AUTO_YES_ACTIVE=1`을 설정한 다음, 가상 터미널(`spawn -noecho`)에서 `$SHELL -l`을 실행한다.
2. `interact -o -nobuffer -re <패턴> { send "1\r" }`가 터미널과 셸 사이의 모든 것을 복사한다; 프로그램의 출력이 패턴과 일치하면 Expect가 `1`과 Enter를 전송한다.
3. `trap … WINCH`가 창 크기(`stty rows/columns`)를 셸의 가상 터미널에 복사하고 `SIGWINCH`를 전송한다.

<a id="depannage"></a>

## 문제 해결

| 증상 | 원인 및 해결책 |
|---|---|
| ↑/↓로 불러온 명령을 편집할 때 줄이 밀리거나 사라진다 | 1.1 이하 버전: 창 크기가 중계되지 않아 bash가 80열에 머물러 있었다. 1.2에서 수정됨; 업데이트 후 새 터미널을 여세요. `stty size`가 실제 크기를 표시해야 한다. |
| 아무도 요청하지 않았는데 「1」이 나타난다 | 표시된 텍스트가 패턴과 일치한다(예: 인용된 확인 메뉴를 표시하는 프로그램, 또는 패턴 자체의 코드). 패턴을 좁히거나 해당 프로그램을 auto-yes 밖에서 실행하세요(`AUTO_YES_ACTIVE=1 bash`). |
| 아무 응답도 없다 | `AUTO_YES_PATTERNS`로 패턴을 확인하세요; 실제 줄바꿈 없이 커서 시퀀스로 그려진 메뉴는 `\n`과 일치하지 않는다. |
| 터미널이 현재 폴더가 아니라 루트에서 열린다 | 「GNOME Terminal 프로필」 방법: `~/.bashrc` 방법으로 전환하세요. |
| 한 세션만 비활성화 | `AUTO_YES_ACTIVE=1 bash`는 auto-yes 없는 셸을 엽니다. |

<a id="depot"></a>

## 저장소 구조

| 경로 | 내용 |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | Expect 스크립트 |
| `bin/auto-yes-configurer-gnome-terminal` | GNOME Terminal 프로필 연결 |
| `etc/patterns.conf` | 기본 제공 패턴(`/etc/auto-yes/patterns.conf`, 업데이트 시에도 유지되는 설정 파일) |
| `packaging/` | `build-deb.sh`, `control`, `changelog`, `copyright`, 패키지 스크립트 |
| `tests/test_auto_yes.py` | 가상 터미널 테스트: 크기 조절, 인식된 메뉴, 고립된 문장 무시 |
| `docs/readme/` | 이 README의 다른 18개 언어 버전 |

<a id="deb"></a>

## 패키지 빌드

```bash
python3 -m unittest discover -s tests -v   # 테스트 (expect 필요)
packaging/build-deb.sh                     # → dist/auto-yes_<버전>_all.deb
```

버전은 `packaging/changelog`의 첫 줄에서 가져옵니다.

<a id="licence"></a>

## 라이선스

[MIT](../../LICENSE).

<a id="soutien"></a>

## 프로젝트 후원하기

이 프로젝트가 도움이 되었다면, 커피 한 잔이 유지 관리에 도움이 됩니다:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=커피%20한%20잔%20사주기&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

버그 제보와 아이디어: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). 보안 취약점: [SECURITY.md](../../SECURITY.md).
