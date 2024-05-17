import random

numColumns = 5
numRows = 50

def generateData():

        output = [ [0]*numColumns for i in range(numRows)]
        output[0] = ["adminID", "firstName", "lastName", "username", "password"]

        firstNameChoices = []
        with open('./firstnames.txt') as f:
            firstNameChoices = f.read().splitlines()
        lastNameChoices = []
        with open('./lastnames.txt') as f:
            lastNameChoices = f.read().splitlines()
        usernameChoices = ["kali", "root", "username", "myname"]
        with open('./usernames.txt') as f:
            usernameChoices = f.read().splitlines()
        passwordChoices = ["kali", "root", "password", "mypassword123"]
        with open('./passwords.txt') as f:
            passwordChoices = f.read().splitlines()

	#Populate
        for x in range(1, numRows):
            output[x] = [x, random.choice(firstNameChoices), random.choice(lastNameChoices), random.choice(usernameChoices), random.choice(passwordChoices)]

        return output

def printTableAsCSV(input):
    for x in range(0, numRows): #For each row:
    	for y in range(0, numColumns - 1):
    		print(input[x][y],",",end='',sep='')
    	print(input[x][numColumns - 1])







#MAIN
myAdmin = generateData()
printTableAsCSV(myAdmin)


