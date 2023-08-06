pypi: build
	twine upload dist/*

testpypi: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

build: clean_pypi
		python3 -m build

clean_pypi:
		rm -rf build dist

