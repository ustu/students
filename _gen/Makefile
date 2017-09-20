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
	
debug:
	@echo "Debug..."
	@nix-shell 								 \
		-p python3 							 \
		-p python36Packages.Mako \
		-p python36Packages.ipdb \
		--run "python3 -m pdb -c continue stud.py"

check:
	@echo "Checking ..."
	@nix-shell \
		-p mypy \
		--run "mypy --ignore-missing-imports stud.py"

rst2html:
	@echo "Html..."
	@nix-shell 								   \
		-p python36Packages.sphinx \
		--run "./rst2html.sh"


# vim:ft=make
#
