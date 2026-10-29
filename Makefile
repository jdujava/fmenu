# fmenu - a `fzf` dmenu replacement, and related scripts

# Installation directory (default: /usr/local/bin/)
PREFIX ?= /usr/local
BIN_DIR := ${DESTDIR}${PREFIX}/bin

# List of all scripts
SCRIPTS := fmenu fmenu_run fzf-files vfzf zfzf mfzf fprompt \
           clipfmenu passfmenu fzfopen fzf-oneliner fdict \
           fmenu-run-wl clipfmenu-wl fzf-oneliner-wl

# Install scripts
install:
	@mkdir -pv "$(BIN_DIR)"
	@for script in $(SCRIPTS); do \
		install -m755 -T -- "$$script" "$(BIN_DIR)/$$script" || exit $$?; \
	done

# Uninstall scripts
uninstall:
	@for script in $(SCRIPTS); do \
		rm -fv "$(BIN_DIR)/$$script"; \
	done

.PHONY: install uninstall
