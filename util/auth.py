from flask import Flask
import sqlite3

def checkInfo(user,pswd):
    
    '''This function takes in two parameters (username, password) and checks the database for the params.
       If they are found, the function returns "Login Successful".
       If the username is found and the associated password doesn't match, it returns "Incorrect Password".
       If the username isn't found, it returns "User not found".'''
    
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    
    #Looks for the password of the inputted user
    for i in c.execute("SELECT pass FROM userInfo WHERE username = ?",(user,)):
    
         #If user is found and passwords match
        if i[0] == pswd: return "Login Successful"
    
         #If passwords don't match
        else: 
            db.close()
            return "Incorrect Password"
    
    else:
    
        #If the user doesn't exist in the table
        db.close()
        return "User not found"

def createAcc(user,pswd,passConf):
    
    '''This function takes in three parameters (username, password, password confirmation).
       If the username is found in the database, it returns "Username already exists.
       If the password and password confirmation aren't the same, it returns "Passwords do not match".
       Otherwise, it will add the username and password to the database and return "Account Creation Successful."'''
    
    db = sqlite3.connect("data/info.db")
    c = db.cursor()
    
    #checks if the username already exists
    for i in c.execute("SELECT username FROM userInfo WHERE username = ?",(user,)):
        db.close()
        return "Username already exists"
    
    else:
        #if password confirmation fails
        if pswd != passConf: 
            db.close()
            return "Passwords do not match"        
        
        #if password confirmation succeeds add the user to the database
        c.execute("INSERT INTO userInfo (username,pass) VALUES(?,?)",(user,pswd,))
        db.commit()
        db.close()
        return "Account creation successful"

print(createAcc("abc","123","123")) #expect account creation successful

