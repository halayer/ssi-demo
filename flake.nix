{
  description = "ssi-demo";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/25.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3;
        pythonEnv = python.withPackages (ps: with ps; [
          pip # For freezing
          cryptography
        ]);
      in {
        apps.default = {
          type = "app";
          program = toString (pkgs.writeShellScript "run" "${pythonEnv}/bin/python src/main.py $@");
        };

        devShells.default = pkgs.mkShell {
          packages = [ pythonEnv ];
          shellHook = ''
            export PS1="[dev] \u@\h:\w$ "
          '';
        };
      }
    );
}
