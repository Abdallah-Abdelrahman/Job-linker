.PHONY: run setup stop
.SILENT:

TMUX := $(shell command -v tmux 2> /dev/null) # ensure tmux is installed first

setup:
	python3 -m venv server/venv
	source server/venv/bin/activate
	pip install -r rquirements.txt
run:
	if [ ! "$(TMUX)" ]; then \
        	echo 'Error: tmux is not installed. Please install tmux to run this target.'; \
    	else \
	    . server/venv/bin/activate; \
	    tmux new-session -d -s api 'yarn api'; \
	    tmux new-session -d -s client 'yarn dev'; \
    	fi
stop:
	tmux send-keys -t api C-c
	tmux send-keys -t client C-c
