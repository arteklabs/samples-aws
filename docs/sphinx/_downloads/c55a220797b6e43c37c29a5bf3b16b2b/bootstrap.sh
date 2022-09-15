#!/bin/bash

# SYSTEM DEPENDENCIES
#
# 1 - oracle client
sudo apt install libaio1
curl -o oracle_basic_client.zip https://download.oracle.com/otn_software/linux/instantclient/216000/instantclient-basic-linux.x64-21.6.0.0.0dbru.zip
unzip oracle_basic_client.zip
rm oracle_basic_client.zip
mkdir -p "$HOME/opt/oracle/"
mv instantclient* "$HOME/opt/oracle/"
sudo sh -c "echo $HOME/opt/oracle/instantclient_21_6 > /etc/ld.so.conf.d/oracle-instantclient.conf"
sudo ldconfig

# 2 - ms client (ubuntu specific)
sudo apt install python-dev python3-dev unixodbc unixodbc-dev
if ! [[ "18.04 20.04 21.04" == *"$(lsb_release -rs)"* ]]; then
    echo "Ubuntu $(lsb_release -rs) is not currently supported.";
    exit;
fi

sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list
exit

sudo apt update
sudo ACCEPT_EULA=Y apt install -y msodbcsql18
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt install -y mssql-tools18
echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
source ~/.bashrc

# APP DEPENDENCIES
python3 -m venv .env
source .env/bin/activate
python setup.py install
