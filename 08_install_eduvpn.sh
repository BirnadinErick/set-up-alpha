#! /usr/bin/env bash
curl https://app.eduvpn.org/linux/v4/rpm/app+linux@eduvpn.org.asc | sudo tee /etc/pki/rpm-gpg/RPM-GPG-KEY-python-eduvpn-client_v4 > /dev/null
	
cat << 'EOF' | sudo tee /etc/yum.repos.d/python-eduvpn-client_v4.repo
[python-eduvpn-client_v4]
name=eduVPN for Linux 4.x (Fedora $releasever)
baseurl=https://app.eduvpn.org/linux/v4/rpm/fedora-$releasever-$basearch
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-python-eduvpn-client_v4
gpgcheck=1
enabled=1
EOF

sudo dnf install eduvpn-client
