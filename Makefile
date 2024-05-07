.PHONY: run setup stop restart

TMUX := $(shell command -v tmux 2> /dev/null)
YARN := $(shell command -v yarn 2> /dev/null)
NPM := $(shell command -v npm 2> /dev/null)
VENV := $(shell command -v python3-venv 2> /dev/null)
PIP := $(shell command -v pip 2> /dev/null)
PYTHON := python3.10
VENV_DIR := server/venv

setup: check-dependencies create-venv install-dependencies

check-dependencies:
ifndef TMUX
	sudo apt install -y tmux
endif

ifndef YARN
	sudo apt install -y yarn
endif

ifndef NPM
	sudo apt install -y npm
endif

ifndef VENV
	sudo apt install -y python3-venv
endif

ifndef PIP
	sudo apt install -y python3-pip
endif

create-venv:
	$(PYTHON) -m venv $(VENV_DIR)

install-dependencies:
	$(VENV_DIR)/bin/pip install -r server/requirements.txt
	$(NPM) install -g yarn
	$(YARN) install

run:
	@. server/venv/bin/activate && \
	$(TMUX) new-session -d -s api 'yarn api' && echo 'api is running...' && \
	$(TMUX) new-session -d -s client 'yarn dev' && echo 'client is running...'
list:
	@$(TMUX) ls # list running processes
stop:
	@$(TMUX) send-keys -t api C-c && sleep 1
	@$(TMUX) send-keys -t client C-c
restart: stop run
