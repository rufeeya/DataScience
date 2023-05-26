import os

filesToBeDeleted=input("Enter Files to be deleted: (Comman separated)\n").split(',')
print(filesToBeDeleted)

for file in filesToBeDeleted:
    if os.path.exists(file): 
        os.remove(file)
        print("File deleted")
    else:
        print("File doesnot exist")
