shell:
	nix develop

build:
	cc -fPIC -shared -o automaton.so automaton.c

start:
	python3 main.py
