{
  description = "ssi-demo";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/25.11";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, nixpkgs-old, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python36;
        pythonEnv = python.withPackages (ps: with ps; [
          cryptography
        ]);
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      in {
        /*apps.default = {
          type = "app";
          program = toString (pkgs.writeShellScript "run" "${pythonEnv}/bin/python run.py $@");
        };*/

        devShells.default = pkgs.mkShell {
          buildInputs = [ pythonEnv ];
          shellHook = ''
            export PS1="[dev] \u@\h:\w$ "
          '';
        };
      }
    );
}
