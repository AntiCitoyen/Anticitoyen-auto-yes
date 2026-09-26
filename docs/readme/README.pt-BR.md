<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — responder «1» sozinho às solicitações de confirmação

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![Licença MIT](https://img.shields.io/badge/licença-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-apoiar-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

Em um terminal Linux, o **auto-yes** monitora o que os programas exibem e, assim que um menu de confirmação reconhecido aparece (por padrão «Do you want to proceed?» seguido de «1. Yes»), digita **1** e depois Enter no seu lugar. O terminal permanece totalmente interativo: digitação, Ctrl-C, redimensionamento, cores.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · **🇧🇷 Português** · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes em ação" width="760"><br><em>O menu aparece, o auto-yes responde «1», o comando continua.</em></p>

> ⚠️ **Use com conhecimento de causa.** O auto-yes confirma **qualquer** solicitação que corresponda a um padrão configurado, inclusive a de um comando destrutivo (remoção de pacotes, ferramentas de disco) ou de outro programa que peça sua concordância. Mantenha os padrões restritos.

---

## Sumário

- [O que o projeto faz](#projet)
- [Instalação](#installation)
- [Uso](#utilisation)
- [Padrões](#motifs)
- [Como funciona](#fonctionnement)
- [Solução de problemas](#depannage)
- [Organização do repositório](#depot)
- [Construir o pacote](#deb)
- [Licença](#licence)
- [Apoiar o projeto](#soutien)

---

<a id="projet"></a>

## O que o projeto faz

| Comando | Papel |
|---|---|
| `auto-yes <comando> [argumentos…]` | inicia **um** comando e responde às suas solicitações de confirmação |
| `auto-yes-shell` | substitui o shell de login: **todos** os comandos digitados nesse terminal se beneficiam, sem prefixo |
| `auto-yes-configurer-gnome-terminal` | conecta o `auto-yes-shell` ao perfil padrão do GNOME Terminal (`--revert` para reverter) |
| `auto-yes --pause` / `--reprise` | suspende / restabelece as respostas em **todos** os terminais, mesmo os já abertos |
| `auto-yes --etat` / `--journal [N]` | estado atual; últimas N respostas registradas |

- **Terminal intacto**: `spawn` + `interact` do Expect; tudo o que você digita passa, apenas o padrão dispara um envio.
- **Tela calma**: a resposta só é enviada se nada for exibido 300 ms depois do menu; uma pergunta citada em um texto que rola é ignorada.
- **Registro**: cada padrão reconhecido é anotado (data, resposta ou motivo da abstenção, programa em primeiro plano, texto) em `~/.local/state/auto-yes/journal.log`.
- **Redimensionamento retransmitido**: quando a janela muda de tamanho, o shell e os programas sabem disso (edição do histórico, `less`, `vim`, `htop` permanecem corretos).
- **Padrões modificáveis sem reinstalar**: `/etc/auto-yes/patterns.conf`, relido a cada novo terminal.
- **Sem duplo empacotamento**: um terminal já sob auto-yes que relança outro não se empacota duas vezes (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Instalação

### Pacote Debian / Ubuntu

Baixe o `.deb` da [última release](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest), depois:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Dependências: `expect` (≥ 5.45) e `procps`.

### Fedora, openSUSE… (RPM) e Arch Linux

A mesma release fornece `auto-yes-<versão>-1.noarch.rpm` (`sudo dnf install ./auto-yes-*.noarch.rpm`), o `.src.rpm`, o pacote Arch (`sudo pacman -U auto-yes-*.pkg.tar.zst`) e os arquivos AUR (`aur-<versão>.tar.gz`: `PKGBUILD` e `.SRCINFO`).

### A partir do código-fonte

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Uso

### Um único comando

```bash
auto-yes apt install pacote
auto-yes ./script-interativo.sh --opcao
```

### Um terminal inteiro

**Método recomendado — `~/.bashrc`** (mantém a pasta de origem, por exemplo com *Abrir no terminal* do gerenciador de arquivos); coloque no final do arquivo:

```bash
# auto-yes em todo terminal interativo (sem duplo empacotamento, shells não interativos excluídos)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Outro método — perfil do GNOME Terminal** (execute como você mesmo, nunca com `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # novas janelas e abas → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # reverter
```

Este método não afeta nem os terminais já abertos, nem `gnome-terminal -- <comando>`, nem outros emuladores.

<a id="motifs"></a>

## Padrões

`/etc/auto-yes/patterns.conf`: uma expressão regular Tcl (`interact -re`) por linha; linhas vazias e as que começam com `#` são ignoradas. Padrão fornecido:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Ele exige a pergunta **e**, na linha seguinte, a opção `1.` de um menu numerado: a frase sozinha (exibida por `cat`, `echo`, um log) não dispara nada.

| Regra | Por quê |
|---|---|
| Visar o menu completo, não uma frase isolada | um texto que cita a frase não deve disparar uma resposta |
| `\s` ou `\y` para os limites, nunca `\b` | em Tcl, `\b` é um backspace, não um limite de palavra |
| `(?i)` no início para ignorar maiúsculas/minúsculas | os programas variam entre «Proceed» / «proceed» |
| Testar com `AUTO_YES_PATTERNS=arquivo auto-yes …` | a variável substitui `/etc/auto-yes/patterns.conf` para um teste |

### Variáveis de ambiente

| Variável | Papel | Padrão |
|---|---|---|
| `AUTO_YES_PATTERNS` | arquivo de padrões | `/etc/auto-yes/patterns.conf` |
| `AUTO_YES_CALME` | silêncio exigido após o menu, em milissegundos (`0`: resposta imediata) | `300` |
| `AUTO_YES_JOURNAL` | arquivo de registro (vazio: nada é anotado) | `~/.local/state/auto-yes/journal.log` |
| `AUTO_YES_ETAT` | pasta de estado (sinalizador de pausa) | `~/.local/state/auto-yes` |

Ajuda completa: `man auto-yes`.

<a id="fonctionnement"></a>

## Como funciona

1. O `auto-yes-shell` lê os padrões, define `AUTO_YES_ACTIVE=1`, depois inicia `$SHELL -l` em um pseudoterminal (`spawn -noecho`).
2. `interact -o -nobuffer -re <padrão>` copia tudo entre seu terminal e o shell; quando a saída do programa corresponde a um padrão, o auto-yes verifica que a pausa não está ativa e que a tela permanece calma por `AUTO_YES_CALME` ms, depois envia `1` e Enter, e anota tudo no registro.
3. Um `trap … WINCH` copia o tamanho da janela (`stty rows/columns`) para o pseudoterminal do shell e envia `SIGWINCH` a ele.

<a id="depannage"></a>

## Solução de problemas

| Sintoma | Causa e correção |
|---|---|
| Ao editar um comando resgatado com ↑/↓, a linha se desloca ou desaparece | versões ≤ 1.1: o tamanho da janela não era retransmitido, o bash ficava em 80 colunas. Corrigido na 1.2; abra um novo terminal após a atualização. `stty size` deve mostrar o tamanho real. |
| Um «1» aparece sem que ninguém tenha pedido | o texto exibido corresponde a um padrão e a tela permaneceu calma em seguida (versões ≤ 1.2: nenhuma espera). `auto-yes --journal` mostra qual programa e qual texto; restrinja o padrão, aumente `AUTO_YES_CALME`, ou `auto-yes --pause` durante a operação. |
| Nada é respondido | verifique o padrão com `AUTO_YES_PATTERNS`; um menu desenhado com sequências de cursor (sem quebras de linha reais) não corresponde a `\n`. |
| O terminal abre na raiz em vez da pasta atual | método «perfil do GNOME Terminal»: mude para o método `~/.bashrc`. |
| Um menu real não é confirmado mesmo sendo reconhecido | o programa continua exibindo algo (animação, relógio): o registro indica `ignoré:défilement`. Diminua `AUTO_YES_CALME` ou defina `0` para esse programa. |
| Desativar em todo lugar por um tempo | `auto-yes --pause` (depois `--reprise`); ou `AUTO_YES_ACTIVE=1 bash` para um shell sem auto-yes. |

<a id="depot"></a>

## Organização do repositório

| Caminho | Conteúdo |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | scripts Expect |
| `bin/auto-yes-configurer-gnome-terminal` | conexão com o perfil do GNOME Terminal |
| `share/auto-yes/commun.tcl` | código comum: padrões, tela calma, registro, pausa, tamanho de janela |
| `man/` | página de manual `auto-yes(1)` |
| `etc/patterns.conf` | padrões fornecidos (`/etc/auto-yes/patterns.conf`, arquivo de configuração preservado nas atualizações) |
| `packaging/` | `install.sh` (comum), `build-deb.sh`, `control`, `changelog`, `copyright`, scripts do pacote; `rpm/auto-yes.spec`, `aur/PKGBUILD` |
| `tests/test_auto_yes.py` | testes em pseudoterminal: redimensionamento, menu reconhecido, frase isolada e texto que rola ignorados, registro, pausa |
| `docs/readme/` | este README em outros 18 idiomas |

<a id="deb"></a>

## Construir o pacote

```bash
python3 -m unittest discover -s tests -v   # testes (requer expect)
packaging/build-deb.sh                     # → dist/auto-yes_<versão>_all.deb
```

A versão vem da primeira linha de `packaging/changelog`. A cada release publicada, `.github/workflows/release.yml` compila e anexa os pacotes RPM, Arch e os arquivos AUR.

<a id="licence"></a>

## Licença

[MIT](../../LICENSE).

<a id="soutien"></a>

## Apoiar o projeto

Se este projeto lhe é útil, um café ajuda a mantê-lo:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Pagar%20um%20café&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Relatórios de bugs e ideias: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Falhas de segurança: [SECURITY.md](../../SECURITY.md).
