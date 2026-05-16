#!/bin/bash

echo "Installing EduVPN..."
curl --proto '=https' --tlsv1.2 https://docs.eduvpn.org/client/linux/install.sh -O
bash ./install.sh
rm install.sh