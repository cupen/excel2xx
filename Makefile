build: clean
	python setup.py sdist bdist_wheel


clean:
	rm -fr build
	rm -fr dist
	rm -fr *.egg-info


test:
	tox


publish-test: build
	twine upload -r testpypi dist/*


publish: build
	twine upload dist/*

