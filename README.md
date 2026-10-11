# `fmenu` and related scripts

This is a collection of scripts using [`fzf`](https://github.com/junegunn/fzf).
The main script is `fmenu` — fuzzy-selection dynamic menu — which can be
used as a [`dmenu`](https://tools.suckless.org/dmenu/) replacement/enhancement.

Other scripts include:

- `fmenu_run` — run binaries/commands in `$PATH`
- `vfzf` — open files in an `$EDITOR`
- `zfzf` — open PDF/DjVu/PS files in `zathura`
- `mfzf` — open manpage(s)
- `fprompt` — simple binary ("No/Yes") prompt
- `clipfmenu` — clipboard history menu
- `passfmenu` — password manager menu
- `fzfopen` — open files by the mime type
- `fdict` — fuzzy-finder interface to dictionaries
- `fzf-oneliner` — run one-liner shell scripts

## Installation

Clone this repository, then install the scripts:

```sh
make install
```

The default location is `/usr/local/bin`, which usually needs root. To install
just for your user:

```sh
make install PREFIX="$HOME/.local"
```

Make sure `~/.local/bin` is in your `PATH`. After editing a script here, run the
same install command again. Arch users can also use the package recipes in
[AUR-jdujava](https://github.com/jdujava/AUR-jdujava).

## Using fmenu

Pipe a list into `fmenu`; the selected line comes back on stdout:

```sh
printf '%s\n' apple banana orange | fmenu -p 'Fruit:'
fmenu -h
```

On Wayland, the menu opens in Foot. On X11, it uses `${TERMINAL:-st}`. Use `-f`
to run fzf directly in your current terminal. Options after `--` go to fzf.

The run, clipboard and oneliner menus keep their X11 behavior. In a Wayland
session they use the `*-wl` helpers installed by the same Makefile.

## File pickers

`vfzf` searches for files to edit, and `zfzf` searches for PDF, DjVu and
PostScript files. Both use `fd` and work when launched directly from a window
manager shortcut. Pass a directory as the first argument to search there.

The shared search definitions are in `fzf-files`. Its `lf` mode also includes
directories. If present, `~/.config/fzf/config.sh` supplies your fzf options.
File-search reload bindings should run command strings through `sh -c`;
zsh otherwise treats a space-containing `$FZF_DEFAULT_COMMAND` as one name.
`vfzf` uses fzf's `become` action to hand the terminal to the editor; Enter and
Ctrl+l open the selection. This needs fzf 0.38 or newer.

`fzfopen FILE` offers the applications registered for that file type. It uses
Python and GIO (`python-gobject` on Arch) to get application names and MIME
associations, then launches the choice with `gtk-launch`.

Dictionary and confirmation-menu settings are passed as fzf arguments, so
they work without an exported `FZF_DEFAULT_OPTS`. The general menus disable
file-search reload bindings to keep their supplied lists intact.

## Wayland helpers

- Run menu: Foot and Bash.
- Clipboard history: Foot, `cliphist` and `wl-clipboard`.
- Oneliners: Foot, `wl-clipboard`, `jq` and Mango's `mmsg`.

For oneliners, Enter runs the command and copies its output; Ctrl+y copies the
command itself. Alt+Enter returns to the original window and types the command
using `wtype`, leaving you to press Enter.
