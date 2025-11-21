#!/usr/bin/env bash

sudo dnf install -y git

# git lfs
#wget "https://github.com/git-lfs/git-lfs/releases/download/v3.6.1/git-lfs-linux-amd64-v3.6.1.tar.gz"
#tar -xvf "git-lfs-linux-amd64-v3.6.1.tar.gz"
#cd git-lfs-v3.6.1/
#sudo ./git-lfs-3.6.1/install.sh 
git lfs install

#rm -rf git-lfs-3.6.1/
#rm "git-lfs-linux-amd64-v3.6.1.tar.gz"

# git config
git config --global user.name "BirnadinErick"
git config --global user.email "45619033+BirnadinErick@users.noreply.github.com"
git config --global core.editor "nvim"
git config --global init.defaultBranch "master"
git config --global gpg.format ssh
git config --global commit.gpgsign true

# creds
ssh-keygen -t ed25519 -C "45619033+BirnadinErick@users.noreply.github.com" -f /home/be/.ssh/github_key
cat ~/.ssh/github_key.pub
git config --global user.signingkey $HOME/.ssh/github_key.pub
