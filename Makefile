setup:
	@pyenv local 3.5.0
	@pyvenv env

deps:
	@pip install -r requirements-to-freeze.txt --upgrade
	@pip freeze > requirements.txt

test:
	@py.test tests -q

debug:
	@py.test --pdb tests -q

.PHONY: test setup deps
