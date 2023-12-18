from tabulate import tabulate
import random

def generateTable(type):
    if type == "admin":
        #Creating Admin style table
        listSize = 3

        output = [ [0]*5 for i in range(listSize)]
        output[0] = ["adminID", "firstName", "lastName", "username", "password"]

        adminIDchoices = [1, 2]
        firstNameChoices = ["Marko", "Brandon"]
        lastNameChoices = ["Morrison", "Bui"]
        usernameChoices = ["kali", "root"]
        passwordChoices = ["kali", "root"]

        for x in range(1, listSize):
            output[x] = [random.choice(adminIDchoices), random.choice(firstNameChoices), random.choice(lastNameChoices), random.choice(usernameChoices), random.choice(passwordChoices)]

        return output

def printTable(input):
    headers = input[0]
    del input[0]
    print(tabulate(input, headers, tablefmt='psql'))

myAdmin = generateTable("admin")
printTable(myAdmin)

# headers = ["adminID", "firstName", "lastName", "username", "password"]
# row1 = [1, "Marko", "Morrison", "kali", "kali"]


