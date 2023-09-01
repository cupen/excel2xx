root_dir:=$(CURDIR)
python_venv:=$(root_dir)/.venv
python:=$(python_venv)/bin/python


init:
	python -m venv $(python_venv)


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
	tox


publish-test: build
	twine upload -r testpypi dist/*


publish: build
	twine upload dist/*

