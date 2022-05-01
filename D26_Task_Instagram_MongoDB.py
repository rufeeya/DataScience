#Instagram using MongoDB and Python
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io
import time

client = pymongo.MongoClient("mongodb+srv://rufeeya:Rufi2711@cluster0.g2djj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.instaGram
records = db.myInsta
    
def displayMenu():
  print("Instagram".center(30,"*"))
  print("1. Register \n2. Login\n3. Exit")

def showImage( pic ):
    pil_img = Image.open(io.BytesIO(pic)) 
    plt.imshow(pil_img)
    plt.show()
    #pil_img.show()

def displayRecord( x  ):
  pics = x["picDetails"]
  for pic in pics:
    imagesList = availableImages( x["_id"] )
    if len(imagesList)  == 0:
      print("{} has not uploaded any image".format(x["_id"]))
    else:
      print("*" * 30)
      print(x["_id"] + " posted " , end = "")
      print(pic["caption"])
      showImage( pic['image'] )
      like = len(pic['likes'])
      comments = pic['comments']
      print(str(like) + " likes | "+ str(len(comments))+ " Comments")
      if len(comments)>0:
        print("Comments:\n")
        for comment in comments:
          (key, value), = comment.items()
          print(key,": ", value)

def initial():
   displayMenu()
   ch = input("Enter your choice: ")
   repeat = True
   while repeat:
      if ch == "3":
        print("Thank you")
        repeat = False
        break
      else:
        switcher = {
                    "1": userRegister,
                    "2": userLogin
                  } 
        switcher.get(ch, "Enter Valid Choice")()
        ch = input("Enter your choice: ")

def addPic(userId):
    name = input("Pic Name: ")
    im = Image.open("/content/"+name)
    image_bytes = io.BytesIO()
    im.save(image_bytes, format = 'JPEG')
    
    query = records.find_one({"_id":userId})
    #print("Found:\n", query )
    details ={"$push": {'picDetails':{
                              'image':image_bytes.getvalue(),
                              'caption':input("Enter Name: "),
                              "$currentDate":{"lastModified":True},
                              'likes':[],
                              'comments':[]
                            }       
              }}
    records.update_one(query,details)
    
def allFeeds(userId):
    print(userId + "'s Feeds")
    for x in records.find({},{"password":0,"mail":0}).sort("picDetails.lastModfied"):
            displayRecord(x)

def availableImages( friend ):
  imagesList = []
  userData =  records.find_one({"_id":friend})
  for img in userData["picDetails"]:
    imagesList.append(img["caption"])
  return imagesList

def availableFriends( userId ):
    friendsList = []
    userData =  records.find({},{"_id":1})
    print(userData)
    for i in userData:
      (k,v), = i.items()    
      if v != userId:
        friendsList.append(v)
    return friendsList

def likeImage( userId):
  print("*** {}'s Friends: ***".format(userId))
  print(availableFriends( userId ))
  friend = input("Whose Pic do you wanna like ? ")
  if userId == friend:
    print("You cannot like your own image!")
  else:
    imagesList = availableImages( friend )
  if len(imagesList) > 0:
      print("Images uploaded by " + friend + ":")
      print(imagesList)
      likedAlready = []
      like = input("Which image do you wanna like? ")
      imgData =  records.find_one({"_id":friend})
      for i in imgData["picDetails"]:
        if i["caption"] == like:
          likedAlready = i["likes"]
      if userId in likedAlready:
        print("You have already liked this image!")
      else:
        query = records.find_one({ "$and" : [{"_id":friend},{"picDetails.caption":like}]})
        details ={"$push": {"picDetails.$[].likes": userId }}
        #records.update_one(query,details)
        print("{} liked the image: {}".format(userId, like))
        likedPicDetails = imgData["picDetails"]
        #print(likedPicDetails)
        for pic in likedPicDetails:
          if pic["caption"] == like:
            showImage( pic['image'] )
  else:
      print("{} has not uploaded any image".format(friend))

def commentImage( userId ):
  friend = input("Whose Pic do you wanna comment on ? ")
  imagesList = availableImages( friend )
  if len(imagesList) > 0:
      print("Images uploaded by " + friend + ":")
      print(imagesList)
      commentImg = input("Which image do you wanna comment on? ")
      comment = input("Enter your comment: ")
      imgData =  records.find_one({"_id":friend})
      query = records.find_one({ "$and" : [{"_id":friend},{"picDetails.caption":commentImg}]})
      details ={"$push": {"picDetails.$[].comments": { userId : comment }}}
      records.update_one(query,details)
      print("{} commented on {}'s image: {}".format(userId, friend, commentImg))
  else:
    print("{} has not uploaded any image".format(friend))

def displayFriendFeed(userId):
   friend = input("Whose feed do you wanna see? ")
   print(friend + "'s Feeds")
   for x in records.find({"_id":friend},{"password":0,"mail":0}).sort("picDetails.lastModfied"):
            displayRecord(x)

def friendsProfile(userId):
     userInput = input("1. View All Pics \n2. Like\n3. Comment\n")
     switcher = {
                 "1": displayFriendFeed,
                 "2": likeImage,
                 "3": commentImage,
                }
     switcher.get(userInput, "Enter Valid Choice")(userId) 
        
def welcomeToInsta( userId ):
    print("\nWelcome " + userId + "!")
    repeat = True
    choice = input("What would you like to do today?\n1. Add Post\n2. All Feeds\n3. Friend's Profile \n4. Log out\n")
    while repeat:
      if choice == "4":
        repeat = False
        initial()
      else:
        switcher = {
                 "1": addPic,
                 "2": allFeeds,
                 "3": friendsProfile,
                }
        switcher.get(choice, "Enter Valid Choice")(userId)      
        choice = input("What would you like to do next?\n1. Add Post\n2. All Feeds\n3. Friend's Profile \n4. Log out\n")
    return()    
    
def userRegister():
    userData = {
        "_id": input("Enter user name: "),
        "password":input("Enter Password: "),
        "mail": input("Enter Email: "),
        'picDetails': []
        }
    records.insert_one(userData)
    print("User Registered Successfully")

def userLogin():
    uid = input("Enter user name: ")
    pwd = input("Enter Password: ")
    userRecord = records.find_one({"_id":uid})
    if userRecord is not None:
        if userRecord["password"] == pwd:
            welcomeToInsta(uid)
        else:
            print("Invalid Credentials. Try Again")
    else:
        print("User does not exist")
    return()


initial()
