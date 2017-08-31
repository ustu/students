with import <nixpkgs> {};

stdenv.mkDerivation rec {
  name = "StudentsEnv";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    stack
    python36Packages.pip
    mypy
    python3
  ];
}
