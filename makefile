BIN=venv/bin/

install: venv
	. $(BIN)activate;	pip3 install -Ur requirements.txt

venv:
	test -d venv || python3 -m venv venv

run: venv
	$(BIN)python3 Example.py


clean:
	rm -rf venv
	find -iname "*.pyc" -delete
