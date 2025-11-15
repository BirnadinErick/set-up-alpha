#! /usr/bin/env bash

# AppImage Manager
flatpak install flathub it.mijorus.gearlever

# get client appimage (v4)
mkdir tmp
cd tmp/
wget https://github.com/nextcloud-releases/desktop/releases/download/v4.0.1/Nextcloud-4.0.1-x86_64.AppImage

# integrate
flatpak run it.mijorus.gearlever --integrate ./Nextcloud-4.0.1-x86_64.AppImage
 
