<p align="center">
  <img src="../images/auto-yes.svg" alt="auto-yes" width="140">
</p>

# auto-yes — responder «1» automáticamente a las peticiones de confirmación

[![Release](https://img.shields.io/github/v/release/AntiCitoyen/Anticitoyen-auto-yes)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest)
[![CI](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml/badge.svg)](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/actions/workflows/ci.yml)
[![Licencia MIT](https://img.shields.io/badge/licencia-MIT-blue.svg)](../../LICENSE)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-apoyar-FFDD00?logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/anticitoyen)

En una terminal Linux, **auto-yes** vigila lo que muestran los programas y, en cuanto aparece un menú de confirmación reconocido (por defecto «Do you want to proceed?» seguido de «1. Yes»), teclea **1** y luego Intro en su lugar. La terminal permanece totalmente interactiva: tecleo, Ctrl-C, redimensionado, colores.

<div align="center">

[🇫🇷 Français](../../README.md) · [🇬🇧 English](README.en.md) · **🇪🇸 Español** · [🇩🇪 Deutsch](README.de.md) · [🇮🇹 Italiano](README.it.md) · [🇧🇷 Português](README.pt-BR.md) · [🇳🇱 Nederlands](README.nl.md) · [🇵🇱 Polski](README.pl.md) · [🇷🇺 Русский](README.ru.md) · [🇺🇦 Українська](README.uk.md) · [🇹🇷 Türkçe](README.tr.md) · [🇸🇦 العربية](README.ar.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇰🇷 한국어](README.ko.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Bahasa Indonesia](README.id.md)

</div>

<p align="center"><img src="../images/demo.svg" alt="auto-yes en acción" width="760"><br><em>El menú aparece, auto-yes responde «1», el comando continúa.</em></p>

> ⚠️ **Úsese con conocimiento de causa.** auto-yes confirma **cualquier** petición que coincida con un patrón configurado, incluida la de un comando destructivo (eliminación de paquetes, herramientas de disco) u otro programa que solicite su aprobación. Mantenga los patrones estrechos.

---

## Índice

- [Qué hace el proyecto](#projet)
- [Instalación](#installation)
- [Uso](#utilisation)
- [Patrones](#motifs)
- [Cómo funciona](#fonctionnement)
- [Resolución de problemas](#depannage)
- [Organización del repositorio](#depot)
- [Construir el paquete](#deb)
- [Licencia](#licence)
- [Apoyar el proyecto](#soutien)

---

<a id="projet"></a>

## Qué hace el proyecto

| Comando | Función |
|---|---|
| `auto-yes <comando> [argumentos…]` | lanza **un** comando y responde a sus peticiones de confirmación |
| `auto-yes-shell` | sustituye el shell de inicio de sesión: **todos** los comandos tecleados en esa terminal se benefician, sin prefijo |
| `auto-yes-configurer-gnome-terminal` | conecta `auto-yes-shell` al perfil de GNOME Terminal por defecto (`--revert` para deshacerlo) |
| `auto-yes --pause` / `--reprise` | suspende / restablece las respuestas en **todas** las terminales, incluso las ya abiertas |
| `auto-yes --etat` / `--journal [N]` | estado actual; últimas N respuestas registradas |

- **Terminal intacta**: `spawn` + `interact` de Expect; todo lo que teclee pasa, solo el patrón activa un envío.
- **Pantalla en calma**: la respuesta solo se envía si nada se muestra 300 ms después del menú; una pregunta citada en un texto que se desplaza se ignora.
- **Registro**: cada patrón reconocido se anota (fecha, respuesta o motivo de la abstención, programa en primer plano, texto) en `~/.local/state/auto-yes/journal.log`.
- **Redimensionado retransmitido**: cuando la ventana cambia de tamaño, el shell y los programas lo saben (edición del historial, `less`, `vim`, `htop` se mantienen correctos).
- **Patrones modificables sin reinstalar**: `/etc/auto-yes/patterns.conf`, releído en cada nueva terminal.
- **Sin doble envoltura**: una terminal ya bajo auto-yes que relanza otra no se envuelve dos veces (`AUTO_YES_ACTIVE`).

<a id="installation"></a>

## Instalación

### Paquete Debian / Ubuntu

Descargue el `.deb` de la [última release](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/releases/latest), luego:

```bash
sudo apt install ./auto-yes_*_all.deb
```

Dependencias: `expect` (≥ 5.45) y `procps`.

### Fedora, openSUSE… (RPM) y Arch Linux

La misma release ofrece `auto-yes-<version>-1.noarch.rpm` (`sudo dnf install ./auto-yes-*.noarch.rpm`), el `.src.rpm`, el paquete de Arch (`sudo pacman -U auto-yes-*.pkg.tar.zst`) y los archivos de AUR (`aur-<version>.tar.gz`: `PKGBUILD` y `.SRCINFO`).

### Desde las fuentes

```bash
git clone https://github.com/AntiCitoyen/Anticitoyen-auto-yes.git
cd Anticitoyen-auto-yes
packaging/build-deb.sh
sudo apt install ./dist/auto-yes_*_all.deb
```

<a id="utilisation"></a>

## Uso

### Un solo comando

```bash
auto-yes apt install paquete
auto-yes ./script-interactivo.sh --opcion
```

### Toda una terminal

**Método recomendado — `~/.bashrc`** (conserva la carpeta de partida, por ejemplo con *Abrir en terminal* del gestor de archivos); colóquelo al final del archivo:

```bash
# auto-yes en toda terminal interactiva (sin doble envoltura, shells no interactivos excluidos)
if [[ $- == *i* ]] && [ -z "$AUTO_YES_ACTIVE" ] && [ -x /usr/bin/auto-yes-shell ] \
   && [ "$(ps -o comm= -p "$PPID" 2>/dev/null)" != expect ]; then
  exec /usr/bin/auto-yes-shell
fi
```

**Otro método — perfil de GNOME Terminal** (ejecútelo como usted mismo, nunca con `sudo`):

```bash
auto-yes-configurer-gnome-terminal           # nuevas ventanas y pestañas → auto-yes-shell
auto-yes-configurer-gnome-terminal --revert  # deshacer
```

Este método no afecta ni a las terminales ya abiertas, ni a `gnome-terminal -- <comando>`, ni a otros emuladores.

<a id="motifs"></a>

## Patrones

`/etc/auto-yes/patterns.conf`: una expresión regular Tcl (`interact -re`) por línea; las líneas vacías y las que empiezan por `#` se ignoran. Patrón incluido:

```
(?i)do you want to proceed\??[^\n]*\n\s*1\.
```

Exige la pregunta **y**, en la línea siguiente, la opción `1.` de un menú numerado: la frase sola (mostrada por `cat`, `echo`, un registro) no activa nada.

| Regla | Por qué |
|---|---|
| Apuntar al menú completo, no a una frase aislada | un texto que cite la frase no debe activar una respuesta |
| `\s` o `\y` para los límites, nunca `\b` | en Tcl, `\b` es un retroceso, no un límite de palabra |
| `(?i)` al principio para ignorar mayúsculas/minúsculas | los programas varían entre «Proceed» / «proceed» |
| Probar con `AUTO_YES_PATTERNS=archivo auto-yes …` | la variable sustituye a `/etc/auto-yes/patterns.conf` para una prueba |

### Variables de entorno

| Variable | Función | Predeterminado |
|---|---|---|
| `AUTO_YES_PATTERNS` | archivo de patrones | `/etc/auto-yes/patterns.conf` |
| `AUTO_YES_CALME` | silencio exigido tras el menú, en milisegundos (`0`: respuesta inmediata) | `300` |
| `AUTO_YES_JOURNAL` | archivo de registro (vacío: no se anota nada) | `~/.local/state/auto-yes/journal.log` |
| `AUTO_YES_ETAT` | carpeta de estado (bandera de pausa) | `~/.local/state/auto-yes` |

Ayuda completa: `man auto-yes`.

<a id="fonctionnement"></a>

## Cómo funciona

1. `auto-yes-shell` lee los patrones, establece `AUTO_YES_ACTIVE=1`, luego lanza `$SHELL -l` en una pseudoterminal (`spawn -noecho`).
2. `interact -o -nobuffer -re <motif>` copia todo entre su terminal y el shell; cuando la salida del programa coincide con un patrón, auto-yes comprueba que la pausa no esté activa y que la pantalla haya permanecido en calma `AUTO_YES_CALME` ms, luego envía `1` e Intro, y lo anota todo en el registro.
3. Un `trap … WINCH` copia el tamaño de la ventana (`stty rows/columns`) a la pseudoterminal del shell y le envía `SIGWINCH`.

<a id="depannage"></a>

## Resolución de problemas

| Síntoma | Causa y solución |
|---|---|
| Al editar un comando recuperado con ↑/↓, la línea se desplaza o desaparece | versiones ≤ 1.1: el tamaño de la ventana no se retransmitía, bash se quedaba en 80 columnas. Corregido en 1.2; abra una nueva terminal tras la actualización. `stty size` debe mostrar el tamaño real. |
| Aparece un «1» sin que nadie lo haya pedido | el texto mostrado coincide con un patrón y la pantalla permaneció en calma después (versiones ≤ 1.2: sin ninguna espera). `auto-yes --journal` muestra qué programa y qué texto; restrinja el patrón, aumente `AUTO_YES_CALME`, o `auto-yes --pause` mientras dure la operación. |
| No se responde nada | compruebe el patrón con `AUTO_YES_PATTERNS`; un menú dibujado con secuencias de cursor (sin saltos de línea reales) no coincide con `\n`. |
| La terminal se abre en la raíz en lugar de la carpeta actual | método «perfil de GNOME Terminal»: cambie al método `~/.bashrc`. |
| Un menú real no se confirma aunque se reconozca | el programa sigue mostrando contenido (animación, reloj): el registro indica `ignoré:défilement`. Baje `AUTO_YES_CALME` o póngalo a `0` para ese programa. |
| Desactivar en todas partes un rato | `auto-yes --pause` (luego `--reprise`); o `AUTO_YES_ACTIVE=1 bash` para un shell sin auto-yes. |

<a id="depot"></a>

## Organización del repositorio

| Ruta | Contenido |
|---|---|
| `bin/auto-yes`, `bin/auto-yes-shell` | scripts Expect |
| `bin/auto-yes-configurer-gnome-terminal` | conexión al perfil de GNOME Terminal |
| `share/auto-yes/commun.tcl` | código común: patrones, pantalla en calma, registro, pausa, tamaño de ventana |
| `man/` | página de manual `auto-yes(1)` |
| `etc/patterns.conf` | patrones incluidos (`/etc/auto-yes/patterns.conf`, archivo de configuración conservado en las actualizaciones) |
| `packaging/` | `install.sh` (común), `build-deb.sh`, `control`, `changelog`, `copyright`, scripts del paquete; `rpm/auto-yes.spec`, `aur/PKGBUILD` |
| `tests/test_auto_yes.py` | pruebas en pseudoterminal: redimensionado, menú reconocido, frase aislada y texto que se desplaza ignorados, registro, pausa |
| `docs/readme/` | este README en otros 18 idiomas |

<a id="deb"></a>

## Construir el paquete

```bash
python3 -m unittest discover -s tests -v   # pruebas (requiere expect)
packaging/build-deb.sh                     # → dist/auto-yes_<versión>_all.deb
```

La versión proviene de la primera línea de `packaging/changelog`. En cada release publicada, `.github/workflows/release.yml` construye y adjunta los paquetes RPM, Arch y los archivos de AUR.

<a id="licence"></a>

## Licencia

[MIT](../../LICENSE).

<a id="soutien"></a>

## Apoyar el proyecto

Si este proyecto le resulta útil, un café ayuda a mantenerlo:

[![Buy Me a Coffee](https://img.buymeacoffee.com/button-api/?text=Invitar%20un%20café&emoji=☕&slug=anticitoyen&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff)](https://buymeacoffee.com/anticitoyen)

**https://buymeacoffee.com/anticitoyen**

Informes de errores e ideas: [Issues](https://github.com/AntiCitoyen/Anticitoyen-auto-yes/issues). Fallos de seguridad: [SECURITY.md](../../SECURITY.md).
