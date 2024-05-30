import urllib3
import random
import datetime
import yaml
import csv
import argparse
import hashlib

#SET UP ARGS
parser = argparse.ArgumentParser(description="A deceptive credential generator for cyber defense. Creates a CSV output of useless, \"junk\" credentials intended to look real. Use this in a honeypot or legitimate database and introduce uncertainty to exfiltrated data. Can output to file or CLI. Check config.yml for more configuration options.")
#General arguments
    #Verbosity
arg_verbosity = parser.add_mutually_exclusive_group()
arg_verbosity.add_argument("-v", "--verbose", help="enables verbose operation", action="store_true")
arg_verbosity.add_argument("-q", "--quiet", help="enables quiet operation", action="store_true")
    #Output type
arg_outputType = parser.add_mutually_exclusive_group()
arg_outputType.add_argument("-c", "--cli", action="store_true", help="output the csv result to the command line")
arg_outputType.add_argument("-o", "--output-to-file", dest="outputFilePath", type=str, help="output the csv result to the provided filepath. Default: ./csv-storage/")
    #Full name mode
parser.add_argument("-nE", "--enhanced-names", dest="fullNameMode", help="activates enhanced name selection mode. Simple mode uses the default wordlists and randomly selects first and last names. Enhanced mode uses the name-dataset package and provided demographic information to select a more representative set of names. Default: simple", action="store_true")
    #Enable password online mode
parser.add_argument("-pO", "--online-passwords", dest="passwordMode", help="activates online password selection mode. Simple mode uses a stored wordlist to select passwords (Default wordlist is VERY BASIC!! REPLACE IF POSSIBLE!!) Quick and cheap, best suited for selecting simple passwords. Online mode loads a wordlist into RAM from a URL for selection. By default, this is set to a MUCH MORE ROBUST WORDLIST THAN SIMPLE MODE. Default: simple", action="store_true")
    #Password format (set to a hash option provided)
parser.add_argument("-pF", "--password-format", dest="passwordFormat", type=str, choices=["md5","sha1","sha224","sha256","sha384","sha512","sha3_224","sha3_256","sha3_384","sha3_512","shake_128","shake_256","blake2b","blake2s"], help="specify password hash format in the csv file. Default: plaintext")
    #Config YML to use
parser.add_argument("--config-yml-filepath", dest="configFilePath", type=str, help="filepath of the config file to use. Default: ./config.yml")
    #Offline mode wordlists to use 
parser.add_argument("--first-name-filepath", dest="firstNameFilePath", type=str, help="filepath of the first name wordlist to use (offline mode only.) Default: ./default-wordlists/firstnames.txt")
parser.add_argument("--last-name-filepath", dest="lastNameFilePath", type=str, help="filepath of the last name wordlist to use (offline mode only.) Default: ./default-wordlists/lastnames.txt")
parser.add_argument("--username-filepath", dest="usernameFilePath", type=str, help="filepath of the username wordlist to use (for telling credential ONLY.) Default: ./default-wordlists/usernames.txt")
parser.add_argument("--password-filepath", dest="passwordFilePath", type=str, help="filepath of the password wordlist to use (offline mode only.) Default: ./default-wordlists/passwords.txt")

args = parser.parse_args()
if args.verbose:
    print("CLI arguments successfully parsed")

#SET UP CONFIG FILE
#Read config file, set up global variables
configLoc = "./config.yml"
if args.configFilePath is not None:
    configLoc = args.configFilePath
config = yaml.safe_load(open(configLoc))
if args.verbose:
    print("Opened config YML file")
    print("Beginning configuration parsing")

#Set up columns and row num
numColumns = config['general']['num_columns']
numEntries = config['general']['num_entries']
if args.verbose:
    print("\tCONFIG: Table size successfully parsed")

#Set up telling credential location
if (config['general']['telling_cred_index_in_table'] == -1): #If not specified, place the telling credential at a random point past halfway in the table
    tellingCredLoc = int((random.random() * ((numEntries - 1) / 2)) + (numEntries / 2))
else: #Otherwise, place it at the specified location
    tellingCredLoc = config['general']['telling_cred_index_in_table']
if args.verbose:
    print("\tCONFIG: Telling credential location successfully determined")

#Set up credentials to insert
credentialsToInsert = config['general']['credentials_to_include']
if args.verbose:
    print("\tCONFIG: Predefined credentials successfully parsed")

