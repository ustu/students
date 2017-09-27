{ pkgs ? import <nixpkgs> {} }:

let
  pythonPackages = pkgs.python36Packages;
  stdenv = pkgs.stdenv;
  python3 = pkgs.python36;

  rstcheck = pythonPackages.buildPythonPackage rec {
    name = "rstcheck-3.1";

    src = pkgs.fetchFromGitHub{
      owner = "myint";
      repo = "rstcheck";
      rev = "master";
      sha256 = "1wmjmmbg43vbkimahlj92g2bzzazwavrwg9f284zpa2npaxrlpq5";
    };


    buildInputs = with pythonPackages; [ pythonPackages.docutils ];

    doCheck = false; # some files required by the test seem to be missing
  };
in rec {
  pyEnv = stdenv.mkDerivation {
    name = "Students";
    buildInputs = [ stdenv python3 rstcheck pythonPackages.docutils ];
  };
}
