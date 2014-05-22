#!/bin/sh
LIST_OF_APPS="python3 python3-gi python3-keyring conky-all libsqlite3-dev luarocks"

apt-get update
apt-get install -y ${LIST_OF_APPS}
luarocks install lsqlite3

python3 setup.py install
cp ITCKit/EITC-kit.py /usr/bin/
chmod +x /usr/bin/EITC-kit.py

while true; do
    read -p "Use the default terminal shorthand? (itc) (yes/no)" yn
    case ${yn} in
        [Yy]* ) echo "alias itc='EITC-kit.py'" >> ~/.bashrc;;
        [Nn]* ) read -p "Enter the preferred shorthand: " shorthand;
        echo "alias $shorthand='EITC-kit.py'" >> ~/.bashrc;
        echo "After reopening terminal, EITC-kit can be run by using the shorthand $shorthand in your terminal";
        exit;;
        * ) echo "Please answer y or n.";;
    esac
done