ENV=env
PIP=$(ENV)/bin/pip
RUFF=$(ENV)/bin/ruff
PYRIGHT=$(ENV)/bin/pyright

.PHONY: env install install-dev lsp fmt lintfix test run check

default: check 
check: lsp fmt test

env:
	$(info 🌍 ACTIVATING ENVIRONMENT...)
	python -m venv $(ENV)

install:
	$(info 📥 DOWNLOADING DEPENDENCIES...)
	$(PIP) install -r requirements.txt

install-dev:
	$(info 📥 DOWNLOADING DEPENDENCIES...)
	$(PIP) install -r requirements_dev.txt

lsp:
	$(info 🛠️ CHECKING STATIC TYPES...)
	$(PYRIGHT)
	
lintfix:
	$(info 🔍 RUNNING LINT TOOLS...)
	$(RUFF) check --select I --fix

fmt: lintfix
	$(info ✨ CHECKING CODE FORMATTING...)
	$(RUFF) format

test:
	$(info 🧪 TESTING...)
	./test.sh

run:
	$(info 🚀 RUNNING...)
	./main.sh
