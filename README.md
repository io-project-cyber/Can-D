# "Can-D" (Database in a Can)

Can-D is a proof-of-concept cyber deception tool. Using wordlists of names and login credentials, DIAC outputs a randomly generated list of "sensitive information" (actually junk credentials) in CSV format. This tool is intended to be imported into a SQL database with high logging as a piece of "valuable information" that an attacker would steal. Being randomly generated and useless credentials, this tool is intended to **introduce uncertainty to exfiltrated data.** 

Use this in a legitimate database hosting valuable data or in a dedicated "sensor" server to bait attackers into exfiltrating completely uesless data!

The tool also inserts an unusually long or complex set of credentials called the "telling" credential. If you see this used somewhere else in your network or in a future attack, you'll know this database is stolen and being used - potential attribution!

>PLANNED: The user can select a minimum password length. 

>PLANNED: The user can provide a list of company usernames that they want included. Done to add realism.

>PLANNED: The user can provide a regex expression to DIAC that correspond to a naming convention. When generating usernames, DIAC follows this convention for more consistent, realistic results. Fake employee Barbara Cohen wouldn't have the username "michaelj4."

>EXAMPLE: My name is Marko Morrison and my company username is markom2. This means that I want first name + last initial + no. if repeating. With these conventions, if DIAC were to generate four names for Kathy Smith, the last username would be ksmith4.

>PLANNED: The user can choose for a single complex credential from the database to be stored in a seperate file. If this credential is found anywhere else on the network, it will be known that the database list was sprayed.

>PLANNED: Some passwords are more common than others - it's probably unusual to see perfectly unique passwords in a company. Therefore, assign different weight to passwords based on repetition (no need to make it too complicated.)

>PLANNED: Company demographics could be interesting when selecting names. If your IT team is 50% European, roughly that many would have names based in European countries, so selecting names based off your company's real demographic information could help enhance the realism.
