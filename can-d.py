import random
import datetime

numColumns = 5
numRows = 50
tellingCredLoc = int((random.random() * ((numRows - 1) / 2)) + (numRows / 2))#random point past halfway 
print("Your telling credential is at entry",tellingCredLoc)
print("-------------------------------------")

# When passed a credential table,
# Select and insert a full name (First name -> [1], Last name -> [2]) for each row
def generateFullNames(input):
    firstNameChoices = []
    with open('./firstnames.txt') as f:
        firstNameChoices = f.read().splitlines()
    
    lastNameChoices = []
    with open('./lastnames.txt') as f:
        lastNameChoices = f.read().splitlines()

    for x in range(1, numRows):
        input[x][1] = random.choice(firstNameChoices)
        input[x][2] = random.choice(lastNameChoices)




# When passed a credential table WITH FIRST AND LAST NAMES FILLED IN,
# Select and insert a username (based on the full name, username -> [3]) for each row
# TODO - Use some kind of reverse regex to follow a naming convention
def generateUsernames(input):
    usernameChoices = []
    with open('./usernames.txt') as f:
        usernameChoices = f.read().splitlines()
    for x in range(1, numRows):
        if (x != tellingCredLoc):
            input[x][3] = random.choice(usernameChoices)
        else:
            input[x][3] = random.choice(usernameChoices) + random.choice(usernameChoices) + random.choice(usernameChoices)
            
        



# When passed a credential table WITH FIRST NAME, LAST NAME, AND USERNAME FILLED IN,
# Select and insert a password (password -> [4] for each row)
def generatePasswords(input):
    passwordChoices = []
    with open('./passwords.txt') as f:
        passwordChoices = f.read().splitlines()

    for x in range(1, numRows):
        if (x != tellingCredLoc):
            input[x][4] = random.choice(passwordChoices)
        else:
            input[x][4] = random.choice(passwordChoices) + random.choice(passwordChoices) + random.choice(passwordChoices)



def generateCredentialTable():    
    #Set up table
    output = [[0]*numColumns for i in range(numRows)]
    output[0] = ["adminID", "firstName", "lastName", "username", "password"]

    #Fill in full names of table
    generateFullNames(output) 

    #Generate username based on real name
    generateUsernames(output)

    #Read in credential options from wordlists
    generatePasswords(output)

    #Print telling credential information
    print("Your telling credentials are:")
    print("UN:",output[tellingCredLoc][3])
    print("PW:",output[tellingCredLoc][4])
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
myAdmin = generateCredentialTable()


#Print it as CSV

outputTableToCSVFile(myAdmin)


