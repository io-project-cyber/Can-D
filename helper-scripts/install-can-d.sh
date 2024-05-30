#!/bin/bash
git clone https://github.com/ouro-borous/Can-D.git
cd ./Can-D/
python3 -m venv venv
source venv/bin/activate
pip install names-dataset
echo "~~~~~~~"
echo "!READY!"
echo "~~~~~~~"
