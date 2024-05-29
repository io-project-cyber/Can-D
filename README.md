# **"Can-D" (Database in a Can)**

Can-D is a proof-of-concept cyber deception tool. Using wordlists of names and login credentials, DIAC outputs a randomly generated list of "sensitive information" (actually junk credentials) in CSV format. This tool is intended to be imported into a SQL database with high logging as a piece of "valuable information" that an attacker would steal. Being randomly generated and useless credentials, this tool is intended to **introduce uncertainty to exfiltrated data.** 

Use this in a legitimate database hosting valuable data or in a dedicated "sensor" server to bait attackers into exfiltrating completely useless data!

Features:
- **Username convention configuration** - make the junk usernames resemble real ones from your company!
- **Password complexity filtering** - make the junk passwords comply with your password policy!
- **"Telling credential"** - an exceptionally complex and unique password is inserted somewhere into the output. Use this cred to determine if your junk data is being used in a spraying attack!
- **Inject predefined credentials** - include credentials that you WANT the attacker to try. These could be real users or honey users designed to trip some other defense in your network!
- **Automatic password hashing** - make the credentials seem more realistic by storing passwords as a hash digest. Options include MD5, SHA256, SHA512, and more.
- **CLI and config file control** - adjust your credential generation and output to best fit your defenses/infrastructure!

>PLANNED: Some passwords are more common than others - it's probably unusual to see perfectly unique passwords in a company. Therefore, assign different weight to passwords based on repetition (no need to make it too complicated.)

>PLANNED: Company demographics could be interesting when selecting names. If your IT team is 50% European, roughly that many would have names based in European countries, so selecting names based off your company's real demographic information could help enhance the realism.

>PLANNED: Provide walkthrough and helper scripts for SQL import commands

## Installation
To install: 
```bash
git clone https://github.com/ouro-borous/Can-D.git
cd ./Can-D
```
If planning on using the **enhanced full name mode,**  you must install the **names-dataset** package via PyPi.
```bash
pip install names-dataset
```
It is recommended to set up a virtual environment before doing so.
```bash
python3 -m venv venv
source venv/bin/activate
pip install names-dataset
```
If you decide to use a virtual environment, remember to activate it before using enhanced full name mode.
```bash
source venv/bin/activate
```
## Dependencies
- names-dataset
## Usage
For a basic credential CSV file:
```bash
./can-d.py
```
For help with options, you can try: 
```bash
./can-d.py -h
```
For a more advanced, realistic set of names and credentials:
```bash
./can-d.py -mP online -pF sha256 -v
```
