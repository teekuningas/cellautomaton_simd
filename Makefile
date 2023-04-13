shell:
	nix develop

build: automaton.c
	gcc -O3 -fPIC -shared -o automaton.so automaton.c

start: build
	python3 main.py

format:
	black *.py
	nix fmt flake.nix
