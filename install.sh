#!/bin/bash

# --- Includes
. scripts/utils.sh

# --- Variables
CONF_PATH="${HOME}/.config/anadi/"
BIN_DESTINATION_PATH="$HOME"
OS=""

# Makes some checks and sets ENGINE variable
check_requirements() {
    if [[ "$OS" == "Windows" ]]; then
        if where docker &>/dev/null; then
            ENGINE="docker"
        elif where podman &>/dev/null; then
            ENGINE="podman"
        else
            echo "Error: Neither Docker nor Podman is installed."
            exit 1
        fi
    else
        if command -v docker &>/dev/null; then
            ENGINE="docker"
        elif command -v podman &>/dev/null; then
            ENGINE="podman"
        else
            echo "Error: Neither Docker nor Podman is installed."
            exit 1
        fi
    fi
}

# OS detection and calling the appropriate install function
case "$OSTYPE" in
  darwin*)  
    OS="OSX" 
    ;; 
  linux*)   
    OS="Linux" 
    ;; 
  msys*|cygwin*|mingw*)  
    OS="Windows"
    ;; 
  *)        
    echo "Error: Unknown OS: $OSTYPE"
    exit 1
    ;;
esac

# Notify about the detected OS
echo -e "OS: ${Green}${OS}${NC}"

# Function to install on Debian/Ubuntu (Linux)
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

# Function to install on macOS
install_osx() {
    sudo mkdir -p /usr/local/bin
    sudo cp anadi.sh /usr/local/bin/anadi
    echo "Installed anadi.sh to /usr/local/bin/anadi"
}

# Install based on detected OS
case "$OS" in
  "Linux")
    install_linux
    ;;
  "Windows")
    install_windows
    ;;
  "OSX")
    install_osx
    ;;
esac

# Create the config directory if needed
if [ ! -d "$CONF_PATH" ]; then
    mkdir -p "$CONF_PATH"
fi
