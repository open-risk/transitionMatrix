autopep8:
	autopep8 --ignore E501,E241,W690 --in-place --recursive --aggressive transitionMatrix/

lint:
	flake8 transitionMatrix

autolint: autopep8 lint

