#! /usr/bin/env bash

if [ ! -d "./keys/" ]; then
	mkdir keys
fi

dconf dump /org/gnome/settings-daemon/plugins/media-keys/ > keys/media_keys
dconf dump /org/gnome/desktop/wm/keybindings/ > keys/wm_keys
dconf dump /org/gnome/shell/keybindings/ > keys/shell_keys
dconf dump /org/gnome/mutter/keybindings/ > keys/mutter_keys
dconf dump /org/gnome/mutter/wayland/keybindings/ > keys/wayland_keys
