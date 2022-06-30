from pickle import TRUE
from select import select
from venv import create
# from psycopg2 import cursor
import pymongo
import datetime
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId
from sqlalchemy import false, true

client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
collection = db.test_collection
posts = db.posts


#****************************************************************************************************
# Function Name:      createPost
# In:                 posts
# Out:                N/A
# In/Out:             N/A
# Returns:            N/A
# Description:        Creates a post consisting of a user first name, a user last name, a message 
#                       title, and a message, and writes it to the MongoDB, test_database.
#****************************************************************************************************

def createPost(posts):
  print("\nCreate Post")
  authorFirstName = input("Enter author first name: ")
  authorLastName =  input("Enter author last name: ")
  postTitle = input("Enter post title: ")
  postBody = input("Enter post body: ")
  post = {"author first name": authorFirstName, "author last name": authorLastName, "title": postTitle, "text": postBody, "date": datetime.datetime.utcnow()}
  print(post)
  print("Post successful!")


#****************************************************************************************************
# Function Name:      printReadPostSubMenu
# In:                 N/A
# Out:                N/A
# In/Out:             N/A
# Returns:            N/A
# Description:        Prints submenu.
#****************************************************************************************************

def printReadPostSubMenu():
  print("\nRead")
  print("1 - Read by author first name")
  print("2 - Read by author last name")
  print("3 - Read by post title")
  print("4 - Exit Read")


#****************************************************************************************************
# Function Name:      readPost
# In:                 posts
# Out:                N/A
# In/Out:             N/A
# Returns:            N/A
# Description:        Takes a collection, posts, finds posts by parameter, displays posts.
#****************************************************************************************************

def readPost(posts):
  printReadPostSubMenu()

  readChoice = input("Enter a selection: ")

  while readChoice != "4":
    if readChoice == "1":
      authorFirstName = input("Enter author first name: ")
      cursor = posts.find({"author first name": authorFirstName})
      temp = readPostDisplayResults(cursor, false)
      break
    elif readChoice == "2":
      authorLastName = input("Enter author last name: ")
      cursor = posts.find({"author last name": authorLastName})
      temp = readPostDisplayResults(cursor, false)
      break
    elif readChoice == "3":
      postTitle = input("Enter post title: ")
      cursor = posts.find({"title": postTitle})
      temp = readPostDisplayResults(cursor, false)
      break
    elif readChoice == "4":
      break
    else:
      break


#****************************************************************************************************
# Function Name:      readPostDisplayResults
# In:                 cursor, flag
# Out:                N/A
# In/Out:             N/A
# Returns:            selectedPosts, selectedPostIDs
# Description:        Retrieves queried data from MongoDB and displays to user.
#****************************************************************************************************

def readPostDisplayResults(cursor, flag):
  selectedPosts = []
  selectedPostIDs = []
  for post in cursor:
    selectedPosts.append(post)
    selectedPostIDs.append(post["_id"])
  if len(selectedPosts) > 1:
    viewPosts = ""
    while ((viewPosts != "Y") or (viewPosts != "n")):
      viewPosts = "n"
      viewPosts = input("Your query returned more than one post. Would you like to view the posts [Y/n]?")
      if viewPosts == "Y":
        for post in selectedPosts:
          print("\n")
          pprint.pprint(post)
          if flag == true:
            updatePost = ""
            while ((updatePost != "Y") or (updatePost != "n")):
              updatePost = input("Update this post [Y/n]?")
              if updatePost == "Y":
                updateByPostID(post, post["_id"])
      else:
        break
      break
    print("\n")
    for ID in selectedPostIDs:
      print(ID)
  else:
    pprint.pprint(selectedPosts)
  
  return([selectedPosts, selectedPostIDs])


#****************************************************************************************************
# Function Name:      updatePost
# In:                 posts
# Out:                N/A
# In/Out:             N/A
# Returns:            N/A
# Description:        Takes a collection, posts, finds posts by parameter, displays posts, requests
#                       user input regarding which post to update, updates or does not update a post
#                       based on input from the user.
#****************************************************************************************************
    
def updatePost(posts):
  print("\nUpdate")
  print("1 - Update by author first name")
  print("2 - Update by author last name")
  print("3 - Update by post title")
  print("4 - Exit Update")

  updateChoice = input("Enter a selection: ")
  
  while updateChoice != "4":
    if updateChoice == "1":
      authorFirstName = input("Enter author first name: ")
      cursor = posts.find({"author first name": authorFirstName})
      temp = readPostDisplayResults(cursor, true)
      break
    if updateChoice == "2":
      authorLastName = input("Enter author last name: ")
      cursor = posts.find({"author last name": authorLastName})
      temp = readPostDisplayResults(cursor, true)
      break
    if updateChoice == "3":
      postTitle = input("Enter post title: ")
      cursor = posts.find({"title": postTitle})
      temp = readPostDisplayResults(cursor, true)
      break
    elif updateChoice == "4":
      break


