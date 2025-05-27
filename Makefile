# fmenu - a `fzf` dmenu replacement, and related scripts

# Installation directory (default: /usr/local/bin/)
PREFIX ?= /usr/local
BIN_DIR := ${DESTDIR}${PREFIX}/bin

# List of all scripts
SCRIPTS := fmenu fmenu_run vfzf zfzf mfzf fprompt \
           clipfmenu passfmenu fzfopen fzf-oneliner fdict

# Install scripts
install:
	@mkdir -pv "$(BIN_DIR)"
	@for script in $(SCRIPTS); do \
		cp -fv "$$script" "$(BIN_DIR)"; \
		chmod 755 "$(BIN_DIR)/$$script"; \
	done

# Uninstall scripts
uninstall:
	@for script in $(SCRIPTS); do \
		rm -fv "$(BIN_DIR)/$$script"; \
	done

.PHONY: install uninstall
