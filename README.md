# "Can-D" (Database in a Can)

Can-D is a proof-of-concept cyber deception tool. Using wordlists of names and login credentials, DIAC outputs a randomly generated list of "sensitive information" (actually junk credentials) in CSV format. This tool is intended to be imported into a SQL database with high logging as a piece of "valuable information" that an attacker would steal. Being randomly generated and useless credentials, this tool is intended to **introduce uncertainty to exfiltrated data.** 

Use this in a legitimate database hosting valuable data or in a dedicated "sensor" server to bait attackers into exfiltrating completely uesless data!

Features:
- **Username convention configuration** - make the junk usernames resemble real ones from your company!
- **Password complexity filtering** - make the junk passwords comply with your password policy!
- **"Telling credential"** - an exceptionally complex and unique password is inserted somewhere into the output. Use this cred to determine if your junk data is being used in a spraying attack!

>PLANNED: The user can select a minimum password length. 

>PLANNED: The user can provide a list of company usernames that they want included. Done to add realism.

>PLANNED: Some passwords are more common than others - it's probably unusual to see perfectly unique passwords in a company. Therefore, assign different weight to passwords based on repetition (no need to make it too complicated.)

>PLANNED: Company demographics could be interesting when selecting names. If your IT team is 50% European, roughly that many would have names based in European countries, so selecting names based off your company's real demographic information could help enhance the realism.
