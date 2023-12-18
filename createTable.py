from texttable import Texttable

def printAsTable(myList):
    output = Texttable()
    output.add_rows(myList)
    print(output.draw())

T = [[11, 12, 5, 2], [15, 6,10, 0], [10, 8, 12, 5], [12,15,8,6]]
printAsTable(T)

