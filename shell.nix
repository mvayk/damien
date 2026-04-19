{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  name = "damiens_doom";

  buildInputs = with pkgs; [
    python313
    python3Packages.pygame
    python3Packages.moderngl
    python313Packages.numpy
    python3Packages.pillow
    libGL
    libGLU
    libxkbcommon
    libxcb
    libX11
    libXrandr
    libXinerama
    libXcursor
    libXxf86vm
    pkg-config
  ];

  shellHook = ''
    echo "DAMIEN's DOOM Nix development environment"
    echo "========================================="

    source .venv/bin/activate
  '';
}
