with import <nixpkgs> {};

stdenv.mkDerivation rec {
  name = "StudentsEnv";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    stack
    mypy
    python3
    python3Packages.pip
    python3Packages.Mako
    python3Packages.docutils
  ];
}
