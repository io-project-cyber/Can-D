# "Can-D" (Database in a Can)

Can-D is a proof-of-concept cyber deception tool. Using wordlists of names and login credentials, DIAC outputs a randomly generated list of "sensitive information" (actually junk credentials) in CSV format. This tool is intended to be imported into a SQL database with high logging as a piece of "valuable information" that an attacker would steal. Being randomly generated and useless credentials, this tool is intended to **introduce uncertainty to exfiltrated data.** 

Use this in a legitimate database hosting valuable data or in a dedicated "sensor" server to bait attackers into exfiltrating completely uesless data!

The tool also inserts an unusually long or complex set of credentials called the "telling" credential. If you see this used somewhere else in your network or in a future attack, you'll know that the table is stolen and being used - potential attribution!

Can-D allows you to modify the username convention in config.yml by changing the number of letters taken from the first and last name of each person and the order in which the username is put together. Repeated names are given trailing numbers for uniqueness.

>PLANNED: The user can select a minimum password length. 

>PLANNED: The user can provide a list of company usernames that they want included. Done to add realism.

>PLANNED: Some passwords are more common than others - it's probably unusual to see perfectly unique passwords in a company. Therefore, assign different weight to passwords based on repetition (no need to make it too complicated.)

>PLANNED: Company demographics could be interesting when selecting names. If your IT team is 50% European, roughly that many would have names based in European countries, so selecting names based off your company's real demographic information could help enhance the realism.