#Set up full name demographic information for enhanced mode
demographics = config['full_names']['enhanced_mode']['demographic_distribution']
nameOptionCount = config['full_names']['enhanced_mode']['name_options']
if nameOptionCount == -1:
    nameOptionCount = 500
if args.verbose:
    print("\tCONFIG: Full name demographics successfully parsed")

#Set up username convention
firstNameLetterNum = config['usernames']['naming_convention']['first_name_letter_num']
lastNameLetterNum = config['usernames']['naming_convention']['last_name_letter_num']
firstNamePlacedFirst = config['usernames']['naming_convention']['first_name_placed_first']
if args.verbose:
    print("\tCONFIG: Username convention successfully parsed")

#Set up online mode URL
wordlistURL = config['passwords']['online_mode']['url']

#Set up password requirements
passwordMinLength = config['passwords']['complexity_requirements']['minimum_length']
passwordMinDigits = config['passwords']['complexity_requirements']['minimum_digits']
passwordMinSymbols = config['passwords']['complexity_requirements']['minimum_symbols']
passwordMinCaps = config['passwords']['complexity_requirements']['minimum_caps']
if args.verbose:
    print("\tCONFIG: Password complexity specifications successfully parsed")

#Complete
if args.verbose:
    print("Config file successfully parsed")

if not args.quiet:
    print("Your telling credential is at entry",tellingCredLoc)
    print("-------------------------------------")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Helper method for enhanced full name selection.

def ndToList(input, countryCode, usingFirstName):
    output = []
    if usingFirstName:
        if args.verbose:
            print("\t\tFinding first names from:",countryCode)
        femaleNames = input[countryCode]['F']
        maleNames = input[countryCode]['M']
        output.extend(femaleNames)
        output.extend(maleNames)
    else:
        if args.verbose:
            print("\t\tFinding last names from:",countryCode)
        output.extend(input[countryCode])
    #print("CHOICES:",output)
    return output

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# When passed a credential table,
# Select and insert a full name (First name -> [1], Last name -> [2]) for each row
def generateFullNames(input):
    if args.verbose:
        print("\tNAMES: Generating full names")
    #Simple mode
    if not args.fullNameMode: 
        if args.verbose:
            print("\tNAMES: Using simple mode")
        firstNameChoices = []
        firstNameFilePath = "./default-wordlists/firstnames.txt"
        if args.firstNameFilePath is not None:
            firstNameFilePath = args.firstNameFilePath
        with open(firstNameFilePath) as f:
            firstNameChoices = f.read().splitlines()
        
        lastNameChoices = []
        lastNameFilePath = "./default-wordlists/lastnames.txt"
        if args.lastNameFilePath is not None:
            lastNameFilePath = args.lastNameFilePath
        with open(lastNameFilePath) as f:
            lastNameChoices = f.read().splitlines()

        for x in range(1, numEntries + 1):
            input[x][1] = random.choice(firstNameChoices)
            input[x][2] = random.choice(lastNameChoices)
    
    #Enhanced mode
    else:
        global demographics
        if args.verbose:
            print("\tNAMES: Using enhanced mode. THIS MIGHT TAKE A WHILE.")
        from names_dataset import NameDataset, NameWrapper
        nd = NameDataset()
        if args.verbose:
            print("\tNAMES: Names dataset loaded.")
        #Create list of names to insert
        fullNamesToInsert = []
        #Get list of keys (countries to be used)
        if demographics is None:
            if args.verbose:
                print("\tNAMES: No demographic information found. Defaulting to {\"ANY\": 1}")
            demographics = {"ANY": 1}
        countriesToInsert = list(demographics.keys())
        #Check if ANY appears. If it does,
        if args.verbose:
            print("\tNAMES: Inputting names of nonspecified origin")
        if "ANY" in countriesToInsert:
            #Read ANY percent
            anyPercent = demographics["ANY"]
            #Find number of people to select from anywhere
            ANYToInsert = int(numEntries * anyPercent)
            
            #Get list of all countries
            allCountries = nd.get_country_codes(alpha_2=True)
            
            for x in range(0, ANYToInsert):                                                                             #For each person:
                randCountry = random.choice(allCountries)                                                                   #Select random country

                firstNamesFromRandCountry = ndToList(nd.get_top_names(n=nameOptionCount, country_alpha2=randCountry, use_first_names=True), randCountry, True)        #Select first + last name from country
                ANYfirstName = random.choice(firstNamesFromRandCountry)  
                lastNamesFromRandCountry = ndToList(nd.get_top_names(n=nameOptionCount, country_alpha2=randCountry, use_first_names=False), randCountry, False)
                ANYlastName = random.choice(lastNamesFromRandCountry)
                                                                   
                ANYfullName = [ANYfirstName, ANYlastName]                                                                   #Place into two-index list
                fullNamesToInsert.append(ANYfullName)                                                                       #Input into overall name list
            countriesToInsert.remove('ANY')
        if args.verbose:
            print("\tNAMES: Inputting names of specified origin")
        for countryCode in countriesToInsert:                                                                       #For each country
            countryPercent = demographics[countryCode]
            numCountryToInsert = int(numEntries * countryPercent)
            firstNamesFromCountry = ndToList(nd.get_top_names(n=nameOptionCount, country_alpha2=countryCode, use_first_names=True), countryCode, True)           
            lastNamesFromCountry = ndToList(nd.get_top_names(n=nameOptionCount, country_alpha2=countryCode, use_first_names=False), countryCode, False)           
            for x in range(0, numCountryToInsert):                                                                      #For each person:
                
                countryFirstName = random.choice(firstNamesFromCountry)                 # Find a first name
                
                countryLastName = random.choice(lastNamesFromCountry)                   # Find a last name
                
                fullName = [countryFirstName, countryLastName]                                                              #Place into two-index list
                fullNamesToInsert.append(fullName)                                                                          #Input into overall name list
        random.shuffle(fullNamesToInsert)                       #Shuffle list
        for x in range(1, numEntries + 1):                      #Insert list into document
            input[x][1] = fullNamesToInsert[x-1][0]
            input[x][2] = fullNamesToInsert[x-1][1]
        


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# When passed a credential table WITH FIRST AND LAST NAMES FILLED IN,
# Select and insert a username (based on the full name, username -> [3]) for each row
def generateUsernames(input):

    #TEMPORARY: Loading in username options from a file
    usernameChoices = []
    usernameFilePath = "./default-wordlists/usernames.txt"
    if args.usernameFilePath is not None:
        usernameFilePath = args.usernameFilePath
    with open(usernameFilePath) as f:
        usernameChoices = f.read().splitlines()

    uniqueUsernamesPostProcess = {}

    #Iterate through list, select a username for each entry.
    for x in range(1, numEntries + 1):
            #input[x][3] = random.choice(usernameChoices)
        input[x][3] = usernameConventionApplicator(input[x][1], input[x][2], uniqueUsernamesPostProcess)
            
