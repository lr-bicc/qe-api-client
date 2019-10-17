lint:
	flake8 --statistics .

clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./pyqlikengine.egg-info

build_pkg:
	python3 setup.py sdist bdist_wheel

publish_test_pkg:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish_pkg:
	python3 -m twine upload dist/*

install_pkg_local:
	pip install .

clean_test_publish: clean build_pkg publish_test_pkg clean

clean_publish: clean build_pkg publish_pkg clean