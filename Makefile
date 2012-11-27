all: build install
	
build:
	python setup.py build

install:
	sudo python setup.py install