#When passed a first name, last name, and list of already created usernames,
#Apply a globally defined username convention to the names, generating a unique username
def usernameConventionApplicator(firstName, lastName, uniqueUsernameDict):
    
    global firstNameLetterNum
    global lastNameLetterNum
    global firstNamePlacedFirst

    #Prepare first name and last name  
    processedFirstName = firstName                              #First name
    processedFirstName.replace(" ", "")                         #Remove spaces
    processedFirstName = processedFirstName.lower()             #Convert to lowercase
    if firstNameLetterNum != -1:                                #Take desired number of letters (if specified)
        processedFirstName = processedFirstName[:firstNameLetterNum]   

    processedLastName = lastName                                #Last name
    processedLastName.replace(" ", "")                          #Remove spaces
    processedLastName = processedLastName.lower()               #Convert to lowercase
    if lastNameLetterNum != -1:                                 #Take desired number of letters (if specified)
        processedLastName = processedLastName[:lastNameLetterNum]

    #Put these together, check uniqueUsernames to see how many times the username has been created
    uniqueUsername = ""
    if firstNamePlacedFirst:
        uniqueUsername = processedFirstName + processedLastName
    else:
        uniqueUsername = processedLastName + processedFirstName
    
    numberToAdd = ""
    if uniqueUsername in uniqueUsernameDict:                    #If the name has been created already, increment it by one, get the number, append, and return this username
        uniqueUsernameDict[uniqueUsername] += 1
        numberToAdd = uniqueUsernameDict[uniqueUsername]
        uniqueUsername += str(numberToAdd)
        return uniqueUsername
    else:                                                       #If the name hasn't been created already, crate an entry and return the username
        uniqueUsernameDict[uniqueUsername] = 1
        return uniqueUsername


    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# When passed a credential table WITH FIRST NAME, LAST NAME, AND USERNAME FILLED IN,
