{ pkgs ? import <nixpkgs> {} }:

let
  pythonPackages = pkgs.python36Packages;
  stdenv = pkgs.stdenv;
  python3 = pkgs.python36;

  rstcheck = pythonPackages.buildPythonPackage rec {
    name = "rstcheck-3.1";

    src = pkgs.fetchurl {
      url = https://pypi.python.org/packages/29/86/397e91d4ec3638e331a2be493725820deec792ad5077924ed3d15c56faab/rstcheck-3.1.tar.gz;
      sha256 = "1s2xxaxnhx6yiax82q2dfi7yxmmzdq5kqcf46cz71hz7g8c2hxq8";
    };

    buildInputs = with pythonPackages; [ pythonPackages.docutils ];

    # doCheck = false; # some files required by the test seem to be missing
  };
in rec {
  pyEnv = stdenv.mkDerivation {
    name = "Students";
    buildInputs = [ stdenv python3 rstcheck pythonPackages.docutils ];
  };
}
