.PHONY: run setup stop restart
.DEFAULT_GOAL:= help

TMUX := $(shell command -v tmux 2> /dev/null)
YARN := $(shell command -v yarn 2> /dev/null)
NPM := $(shell command -v npm 2> /dev/null)
PIP := $(shell command -v pip 2> /dev/null)
PYTHON := $(shell command -v python3.10 2> /dev/null)
VENV_DIR := server/venv
CYAN := \033[36m
BOLD := \e[1m
RESET := \033[0m

setup: ## install system-level tools as well as application dependencies
	@$(MAKE) -s check-dependencies create-venv install-dependencies

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
	sudo add-apt-repository ppa:deadsnakes/ppa # Add custom APT repository
	sudo apt-get install -y python3.10 python3.10-venv python3.10-dev # Install Python 3.10
	curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 # Install PIP for Python 3.10
endif

create-venv:
	$(PYTHON) -m venv $(VENV_DIR)

install-dependencies:
	$(VENV_DIR)/bin/pip install -r server/requirements.txt
	$(YARN) install

run: ## run the application in detached terminal session
	@. server/venv/bin/activate && \
	$(TMUX) new-session -d -s api 'yarn api' && echo 'api is running...' && \
	$(TMUX) new-session -d -s client 'yarn dev' && echo 'client is running...'
list: ## list current running sessions
	@$(TMUX) ls # list running processes
stop: ## stop the application session
	@$(TMUX) kill-session -t api
	@$(TMUX) kill-session -t client
restart: ## restart nextjs app
	@$(MAKE) -s stop run

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-20s$(RESET) %s\n", $$1, $$2}'
