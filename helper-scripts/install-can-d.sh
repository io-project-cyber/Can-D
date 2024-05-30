#!/bin/bash
git clone https://github.com/ouro-borous/Can-D.git
cd ./Can-D/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "~~~~~~~"
echo " READY "
echo "~~~~~~~"
echo "Don't forget to activate your venv before using Can-D!"
