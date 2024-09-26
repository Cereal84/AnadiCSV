#!/bin/bash

# Define the configuration path
CONF_PATH="${HOME}/.config/anadi/"

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

# Build Docker image
./build_image.sh

# Create the config directory if needed
if [ ! -d "$CONF_PATH" ]; then
    mkdir -p "$CONF_PATH"
fi