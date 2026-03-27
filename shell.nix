{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  name = "damiens_doom";

  buildInputs = with pkgs; [
    python313
  ];

  shellHook = ''
    echo "DAMIEN's DOOM Nix development environment"
    echo "========================================="

    source .venv/bin/activate
  '';
}
