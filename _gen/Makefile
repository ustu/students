#
# Makefile
# uralbash, 2017-08-30 10:42
#

all: check
	@# stack runghc --package http-conduit -- Stud.hs
	@echo "Runing..."
	@nix-shell 								 \
		-p python3 							 \
		-p python36Packages.Mako \
		--run "python3 stud.py"

check:
	@echo "Checking ..."
	@nix-shell \
		-p mypy \
		--run "mypy --ignore-missing-imports stud.py"


# vim:ft=make
#
