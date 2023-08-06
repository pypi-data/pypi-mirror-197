SHELL=bash -o pipefail # Just in case

clean:
	rm -rf dist build *egg-info

release:
	python -m pip install --upgrade pip twine setuptools build
	rm -rf dist
	python -m build
	twine upload dist/*
