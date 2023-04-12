shell:
	nix develop

build: automaton.c
	cc -fPIC -shared -o automaton.so automaton.c

start: build
	python3 main.py
