#!/bin/python3

import random
import datetime
import yaml
import csv
import argparse

#SET UP ARGS
parser = argparse.ArgumentParser(description="A deceptive credential generator for cyber defense. Creates a CSV output of useless, \"junk\" credentials intended to look real. Use this in a honeypot or legitimate database and introduce uncertainty to exfiltrated data. Can output to file or CLI.")
#General arguments
    #Verbosity
parser.add_argument("-q", "--quiet", help="enables quiet operation", action="store_true")
    #Output type
arg_outputType = parser.add_mutually_exclusive_group()
arg_outputType.add_argument("-c", "--cli", action="store_true", help="output the csv result to the command line")
arg_outputType.add_argument("-o", "--output-to-file", dest="outputFilePath", type=str, help="output the csv result to the provided file path")
    #Config YML to use
parser.add_argument("--config-yml-path", dest="configFilePath", type=str, help="location of the config file to use")

args = parser.parse_args()

#SET UP CONFIG FILE
#Read config file, set up global variables
configLoc = "./config.yml"
if args.configFilePath is not None:
    configLoc = args.configFilePath
config = yaml.safe_load(open(configLoc))

#Set up columns and row num
numColumns = config['general']['num_columns']
numEntries = config['general']['num_entries']

#Set up credentials to insert
credentialsToInsert = config['general']['credentials_to_include']

#Set up telling credential location
if (config['general']['telling_cred_index_in_table'] == -1): #If not specified, place the telling credential at a random point past halfway in the table
    tellingCredLoc = int((random.random() * ((numEntries - 1) / 2)) + (numEntries / 2))
else: #Otherwise, place it at the specified location
    tellingCredLoc = config['general']['telling_cred_index_in_table']

if not args.quiet:
    print("Your telling credential is at entry",tellingCredLoc)
    print("-------------------------------------")

#Set up username convention
firstNameLetterNum = config['usernames']['naming_convention']['first_name_letter_num']
lastNameLetterNum = config['usernames']['naming_convention']['last_name_letter_num']
firstNamePlacedFirst = config['usernames']['naming_convention']['first_name_placed_first']

#Set up password requirements
passwordMinLength = config['passwords']['complexity_requirements']['minimum_length']
passwordMinDigits = config['passwords']['complexity_requirements']['minimum_digits']
passwordMinSymbols = config['passwords']['complexity_requirements']['minimum_symbols']
passwordMinCaps = config['passwords']['complexity_requirements']['minimum_caps']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# When passed a credential table,
# Select and insert a full name (First name -> [1], Last name -> [2]) for each row
def generateFullNames(input):
    firstNameChoices = []
    with open('./firstnames.txt') as f:
        firstNameChoices = f.read().splitlines()
    
    lastNameChoices = []
    with open('./lastnames.txt') as f:
        lastNameChoices = f.read().splitlines()

    for x in range(1, numEntries):
        input[x][1] = random.choice(firstNameChoices)
        input[x][2] = random.choice(lastNameChoices)




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# When passed a credential table WITH FIRST AND LAST NAMES FILLED IN,
# Select and insert a username (based on the full name, username -> [3]) for each row
def generateUsernames(input):

    #TEMPORARY: Loading in username options from a file
    usernameChoices = []
    with open('./usernames.txt') as f:
        usernameChoices = f.read().splitlines()

    uniqueUsernamesPostProcess = {}

    #Iterate through list, select a username for each entry.
    for x in range(1, numEntries):
        if (x != tellingCredLoc):
            #input[x][3] = random.choice(usernameChoices)
            input[x][3] = usernameConventionApplicator(input[x][1], input[x][2], uniqueUsernamesPostProcess)
        else:
            input[x][3] = random.choice(usernameChoices) + random.choice(usernameChoices) + random.choice(usernameChoices)
            
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

    global passwordMinLength
    global passwordMinDigits
    global passwordMinSymbols
    global passwordMinCaps


    #Read in all passwords
    passwordChoices = []
    with open('./passwords.txt') as f:
        passwordChoices = f.read().splitlines()

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

    for x in range(1, numEntries):
        if (x != tellingCredLoc):
            input[x][4] = random.choice(passwordChoices)
        else:
            input[x][4] = random.choice(passwordChoices) + random.choice(passwordChoices) + random.choice(passwordChoices)




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




def generateCredentialTable():    
    #Set up table
    output = [[0]*numColumns for i in range(numEntries)]
    output[0] = ["adminID", "firstName", "lastName", "username", "password"]
    for x in range(1, numEntries):
        output[x][0] = x

    #Fill in full names of table
    generateFullNames(output) 

    #Generate username based on real name
    generateUsernames(output)

    #Read in credential options from wordlists
    generatePasswords(output)

    #Print telling credential information
    if not args.quiet:
        print("Your telling credentials are:")
        print("UN:",output[tellingCredLoc][3])
        print("PW:",output[tellingCredLoc][4])
        print("RECORD THESE NOW!")
        print("-------------------------------------")

    insertPredefinedCredentials(output)

    return output

def printTableAsCSV(input):
    for x in range(0, numEntries): #For each row:
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
    for x in range(0, numEntries): #For each row:
        for y in range(0, numColumns - 1): #For each entry, print in csv format
            print(input[x][y],",",end='',sep='',file=outputfile)
        print(input[x][numColumns - 1],file=outputfile)
    if not args.quiet:
        print("Printing to file with timestamp:",timestamp,"in ./csv_storage")
    

#MAIN

#Create table
myAdmin = generateCredentialTable()

#Print it as CSV
if (args.cli):
    printTableAsCSV(myAdmin)
else:
    outputTableToCSVFile(myAdmin)


