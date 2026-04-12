{ pkgs, ... }: {
  channel = "stable-23.11";

  packages = [
    # --- Python Base ---
    pkgs.python311Full
    pkgs.python311Packages.pip
    
    # --- System Tools (Essential for J.A.V.E.I.R.S. to work) ---
    pkgs.tesseract      
    pkgs.portaudio      
    pkgs.pkg-config     
    pkgs.flac           
    
    # --- Graphics Libraries for Vision ---
    pkgs.xorg.libxcb
    pkgs.libxkbcommon
    pkgs.libGL

    # --- Firebase Tools ---
    pkgs.nodePackages.firebase-tools
  ];

  env = {
    # This helps OpenCV find the correct drivers
    LD_LIBRARY_PATH = "${pkgs.libGL}/lib:${pkgs.libxkbcommon}/lib:${pkgs.xorg.libxcb}/lib";
  };

  idx = {
    extensions = [
      "ms-python.python"
      "google.gemini-code-assistant-dev"
    ];
  };
}