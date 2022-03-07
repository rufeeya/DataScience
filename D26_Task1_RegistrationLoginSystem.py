#Assignment - 1
#Registration and Login system with Python, file handling
import os
spclChars = "!@#$%^&*()_+-=,./;':~`|[]{}\"\\"
def displayMenu():
  print("***** Welcome to Login and Registration System *****\nPlease choose from below options")
  print("1. Register\n2. Login\n3. Forgot Password\n4. Exit\n******************************************")
  return int(input("Enter your choice: "))
def validateEmail( email):
  emailValid = 0
  userName = email.split("@")
  #If sample email is abc@gmail.com, userName[0] = abc, userName[1] = gmail.com
  message = ""
  #Email ID validation
  if ( email.endswith("gmail.com") or email.endswith("yahoo.com") or email.endswith("icloud.com") ) and (userName[0].isalnum() or '.' in userName[0] or '_' in userName[0]) and email[email.index('@')+1] != '.' and email[0] not in spclChars:
    emailValid = 1
  else:
    message += "Invalid Email. Please check and retry"
  if emailValid:
    return "SUCCESSFUL"
  else:
    return message

def validatePassword( password ):
  message = ''
  pwdValid = 0
  spclChar, oneDigit, oneLowerChar, oneUpperChar = False, False, False, False
  #Password Validation
  for a in password:
    if a.isdigit():
      oneDigit  = True
      break
  for a in password:
    if a.islower():
      oneLowerChar  = True
      break
  for a in password:
    if a.isupper():
      oneUpperChar  = True
      break
  for a in password:
    if a in spclChars:
      spclChar  = True
      break
  if (len(password) >5 and len(password) <= 16 ) and spclChar and oneDigit and oneLowerChar and oneUpperChar:
    pwdValid = 1
  else:
    message += "Invalid Password. Please check and retry"
  if pwdValid:
    return "SUCCESSFUL"
  else:
    return message
def register( email, password):
  file1 = open("userDetails.txt", "a")
  file1.write("\n"+email + "\t" + password)
  file1.close()
  print("Registration Successful")
def getFileData():
  file2= open("userDetails.txt", "r")
  fileContents = tuple(file2.readlines())
  dictData = {}
  for a in fileContents: 
    key, val = a.split('\t')
    dictData[key ] = val.rstrip('\n')
  #print(dictData)
  file2.close()
  return dictData
def checkLoginDetails( email, password, fileData):
  registeredUser = False
  message = ''
  for x in fileData:
    if x == email:
      registeredUser = True
      message = "VALID" if fileData[x] == password else "Invalid Credentials"
  if not registeredUser:
    message = "Not a registered user, please register yourself first"
  return message
def forgotPassword( email , fileData):
  registeredUser = False
  for x in fileData:
    if x == email:
      registeredUser = True
      print("Your password is : ", fileData[email])
  if not registeredUser:
    print("Not a registered user, please register yourself first" )

choice  = displayMenu()
# if os.path.exists("RegisterLoginSystem"):
#   os.chdir("RegisterLoginSystem")
# else:
#   os.mkdir("RegisterLoginSystem")
#   os.chdir("RegisterLoginSystem")
while choice != 4:
  if choice ==1:
    print("Password Rules: Length must be 5 to 16, Must have minimum one special character, one digit, one uppercase,  one lowercase character")
    email = input("Enter email id: ")
    result = validateEmail(email)
    if result == "SUCCESSFUL":
      password = input("Enter password: ")
      result = validatePassword(password)
      if result == "SUCCESSFUL":
        print("Validation Successful. Registering..")
        register(email , password)
    else:
      print(result)

  elif choice ==2:
    email = input("Enter email id: ")
    password = input("Enter password: ")
    fileData = getFileData()
    result = checkLoginDetails( email, password, fileData)
    if result == "VALID":
      print("Login successful")
    else:
      print(result)

  elif choice == 3:
    email = input("Enter email id: ")
    fileData = getFileData()
    forgotPassword(email, fileData)
  else:
    print("Please enter a valid choice")
  choice  = int(input("Enter your choice: "))
print("Thank you for using Registration System.\nExiting ..")
