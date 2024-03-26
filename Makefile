root_dir:=$(CURDIR)
python_venv:=$(root_dir)/.venv
python:=$(python_venv)/bin/python


init:
	python -m venv $(python_venv)
	$(python) -m pip install -r requirements-dev.txt


reinit:
	rm -fr $(python_venv)
	make init
	

build: clean
	python setup.py sdist bdist_wheel


clean:
	rm -fr build
	rm -fr dist
	rm -fr *.egg-info
	# rm -fr ./**/__pycache__
	rm -fr ./*/__pycache__
	rm -fr ./*/*/__pycache__
	rm -fr .testdata


test:
	$(python) -m pytest --doctest-modules -v


lint:
	ruff format
	ruff check


publish-test: build
	twine upload -r testpypi dist/*


publish: build
	twine upload dist/*


.PHONY: run-exmaple
run-example: 
	$(python) -m pip install -e .
	cd example && make build
