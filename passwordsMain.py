"""
file name: passwordsMain.py
version: 1.00.01
author: Tyler S. Budd
author GitHub: https://github.com/tsbudd
date created: 07/23/2022
last updated: 07/23/2022
description: uses MariaDB MySQL database to securely store passwords. If someone were to
            access the database without the program, they would only see gibberish passwords
library install requirements: pwinput, cryptocode, datetime, tabulate, and mysql.connector
"""
import os, time, pwinput, cryptocode
from datetime import datetime
from tabulate import tabulate
import mysql.connector as mysql

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class Passwords:
    def __init__(self):
        exitBool = 0
        self.key = None
        for x in range(5):
            # get username and password
            userN = input("\n\tENTER DATABASE USERNAME:\t")
            if userN == 'q': quit()
            passW = pwinput.pwinput("\tENTER DATABASE PASSWORD:\t")
            if passW == 'q': quit()


            try: # attempt sign in
                self.db = mysql.connect(
                    host = "localhost",
                    database = "passwords",
                    user = userN,
                    password = passW)
                print("\nACCESS GRANTED\n")
                exitBool = 0
                self.key = passW
                break
            except mysql.Error: # if username or password is incorrect
                clearTerminal()
                print("INCORRECT USERNAME OR PASSWORD - TRY AGAIN")
                exitBool = 1

        if exitBool == 1:
            for i in range(3, 0, -1):
                print("TOO MANY INCORRECT ATTEMPTS - PROGRAM WILL NOW TERMINATE IN %d SECONDS" % i, end="\r")
                time.sleep(1)
            clearTerminal()
            exit()

        self.cursor = self.db.cursor()
    
    def getPasswords(self):
        cursor = self.cursor
        resArr = []
        dateFormat = '%Y-%m-%d %H:%M:%S'

        #getting all passwords
        try:
            query = "select * from accounts order by acc_name"
            cursor.execute(query)
            result = cursor.fetchall()
        except mysql.Error as err:
            print("\tERROR - PASSWORD RETRIEVAL UNSUCCESSFUL:\t", err, "\n")

        # adding all passwords to returning list
        for item in result:
            acct = item[0]
            passW = cryptocode.decrypt(item[1], self.key)
            timestamp = datetime.strftime(item[2], dateFormat)

            resArr.append([acct, passW, timestamp])

        # print list of passwords
        print(tabulate(resArr, headers=["Account", "Password", "Last Updated"]))
        print()

        return resArr
        
    def newPassword(self):
        cursor = self.cursor
        db = self.db

        # getting account name
        acctName = input("\tNEW ACCOUNT NAME:\t")
        if acctName == 'q' : exit()

        # getting new password
        while(1):
            newPass = input("\n\tNEW PASSWORD FOR '%s':\t" % acctName)
            if newPass == 'q' : exit()
            newPassValidate = input("\tRE-TYPE NEW PASSWORD FOR '%s':\t" % acctName)
            if newPassValidate == 'q' : exit()
            if newPass != newPassValidate:
                clearTerminal()
                print("\tPASSWORDS DO NOT MATCH")
            else:
                break

        clearTerminal()

        # updating database
        try:
            query = "call newPass(%s, %s)"
            cursor.execute(query, (acctName, cryptocode.encrypt(newPass, self.key)))
            db.commit()

            print("NEW PASSWORD SUCCESSFUL\n")
        except mysql.Error as err:
            print("ERROR - NEW PASSWORD UNSUCCESSFUL: ", err, "\n")

        # display all passwords
        self.getPasswords()

    def updatePassword(self):
        cursor = self.cursor
        db = self.db

        # show all passwords
        clearTerminal()
        accounts = self.getPasswords()

        # picking account to update
        selAcct = None
        while(1):
            acctSel = input("\tWHICH ACCOUNT PASSWORD ARE YOU UPDATING?: ")
            if acctSel == 'q' : exit()
            for acct in accounts:
                if acctSel == acct[0]:
                    selAcct = acct

            if not selAcct:
                clearTerminal()
                accounts = self.getPasswords() 
                print("\tINVALID ENTRY")
            else:
                break

        # getting new password
        while(1):
            newPass = input("\n\tNEW PASSWORD FOR '%s':\t" % selAcct[0])
            if newPass == 'q' : exit()
            newPassValidate = input("\tRE-TYPE NEW PASSWORD FOR %s:\t" % selAcct[0])
            if newPassValidate == 'q' : exit()
            if newPass != newPassValidate:
                clearTerminal()
                accounts = self.getPasswords()
                print("\tPASSWORDS DO NOT MATCH")
            else:
                break

        clearTerminal()

        # updating database
        try:
            query = "call updatePass(%s, %s)"
            cursor.execute(query, (selAcct[0], cryptocode.encrypt(newPass, self.key)))
            db.commit()

            print("PASSWORD UPDATE SUCCESSFUL\n")
        except mysql.Error as err:
            print("ERROR - PASSWORD UPDATE UNSUCCESSFUL: ", err, "\n")

        # # display all passwords
        self.getPasswords()

    def deleteAccount(self):
        cursor = self.cursor
        db = self.db

        # show all passwords
        clearTerminal()
        accounts = self.getPasswords()

        selAcct = None
        while(1):
            acctSel = input("\tWHICH ACCOUNT ARE YOU DELETING?: ")
            if acctSel == 'q' : exit()
            for acct in accounts:
                if acctSel == acct[0]:
                    selAcct = acct

            if not selAcct:
                clearTerminal()
                accounts = self.getPasswords() 
                print("\tINVALID ENTRY")
            else:
                break

        # getting security validation
        while(1):
            veriPass = pwinput.pwinput("\n\tTO CONFIRM, INSERT SECURITY KEY (DATABASE PASSWORD):\t")
            if veriPass == 'q' : exit()
            if veriPass != self.key:
                clearTerminal()
                accounts = self.getPasswords()
                print("INCORRECT SECURITY KEY")
            else:
                break
        
        clearTerminal()

        # updating database
        try:
            query = "call deletePass(%s)"
            cursor.execute(query, [selAcct[0]])
            db.commit()

            print("PASSWORD DELETE SUCCESSFUL")
        except mysql.Error as err:
            print("ERROR - PASSWORD DELETE UNSUCCESSFUL: ", err, "\n")
        

        self.getPasswords()
        
commands = ["seePass", "newPass", "updatePass", "deletePass", "quit"]

# ------------------- MAIN -------------------
clearTerminal()
print("PROGRAM: Password Manager Ver 1.00.01")
print("AUTHOR: Tyler S. Budd")
print("SECURITY: all passwords are encrypted via CRYPTOCODE")
print("NOTE: you can input 'q' for any query, and the program will terminate")

# sign into database
database = Passwords()

while(1):
    print("SELECT COMMAND IN LIST :\n\t", commands, end=":\t")
    command = input()
    clearTerminal()
    print()
    if command == commands[0]:
        database.getPasswords()
    elif command == commands[1]:
        database.newPassword()
    elif command == commands[2]:
        database.updatePassword()
    elif command == commands[3]:
        database.deleteAccount()
    elif command == commands[4] or command == "q":
        clearTerminal()
        quit()
    else:
        clearTerminal()
        print("INVALID COMMAND")

database.cursor.close()
