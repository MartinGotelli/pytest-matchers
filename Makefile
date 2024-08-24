FOLDERS = $(shell scripts/python_folders.sh)

.PHONY: quality format coverage lint vulture spell tests requirements

default: help

.PHONY: python-env \
install-asdf \
install-pyenv \
help

##
# Variables
##
VENV_DIR=venv
PYTHON_VERSION=$(shell if [ -f .python-version ]; then cat .python-version; \
                     elif [ -f .tool-versions ]; then grep "^python " .tool-versions | cut -d ' ' -f 2; \
                     else echo "No version specified"; fi)
PYENV_BIN=$(shell pyenv which python)

###
# Public Targets
##
venv: python-env

activate: _activate

install_hooks:
	@scripts/install_hooks.sh

install_shell_support:
	@scripts/install_shell_support.sh

quality: lint vulture spell black tests

format:
	black $(FOLDERS)

black:
	black -q --check $(FOLDERS)

coverage:
	coverage run && coverage report --skip-covered

coverage_html:
	coverage run && coverage html
	open htmlcov/index.html

lint:
	pylint $(FOLDERS)

vulture:
	vulture

spell:
	codespell

tests:
	pytest src/tests

requirements: validate_env
	@make requirements_dev
	@make requirements_prod

help:
	@echo "Usage: make [target]"
	@echo "available targets:"
	@echo "\t - help: show this message"
	@echo "\t - venv: install python in venv"
	@echo "\t - install_hooks: install git hooks"
	@echo "\t - install_shell_support: install shell support"
	@echo "\t - requirements: regenerates requirements.txt and requirements_dev.txt"
	@echo "\t - quality: runs lint, style, vulture, spell, black and tests"
	@echo "\t - format: runs black"
	@echo "\t - coverage: runs coverage report"
	@echo "\t - coverage_html: runs coverage report in html"
	@echo "\t - lint: runs pylint"
	@echo "\t - vulture: runs vulture"
	@echo "\t - spell: runs codespell"
	@echo "\t - tests: runs unit tests"
	@echo "\t - activate: activates venv, usage: \`make activate\`"

###
# Private Targets
##
python-env:
	@echo "Installing python environment..."
	@echo "would you like to use asdf or pyenv? \n\t 1) pyenv \n\t 2) asdf \n\t x) exit"
	@read py_manager; \
	case $$py_manager in 1) make install-pyenv;; 2) make install-asdf;; *) echo "exiting"; exit 0;; esac
	@make install-poetry
	@echo "Bootstrap finished!"
	@echo "Consider also running:"
	@echo "    make help"
	@echo "    make install_hooks"
	@echo "    make install_shell_support"
	@echo "To activate virtual environment execute: source $(VENV_DIR)/bin/activate"

install-pyenv:
	@echo "Installing pyenv..."
	@brew install pyenv
	@echo "Installing python $(PYTHON_VERSION)..."
	@pyenv install -s $(PYTHON_VERSION)
	@echo "Creating virtual environment on $(VENV_DIR) folder..."
	$(PYENV_BIN) -m venv $(VENV_DIR)

install-asdf:
	@echo "installing python via asdf at $(VENV_DIR)"
	@asdf plugin add python
	@asdf install python $(PYTHON_VERSION)
	@python -m venv $(VENV_DIR)

install-poetry:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		source $(VENV_DIR)/bin/activate; \
		echo "source $(VENV_DIR)/bin/activate"; \
		pip install -U pip setuptools; \
		pip install poetry; \
	  	poetry install; \
	fi

_activate:
	. $(VENV_DIR)/bin/activate

validate_env:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Virtual environment not activated!"; \
		make help; \
		exit 1; \
	fi

requirements_dev:
	poetry export --without-hashes --with=dev --all-extras -o $(or $(OUTFILE),requirements_dev.txt)

requirements_prod:
	poetry export --without-hashes --all-extras -o $(or $(OUTFILE),requirements.txt)
