#! /usr/bin/env bash

# import keybindings
cat keys/media_keys | dconf load /org/gnome/settings-daemon/plugins/media-keys/
cat keys/wm_keys | dconf load /org/gnome/desktop/wm/keybindings/
cat keys/shell_keys | dconf load /org/gnome/shell/keybindings/
cat keys/mutter_keys | dconf load /org/gnome/mutter/keybindings/
cat keys/wayland_keys | dconf load /org/gnome/mutter/wayland/keybindings/
