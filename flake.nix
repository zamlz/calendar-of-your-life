{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }: let
    forAllSystems = nixpkgs.lib.genAttrs [
      "x86_64-linux"
      "x86_64-darwin"
      "aarch64-linux"
      "aarch64-darwin"
    ];
  in
  {
    devShells = forAllSystems (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      default = pkgs.mkShell {
        packages = with pkgs; [
          # Core Packages
          python311Packages.python-dateutil
          python311Packages.pydantic
          # Dev Utiltiies
          python311Packages.ipdb
          python311Packages.ipython
          zsh
        ];
        shellHook = "exec zsh";
      };
    });
  };
}
