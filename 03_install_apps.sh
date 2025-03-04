#! /usr/bin/env bash

# set up necessary repos
# ms repos
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null

sudo dnf upgrade -y --refresh

sudo dnf install -y chromium code

flatpak install flathub -y md.obsidian.Obsidian
flatpak install flathub -y com.obsproject.Studio
#flatpak install flathub -y com.google.AndroidStudio
flatpak install flathub -y com.play0ad.zeroad
flatpak install flathub com.github.alexhuntley.Plots -y
flatpak install flathub -y org.gnome.World.PikaBackup
flatpak install flathub -y org.gnome.design.Emblem

# jetbrains toolbox app v 2.5.3
if [ ! -d "jetbrains-toolbox-2.5.3.37797/" ]; then
	wget "https://download.jetbrains.com/toolbox/jetbrains-toolbox-2.5.3.37797.tar.gz"
	tar -xvf jetbrains-toolbox-2.5.3.37797.tar.gz
	cd jetbrains-toolbox-2.5.3.37797/
	mv jetbrains-toolbox ~/bin/
	rm -rf "jetbrains-toolbox-2.5.3.37797/"
fi

# ki-cad stable
sudo dnf install kicad kicad-packages3d kicad-doc -y
