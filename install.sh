#!/bin/bash

# Function to install on Debian/Ubuntu
install_linux() {
    mkdir -p "$HOME/.local/bin"
    cp "anadi.sh" "$HOME/.local/bin/"
    echo "Installed anadi.sh to $HOME/.local/bin/"
}

# Function to install on Windows
install_windows() {
    local target_dir="$USERPROFILE/AppData/Local/bin"
    mkdir -p "$target_dir"
    cp "anadi.sh" "$target_dir"
    echo "Installed anadi.sh to $target_dir"

    # Optional: Add to PATH (this may need to be done manually in some cases)
    echo "Adding $target_dir to PATH..."
    setx PATH "%PATH%;$target_dir"
    echo "Added $target_dir to PATH."
}

# Main installation logic
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    install_linux
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "MacOS is not currently supported."
else
    echo "Detected OS: $OSTYPE"
    if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
        echo "Installing for Windows..."
        install_windows
    else
        echo "Unsupported operating system."
    fi
fi
