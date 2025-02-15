#!/usr/bin/env bash

# a primary text editor
sudo dnf install nvim -y

# some other 
# fzf / bat / rg / btop
sudo dnf install -y fzf bat ripgrep btop

# default browser
flatpak install flathub app.zen_browser.zen
