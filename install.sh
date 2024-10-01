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
   darwin*)  
    OS="OSX" 
    ;; 
   linux*)   
    OS="Linux" 
    install_linux   # Calling Linux installation function
    exit 1
    ;; 
  msys*|cygwin*|mingw*)  
    OS="Windows"
    install_windows  # Calling Windows installation function
    exit 1
    ;; 
  *)         
    echo "Error: Unknown OS: $OSTYPE"
    exit 1
    ;;
esac

# Notify about the detected OS
echo -e "OS: ${Green}${OS}${NC}"

# Build image (this assumes the build_image function is defined in utils.sh)
build_image $OS $ENGINE

# Create the config directory if needed
if [ ! -d "$CONF_PATH" ]; then
    mkdir -p "$CONF_PATH"
fi

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

# Copy anadi.sh in /usr/local/bin as anadi (for macOS or other Unix-like OSes)
cp anadi.sh /usr/local/bin/anadi

# Build Docker image after installation (if not handled above)
./build_image.sh || {
    echo "Error: Failed to build Docker image"
    exit 1
}
