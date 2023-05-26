count=0
searchString=input("Enter the search string: ")
dupRow=""
name=input("Enter name of file to remove duplicate record: ")

def readFile():
    #print("Opening the file")
    #file = open("sample.txt", "r")
    file = open(name, "r")
    print("Reading the file")
    fileData = file.readlines()
    file.close()
    return(fileData)

def deleteRecord(fileData , row):
    #file = open("sample.txt", "w")
    file = open(name, "w")
    #print("Inside Delete Record")
    for line in fileData:
        if not line.startswith(searchString):
            file.write(line)

def finish():
    print("Exiting program... ")
    exit()

fileData = readFile()
for row in fileData:
    #print("Checking row: " , row)
    #print("row.startswith(searchString) = " , row.startswith(searchString))
    if row.startswith(searchString):
        count+=1
        dupRow = row

print("The file has ", count, " lines starting with - ", searchString)
print(dupRow)

delete = input("Do you wish to proceed to delete? Y/N \n")
deleteRecord(fileData, dupRow) if delete=="Y" else finish()
