test:
	python runtests.py -v --strict

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel upload

# docs-init:
# 	pip install -r docs/requirements.txt

# docs:
# 	cd docs && make html