#****************************************************************************************************
# Function Name:      printUpdateByPostIDMenu
# In:                 N/A
# Out:                N/A
# In/Out:             N/A
# Returns:            N/A
# Description:        Prints submenu.
#****************************************************************************************************

def printUpdateByPostIDMenu():
  print("1 - Update author first name")
  print("2 - Update author last name")
  print("3 - Update post title")
  print("4 - Update post body")
  print("5 - Exit Update")
  
  
#****************************************************************************************************
# Function Name:      updatePost
# In:                 posts
# Out:                N/A
# In/Out:             N/A
# Returns:            N/A
# Description:        
#****************************************************************************************************

def updateByPostID(post, post_id):
  updatePost = ""
  while ((updatePost != "Y") or (updatePost != "n")):
    updatePost = "n"
    updatePost = input("Update this post [Y/n]? Default is [n].")
    if updatePost == "n":
      break
    else:
      printUpdateByPostIDMenu()
      
      selection = input("Enter a selection: ")
      
      while selection != "5":
        if selection == "1":
          authorFirstName = input("Enter new author first name: ")
          posts.update_one({"_id": post_id}, { "$set": {"author first name": authorFirstName}})
          post = posts.find_one({"_id": post_id})
          pprint.pprint(post)
          print("Update successful.")
          break
        elif selection == "2":
          authorLastName = input("Enter new author last name: ")
          posts.update_one({"_id": post_id}, { "$set": {"author last name": authorLastName}})
          post = posts.find_one({"_id": post_id})
          pprint.pprint(post)
          print("Update successful.")
          break
        elif selection == "3":
          postTitle = input("Enter new post title: ")
          posts.update_one({"_id": post_id}, { "$set": {"title": postTitle}})
          post = posts.find_one({"_id": post_id})
          pprint.pprint(post)
          print("Update successful.")
          break
        elif selection == "4":
          postBody = input("Enter new post body: ")
          posts.update_one({"_id": post_id}, { "$set": {"text": postBody}})
          post = posts.find_one({"_id": post_id})
          pprint.pprint(post)
          print("Update successful.")
          break
        elif selection == "5":
          break
      break
    break


#****************************************************************************************************
# Function Name:      updatePost
# In:                 posts
# Out:                N/A
# In/Out:             N/A
# Returns:            N/A
# Description:        Deletes a record from MongoDB based on user input.
#****************************************************************************************************

def deletePost(posts):
  print("\nDelete")
  print("1 - Delete by author first name")
  print("2 - Delete by author last name")
  print("3 - Delete by post title")
  print("4 - Exit Delete")

  readChoice = input("Enter a selection: ")
  
  while readChoice != "4":
    if readChoice == "1":
      authorFirstName = input("Enter author first name: ")
      post = posts.find({"author first name": authorFirstName})
      pprint.pprint(post[0])
      delete = "n"
      delete = input("Delete this post [Y/n]? ")
      if delete == "Y":
        posts.delete_one({"_id": post["_id"]})
      else:
        break
      break
    if readChoice == "2":
      authorLastName = input("Enter author last name: ")
      post = posts.find({"author last name": authorLastName})
      pprint.pprint(post[0])
      delete = "n"
      delete = input("Delete this post [Y/n]? ")
      if delete == "Y":
        posts.delete_one({"_id": post["_id"]})
      else:
        break
      break
    if readChoice == "3":
      postTitle = input("Enter post title: ")
      post = posts.find({"title": postTitle})
      pprint.pprint(post)
      delete = "n"
      delete = input("Delete this post [Y/n]? ")
      if delete == "Y":
        posts.delete_one({"_id": post["_id"]})
      break
    elif readChoice == "4":
      break


#****************************************************************************************************
# Function Name:      printDoStuffMainMenu
# In:                 N/A
# Out:                N/A
# In/Out:             N/A
# Returns:            N/A
# Description:        Prints submenu.
#****************************************************************************************************

def printDoStuffMainMenu():
  print("\nPlease make a selection from 1 to 5:")
  print("1 - Create Post")
  print("2 - Read Post")
  print("3 - Update Post")
  print("4 - Delete Post")
  print("5 - Exit")


#****************************************************************************************************
# Function Name:      doStuff
# In:                 db, collection, posts
# Out:                N/A
# In/Out:             N/A
# Returns:            N/A
# Description:        Primary logic control function for application.
#****************************************************************************************************

def doStuff(db, collection, posts):
  choice = "0"
  while choice != "5":
    printDoStuffMainMenu()    
    choice = input()
    if choice == "1":
      createPost(posts)
    elif choice == "2":
      readPost(posts)
    elif choice == "3":
      updatePost(posts)
    elif choice == "4":
      deletePost(posts)
    elif choice == "5":
      print("\nExit")
      dropDatabase = "n"
      dropDatabase = input("Drop database test_database [Y/n]? Default is [n].")
      if dropDatabase == "Y":
        client.drop_database('test_database')
      break

doStuff(db, collection, posts)