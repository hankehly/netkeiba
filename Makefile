release-test:
	python setup.py sdist bdist_wheel && python -m twine upload --repository testpypi dist/*

release:
	python setup.py sdist bdist_wheel && python -m twine upload dist/*

