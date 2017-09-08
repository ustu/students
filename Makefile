#
# Makefile
# uralbash, 2016-10-13 18:57
#

all: build test

test:
	rstcheck Веб-программирование/20*	
	
build:
	cd _gen && make

# vim:ft=make
#
