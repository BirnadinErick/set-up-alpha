#!/bin/bash

# Update system first
echo "Updating system..."
sudo dnf update -y

# Ensure Flatpak and Flathub are set up
echo "Ensuring Flatpak and Flathub are set up..."
sudo dnf install -y flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

# 1. Apps to install via Flatpak
echo "Installing Flatpak applications..."
FLATPAK_APPS=(
    "eu.betterbird.Betterbird"              # Betterbird
    "com.microsoft.Edge"                    # Microsoft Edge
    "md.obsidian.Obsidian"                  # Obsidian
    "org.telegram.desktop"                  # Telegram
    "com.github.tchx84.Flatseal"            # Flatseal
    "fr.handbrake.ghb"                      # Handbrake
    "org.kicad.KiCad"                       # KiCAD
    "app.eduroam.geteduroam"                # geteduroam
    "org.chromium.Chromium"                 # Chromium
    "org.libreoffice.LibreOffice"           # LibreOffice
    "org.kde.okular"                        # Okular
    "com.obsproject.Studio"                 # OBS Studio
    "org.videolan.VLC"                      # VLC Media Player
    "org.zotero.Zotero"                     # Zotero
    "io.github.zen_browser.zen"             # Zen Browser
    "org.kde.kate"                          # Kate
)

for app in "${FLATPAK_APPS[@]}"; do
    echo "Installing $app..."
    flatpak install -y flathub "$app"
done