# Select and insert a password (password -> [4] for each row)
def generatePasswords(input):

    global wordlistURL
    global passwordMinLength
    global passwordMinDigits
    global passwordMinSymbols
    global passwordMinCaps

    #Read in all passwords
    passwordChoices = []
    #If simple mode is being used
    if args.passwordMode is None or not args.passwordMode:
        if args.verbose:
            print("\tPASSWORD: Simple mode enabled.")
        passwordFilePath = "./default-wordlists/passwords.txt"
        if args.passwordFilePath is not None:
            passwordFilePath = args.passwordFilePath
        if args.verbose:
            print("\tPASSWORD: Using",passwordFilePath)
        with open(passwordFilePath) as f:
            passwordChoices = f.read().splitlines()
    #Otherwise, online mode is being used
    else:
        if args.verbose:
            print("\tPASSWORD: Online mode enabled.")
            print("\tPASSWORD: Requesting wordlist from",wordlistURL)
        http = urllib3.PoolManager()
        resp = http.request("GET", wordlistURL)
        if args.verbose:
            print("\tPASSWORD: Request successful. Parsing into password choice list.")
        passwordChoices = resp.data.decode().split('\n')

    #Adjust password complexity specifications (defaults to no requirements)
    if passwordMinLength == -1:
        passwordMinLength = 0
    if passwordMinDigits == -1:
        passwordMinDigits = 0
    if passwordMinSymbols == -1:
        passwordMinSymbols = 0
    if passwordMinCaps == -1:
        passwordMinCaps = 0

    filteredPasswordChoices = []
    #Filter passwords based on complexity requirements
    
    
    #Filter length
    for x in range(0, len(passwordChoices)):
        if len(passwordChoices[x]) >= passwordMinLength:
            filteredPasswordChoices.append(passwordChoices[x])
    passwordChoices.clear()
    for x in range(0, len(filteredPasswordChoices)):
        passwordChoices.append(filteredPasswordChoices[x])
    filteredPasswordChoices.clear()
    
    #Filter digits
    for x in range(0, len(passwordChoices)):
        digitsInWord = []
        for y in range(0, len(passwordChoices[x])):
            if passwordChoices[x][y].isdigit():
                digitsInWord.append(passwordChoices[x][y])
        #print("Digits for",passwordChoices[x],":",digitsInWord)
        if len(digitsInWord) >= passwordMinDigits:
            filteredPasswordChoices.append(passwordChoices[x])
    passwordChoices.clear()
    for x in range(0, len(filteredPasswordChoices)):
        passwordChoices.append(filteredPasswordChoices[x])
    filteredPasswordChoices.clear()


    #Filter symbols
    symbolSet = {"!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "~", "`", "-", "_", "=", "+", "[", "]", "{", "}", "\\", "|", ";", ":", "\'", "\"", ",", ".", "<", ">", "/", "?"}
    for x in range(0, len(passwordChoices)):
        symbolsInWord = []
        for y in range(0, len(passwordChoices[x])):
            if passwordChoices[x][y] in symbolSet:
                symbolsInWord.append(passwordChoices[x][y])
        #print("Digits for",passwordChoices[x],":",digitsInWord)
        if len(symbolsInWord) >= passwordMinSymbols:
            filteredPasswordChoices.append(passwordChoices[x])
    passwordChoices.clear()
    for x in range(0, len(filteredPasswordChoices)):
        passwordChoices.append(filteredPasswordChoices[x])
    filteredPasswordChoices.clear()


    #Filter caps
    for x in range(0, len(passwordChoices)):
        capsInWord = []
        for y in range(0, len(passwordChoices[x])):
            if passwordChoices[x][y].isupper():
                capsInWord.append(passwordChoices[x][y])
        #print("Digits for",passwordChoices[x],":",digitsInWord)
        if len(capsInWord) >= passwordMinCaps:
            filteredPasswordChoices.append(passwordChoices[x])
    passwordChoices.clear()
    for x in range(0, len(filteredPasswordChoices)):
        passwordChoices.append(filteredPasswordChoices[x])
    filteredPasswordChoices.clear()

    for x in range(1, numEntries + 1):
        if (x != tellingCredLoc):
            input[x][4] = random.choice(passwordChoices)
        else:
            input[x][4] = random.choice(passwordChoices) + random.choice(passwordChoices) + random.choice(passwordChoices)
            #Print telling credential information
            if not args.quiet:
                print("\nYour telling credentials are:")
                print("UN:",input[tellingCredLoc][3])
                print("PW:",input[tellingCredLoc][4])
                if args.passwordFormat is not None: print("**WARNING** Password will be hashed upon output **WARNING**")
                print("RECORD THESE NOW!\n")




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def insertPredefinedCredentials(output):
    #Check if there's credentials in the first place.
    #If there are,
    global credentialsToInsert
    if credentialsToInsert is not None:
        #parse them as a CSV
        formatted_cred = csv.reader(credentialsToInsert)
        #for each entry in the list, choose a random index in the list, insert a new row, add the creds
        for x in formatted_cred:
            insertionIndex = int(random.random() * (len(output)-1))
            output.insert(insertionIndex, [insertionIndex])
            for y in x:
                (output[insertionIndex]).append(y)
            
            #increment every ID ([x][1]) after 
            for z in range(insertionIndex + 1, len(output) - 1):
                output[z][0] += 1



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def hashPasswords(output):
    for x in range(1, len(output)): #For each row:
        plaintextPassword = output[x][4]
        hashedPassword = ""
        match args.passwordFormat:
            case "md5": hashedPassword = hashlib.md5(plaintextPassword.encode()).hexdigest()
            case "sha1": hashedPassword = hashlib.sha1(plaintextPassword.encode()).hexdigest()
            case "sha224": hashedPassword = hashlib.sha224(plaintextPassword.encode()).hexdigest()
            case "sha256": hashedPassword = hashlib.sha256(plaintextPassword.encode()).hexdigest()
            case "sha384": hashedPassword = hashlib.sha384(plaintextPassword.encode()).hexdigest()
            case "sha512": hashedPassword = hashlib.sha512(plaintextPassword.encode()).hexdigest()
            case "sha3_224": hashedPassword = hashlib.sha3_224(plaintextPassword.encode()).hexdigest()
            case "sha3_256": hashedPassword = hashlib.sha3_256(plaintextPassword.encode()).hexdigest()
            case "sha3_384": hashedPassword = hashlib.sha3_384(plaintextPassword.encode()).hexdigest()
            case "sha3_512": hashedPassword = hashlib.sha3_512(plaintextPassword.encode()).hexdigest()
            case "shake_128": hashedPassword = hashlib.shake_128(plaintextPassword.encode()).hexdigest()
            case "shake_256": hashedPassword = hashlib.shake_256(plaintextPassword.encode()).hexdigest()
            case "blake2b": hashedPassword = hashlib.blake2b(plaintextPassword.encode()).hexdigest()
            case "blake2s": hashedPassword = hashlib.blake2s(plaintextPassword.encode()).hexdigest()
        output[x][4] = hashedPassword



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generateCredentialTable():    
    #Set up table
    output = [[0]*numColumns for i in range(0, numEntries + 1)]
    output[0] = ["adminID", "firstName", "lastName", "username", "password"]
    for x in range(1, numEntries + 1):
        output[x][0] = x
    
    #Fill in full names of table
    if args.verbose:
        print("Selecting full names")
    generateFullNames(output) 

    #Generate username based on real name
    if args.verbose:
        print("Generating usernames")
    generateUsernames(output)

    #Read in credential options from wordlists
    if args.verbose:
        print("Selecting passwords")
    generatePasswords(output)

    if args.passwordFormat is not None:
        if args.verbose:
            print("Hashing passwords")
        hashPasswords(output)
    
    insertPredefinedCredentials(output)

    return output

def printTableAsCSV(input):
    for x in range(0, numEntries + 1): #For each row:
        for y in range(0, numColumns - 1): #For each entry, print in csv format
            print(input[x][y],",",end='',sep='')
        print(input[x][numColumns - 1])

def outputTableToCSVFile(input):
    timestamp = datetime.datetime.now()
    filepath = ""
    if args.outputFilePath is not None:
        filepath = args.outputFilePath
    else:
        filename = str(timestamp) + ".csv"
        filepath = "./csv-storage/" + filename
    outputfile = open(filepath, "w+")
    for x in range(0, numEntries + 1): #For each row:
        for y in range(0, numColumns - 1): #For each entry, print in csv format
            print(input[x][y],",",end='',sep='',file=outputfile)
        print(input[x][numColumns - 1],file=outputfile)
    if not args.quiet:
        print("Printing to file with timestamp:",timestamp,"in ./csv_storage")
    

#MAIN

#Create table
if args.verbose:
    print("Beginning credential generation")

myAdmin = generateCredentialTable()
if not args.quiet:
    print("Credential generation complete")
    print("-------------------------------------")

#Print it as CSV
if args.verbose:
    print("Beginning output process")
if (args.cli):
    printTableAsCSV(myAdmin)
else:
    outputTableToCSVFile(myAdmin)
if args.verbose:
    print("Output process complete")


