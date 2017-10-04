#
# Makefile
# uralbash, 2017-08-30 10:42
#

all: check
	@# stack runghc --package http-conduit -- Stud.hs
	@echo "Runing..."
	nix-shell --indirect --add-root .gcroots/dep \
		-p python3 							 \
		-p python3Packages.Mako \
		--run "python3 stud.py"
	
debug:
	@echo "Debug..."
	nix-shell --indirect --add-root .gcroots/dep \
		-p python3 							 \
		-p python3Packages.Mako \
		-p python3Packages.ipdb \
		--run "python3 -m pdb -c continue stud.py"

check:
	@echo "Checking ..."
	nix-shell --indirect --add-root .gcroots/dep \
		-p mypy \
		--run "mypy --ignore-missing-imports stud.py"

rst2html:
	@echo "Html..."
	nix-shell --indirect --add-root .gcroots/dep \
		-p python3Packages.sphinx \
		--run "./rst2html.sh"


# vim:ft=make
#
