from tabulate import tabulate

def generateTable(type):
    if type == "admin":
        #Creating Admin style table
        output = [ [0]*5 for i in range(3)]
        output[0] = ["adminID", "firstName", "lastName", "username", "password"]
        output[1] = ["1", "Marko", "Morrison", "kali", "kali"]
        output[2] = ["2", "Brandon", "Bui", "root", "root"]
        return output

def printTable(input):
    headers = input[0]
    del input[0]
    print(tabulate(input, headers, tablefmt='psql'))

myAdmin = generateTable("admin")
printTable(myAdmin)

# headers = ["adminID", "firstName", "lastName", "username", "password"]
# row1 = [1, "Marko", "Morrison", "kali", "kali"]


