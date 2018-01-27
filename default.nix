{ pkgs ? import <nixpkgs> {} }:

let
  pythonPackages = pkgs.python3Packages;
  stdenv = pkgs.stdenv;
  python3 = pkgs.python3;

  rstcheck = pythonPackages.buildPythonPackage rec {
    name = "rstcheck-3.1";

    src = pkgs.fetchFromGitHub{
      owner = "myint";
      repo = "rstcheck";
      rev = "v3.1";
      sha256 = "08z0phzxvga6m5c9j1vgl7c7lwh2c50mxkdxx08fm9hzabr0iwg6";
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
