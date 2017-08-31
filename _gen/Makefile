#
# Makefile
# uralbash, 2017-08-30 10:42
#

all: check
	@# stack runghc --package http-conduit -- Stud.hs
	nix-shell -p python3 --run "python3 stud.py"

check:
	nix-shell -p mypy --run "mypy stud.py"


# vim:ft=make
#
