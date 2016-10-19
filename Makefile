init:
	pip install -r requirements.txt

test:
	python -c 'import numpy; numpy.test()'
