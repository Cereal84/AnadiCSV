#!/bin/bash

# --- Includes
. scripts/utils.sh

# --- Variables
CONF_PATH="${HOME}/.config/anadi/"
BIN_DESTINATION_PATH="$HOME"
OS=""

# Makes some checks and sets ENGINE variable
check_requirements

# OS detection and calling the appropriate install function
case "$OSTYPE" in
  linux*)   
    OS="Linux"
    install_linux
    exit 1
    ;; 
  msys*|cygwin*|mingw*)  
    OS="Windows"
    install_windows
    exit 1
    ;;
  *)        
    echo "Unknown OS: $OSTYPE"
    exit 1
    ;;
esac

# Function to install on Debian/Ubuntu
install_linux() {
    mkdir -p "$HOME/.local/bin"
    cp "anadi.sh" "$HOME/.local/bin/anadi"
    echo "Installed anadi.sh to $HOME/.local/bin/anadi"
}

# Function to install on Windows
install_windows() {
    local target_dir="$USERPROFILE/AppData/Local/bin"
    mkdir -p "$target_dir"
    cp "anadi.sh" "$target_dir/anadi"
    echo "Installed anadi.sh to $target_dir/anadi"
}

# Build Docker image after installation
./build_image.sh
