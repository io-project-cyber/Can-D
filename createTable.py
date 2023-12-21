from tabulate import tabulate
import random

def generateTable(type):
    if type == "admin":
        #Creating Admin style table
        listSize = 50

        output = [ [0]*5 for i in range(listSize)]
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

        for x in range(1, listSize):
            output[x] = [x, random.choice(firstNameChoices), random.choice(lastNameChoices), random.choice(usernameChoices), random.choice(passwordChoices)]

        return output

def printTable(input):
    headers = input[0]
    del input[0]
    print(tabulate(input, headers, tablefmt='psql'))

myAdmin = generateTable("admin")
printTable(myAdmin)


