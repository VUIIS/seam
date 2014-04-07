.PHONY: docs

test: clean
	python2.7 runtests.py -v --strict
	python3.3 runtests.py -v --strict

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel upload

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf seam.egg-info

docs-init:
	pip install -r docs/requirements.txt

docs:
	cd docs && make clean && make html
