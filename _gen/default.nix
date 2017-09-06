with import <nixpkgs> {};

stdenv.mkDerivation rec {
  name = "StudentsEnv";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    stack
    mypy
    python3
    python36Packages.pip
    python36Packages.Mako
  ];
}
