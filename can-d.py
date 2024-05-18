import random
import datetime

numColumns = 5
numRows = 50
tellingCredLoc = int((random.random() * ((numRows - 1) / 2)) + (numRows / 2))#random point past halfway 
print("Your telling credential is at entry",tellingCredLoc)
print("-------------------------------------")

def generateData():
    #Set up table
    output = [[0]*numColumns for i in range(numRows)]
    output[0] = ["adminID", "firstName", "lastName", "username", "password"]

    #Read in credential options from wordlists
    firstNameChoices = []
    with open('./firstnames.txt') as f:
        firstNameChoices = f.read().splitlines()
    lastNameChoices = []
    with open('./lastnames.txt') as f:
        lastNameChoices = f.read().splitlines()
    usernameChoices = []
    with open('./usernames.txt') as f:
        usernameChoices = f.read().splitlines()
    passwordChoices = []
    with open('./passwords.txt') as f:
        passwordChoices = f.read().splitlines()

	#Populate table with wordlist data
    for x in range(1, numRows):
        if (x != tellingCredLoc): #If we're populating a normal random entry
            output[x] = [x, random.choice(firstNameChoices), random.choice(lastNameChoices), random.choice(usernameChoices), random.choice(passwordChoices)]
        else: #If we're populating the special telling entry
            specialUser = random.choice(usernameChoices) + random.choice(usernameChoices) + random.choice(usernameChoices)
            specialPassword = random.choice(passwordChoices) + random.choice(passwordChoices) + random.choice(passwordChoices)
            output[x] = [x, random.choice(firstNameChoices), random.choice(lastNameChoices), specialUser, specialPassword]
            print("Your telling credentials are:")
            print("UN:",specialUser)
            print("PW:",specialPassword)
            print("RECORD THESE NOW!")
            print("-------------------------------------")
    return output

def printTableAsCSV(input):
    for x in range(0, numRows): #For each row:
        for y in range(0, numColumns - 1): #For each entry, print in csv format
            print(input[x][y],",",end='',sep='')
        print(input[x][numColumns - 1])

def outputTableToCSVFile(input):
    timestamp = datetime.datetime.now()
    filename = str(timestamp) + ".csv"
    filepath = "./csv_storage/" + filename
    outputfile = open(filepath, "w+")
    for x in range(0, numRows): #For each row:
        for y in range(0, numColumns - 1): #For each entry, print in csv format
            print(input[x][y],",",end='',sep='',file=outputfile)
        print(input[x][numColumns - 1],file=outputfile)
    print("Printing to file with timestamp:",timestamp,"in ./csv_storage")
    

#MAIN

#Create table
myAdmin = generateData()
#Print it as CSV
outputTableToCSVFile(myAdmin)

