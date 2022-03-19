# Phonebook Task(MongoDB)
 
# 1.create contact(name ,number,mail id)
# 2.search contact(name or number)
# 3.delete contact(name)
# 4.display all contacts(as a pandas dataframe) 
# conditions:
# 1.everything must be an user input

# !pip install dnspython
# !pip install pymongo[srv]

import pymongo
import pandas as pd

client = pymongo.MongoClient("mongodb+srv://rufeeya:Rufi2711@cluster0.g2djj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.phoneBook
records = db.myContacts

def displayMenu():
  print("1. Add Contact\n2. Search contact\n3. Delete contact\n4. View All Contacts\n5. Exit")

def addContact():
  inputDict = {'name':input("Enter Name: "),'number':input("Enter Phone Number: "),'email':input("Enter Email ID: ")}
  records.insert_one(inputDict)

def searchChoiceQuery():
  searchChoice = int(input("\n1. By Name or 2. By Number: "))
  if searchChoice == 1:
    query = {"name":input("Enter a name to search: ")}
  elif searchChoice ==2:
    query = {"number":input("Enter a number to search: ")}
  else:
    print("Enter a valid search choice")
    return None
  return query

def searchContact():
  query = searchChoiceQuery()
  print(records.find_one(query, {"_id":0} ))

def deleteContact():
  query = {"name":input("Enter a name to search: ")}
  x = records.count_documents(query)
  if x>0:
    records.delete_one(query)
    print("Record Deleted")
  else:
    print("No record found")

def viewAll():
  df = pd.DataFrame(records.find({},{"_id":0}))
  print(df)

## Start Point ##
displayMenu()
cont = True
while cont:
  choice = int(input("Enter your choice: "))
  if choice ==1:
    addContact()
  elif choice ==2:
    searchContact()
  elif choice ==3:
    deleteContact()
  elif choice ==4:
    viewAll()
  else:
    cont = False
    print("Exiting .. ")
