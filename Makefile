.PHONY: run setup stop restart

TMUX := $(shell command -v tmux 2> /dev/null)
YARN := $(shell command -v yarn 2> /dev/null)
NPM := $(shell command -v npm 2> /dev/null)
PIP := $(shell command -v pip 2> /dev/null)
PYTHON := python3.10
VENV_DIR := server/venv

setup: check-dependencies create-venv install-dependencies

check-dependencies:
ifndef TMUX
	sudo apt-get update
	sudo apt-get install -y tmux
endif

ifndef YARN
ifndef NPM
	sudo apt-get update
	sudo apt-get install -y npm
endif
	sudo npm install -g yarn
endif

ifndef PYTHON
	sudo apt-get update
	sudo apt-get install -y python3.10 python3.10-venv python3.10-dev
endif

create-venv:
	$(PYTHON) -m venv $(VENV_DIR)

install-dependencies:
	$(VENV_DIR)/bin/pip install -r server/requirements.txt
	$(YARN) install

run:
	@. server/venv/bin/activate && \
	$(TMUX) new-session -d -s api 'yarn api' && echo 'api is running...' && \
	$(TMUX) new-session -d -s client 'yarn dev' && echo 'client is running...'
list:
	@$(TMUX) ls # list running processes
stop:
	@$(TMUX) send-keys -t api C-c && sleep 0.2
	@$(TMUX) send-keys -t client C-c && sleep 0.2
restart: stop run
