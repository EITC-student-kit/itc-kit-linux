#!/bin/sh

#Add aplay?
LIST_OF_APPS="python3 python3-gi python3-keyring conky-all libsqlite3-dev luarocks"

#Install dependencies

echo "Performing system update"
apt-get update

echo "Installing dependencies"
apt-get install -y ${LIST_OF_APPS}
luarocks install lsqlite3

#Add pythons files to path

echo "Running python setup script"
python3 setup.py install

#Create file structure in home directory

echo "Making executable."

cp itc_kit/gui/icons/itc-icon.png /usr/share/pixmaps

cp itc_kit/itc-kit.py /usr/bin/
chmod +x /usr/bin/itc-kit.py
chmod +x itc-kit.desktop
cp itc-kit.desktop ~/.local/share/applications

echo "Creating filestructure"

su $SUDO_USER -c "

mkdir ~/.itc-kit

cp itc_kit/settings/settings ~/.itc-kit
cp itc_kit/db/itckitdb ~/.itc-kit
cp itc_kit/gui/kill_program.sh ~/.itc-kit
cp itc_kit/utils/notif_sound.wav ~/.itc-kit
touch ~/.itc-kit/user_ical
touch ~/.itc-kit/main_ical

mkdir ~/.itc-kit/icons
cp itc_kit/gui/icons/itc-icon.png ~/.itc-kit/icons
cp itc_kit/gui/icons/Icon2.png ~/.itc-kit/icons
cp itc_kit/gui/icons/Icon3.png ~/.itc-kit/icons
cp itc_kit/gui/icons/Icon4.png ~/.itc-kit/icons

mkdir ~/.itc-kit/conky
cp itc_kit/conky/conky.py ~/.itc-kit/conky
cp itc_kit/conky/Start_Conky.sh ~/.itc-kit/conky
cp itc_kit/conky/table ~/.itc-kit/conky
cp itc_kit/conky/rings ~/.itc-kit/conky

mkdir ~/.itc-kit/conky/scripts/
cp itc_kit/conky/scripts/rings.lua ~/.itc-kit/conky/scripts
cp itc_kit/conky/scripts/table.lua ~/.itc-kit/conky/scripts

cp itc_kit/mail/password_retrieval.py ~/.itc-kit/

"

echo "alias itc='itc-kit.py'" >> ~/.bashrc;

