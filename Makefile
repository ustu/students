#
# Makefile
# uralbash, 2016-10-13 18:57
#

all: build test

test:
	nix-shell . --run "rstcheck Веб-программирование/20*"

checklinks:
	@nix-shell 								 \
		-p ruby 							 \
		--run "gem install awesome_bot --bindir /tmp/gem_bin/ \
		&& /tmp/gem_bin/awesome_bot Веб-программирование/2017.5.*1.rst --allow-dupe"

build:
	cd _gen && make

# vim:ft=make
#
