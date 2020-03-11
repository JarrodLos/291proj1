import sqlite3
import time
import hashlib
import os
import sys

# Kills the program and starts it up again automatically
def restartProgram():
    connection.commit()
    connection.close()

    python = sys.executable
    os.execl(python, python, * sys.argv)

def getPath():
    directory = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(directory, str(sys.argv[1]))
    return path

def connect(path):
    global connection, cursor
    connection = None
    cursor = None
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

# Greeting
def init():
    global currUsr

    currUser = ""

    print("\n\nWelcome to NorthSaskatchewan (not afilliated with Amazon)")
    print('Type "logout" at any time to be taken back to the sign in screen.')
    print('Type "quit" at any time to quit NorthSaskatchewan')
    print('\nTo login, type "login"\nTo create a new account, type "signup"')

# Our implementation of the input() function so that we can exit/logout at any time
def customIn():
    myInput = input()

    if(myInput == "quit"):
        exit()
    elif(myInput == "logout"):
        restartProgram()
    else:
        return myInput

# Verifies that the email does not exist yet
def VerifyNew(email):
    return True # True or False

# Verifies an existing users email and password
def VerifyExisting(email, password):
    return True # True or False

# Adds an email and password for a new user
def CheckAccount():
    print("\nLogin to an Existing Account")

    usr = input('\nEmail: ').lower()

    pwd = input('\nPassword: ').lower()

    if VerifyExisting(usr,pwd):
        print("\nSign in successful!")

        # Set the current user
        currUser = usr

        return True

    else:
        print("\nYour login information was not found.")
        print('\nTo try again, type "login"\nTo create a new account, type "signup"')
        return False

# Returns boolean for new account creation
def CreateAccount():
    global connection, cursor, currUser

    # Flag so that the user can correct information if it was entered improperly
    ReadyToSignUp = False

    while(not ReadyToSignUp):
        print("\nCreate New Account")

        # Initialize the sign up variables
        usr = ""
        pwd = ""
        name = ""
        city = ""
        gender = ""

        # Loop keeps asking for a new email until a valid one is provided
        while(True):
            print("\nEmail:")
            usr = customIn().lower()

            ######## TODO Check to see if the email is already in the database ########

            if(False): # True if the email is in use.
                print("\nThat email is already in use! Please use a different address.")
            else:
                break

        print("\nPassword:")
        pwd = customIn()

        print("\nName:")
        name = customIn().lower()

        print("\nCity:")
        city = customIn().lower()

        # Loop keeps asking for a new gender until a valid one is provided
        while(True):
            print("\nGender (Male/Female/Other):")
            gender = customIn()

            if(gender.lower() == "male" or gender.lower() == "m"):
                gender = "M"
                break
            elif(gender.lower() == "female" or gender.lower() == "f"):
                gender = "F"
                break
            elif(gender.lower() == "other" or gender.lower() == "o"):
                gender = "O"
                break
            else:
                print('Please enter "Male, Female, or Other"')


        print("\nYou are creating an account with the credentials:")
        print("Email: " + usr)
        print("Password: " + pwd)
        print("Name: " + name)
        print("City: " + city)
        print("Gender: " + gender)

        # Loop keeps asking until the account info has been verified
        while(True):
            print("\nIs this information correct? (yes/no):")
            check = customIn()

            if(check.lower() == "yes" or check.lower() == "y"):
                ReadyToSignUp = True
                break
            elif(check.lower() == "no" or check.lower() == "n"):
                ReadyToSignUp = False
                print("\n") #Extra space for organization
                break
            else:
                print('Please enter "yes or no"')

    print("\nAccount Created!")

    print("Signing in as " + usr + "...")

    print("Welcome to NorthSaskatchewan, " + name + "!")

    # Set the current user
    currUser = usr

    newUser = '''
		INSERT INTO users(email, name, pwd, city, gender)
		VALUES(:email, :name, :pwd, :city, :gender);
        	'''
    # cursor.execute(newUser, {"email":usr, "name":name, "pwd":pwd, "city":city, "gender":gender})
    # connection.commit()
    return True

# Redirect to account creation or signing in
def checkSignInCmd():
    command = customIn()

    # User has an account and wants to log in
    if(command.lower() == "login" or command.lower() == "l"):
        return CheckAccount()

    # User wants to create an account
    elif(command.lower() == "signup" or command.lower() == "s"):
        return CreateAccount()

    # User didn't input a correct option
    else:
        print("Input not recognized, please try again")
        return False

def listProducts():
    print("\nRun the List Products")

def postSale():
    print("\nRun the Post a Sale")

def searchSale():
    print("\nRun the Search Sales")

def searchUser():
    print("\nRun the Search Users")

def followUp():
    print("\nRun the Follow Up")


# Main menu
def mainMenu():
    print("\n--------------------------------")
    print("\nMain Menu")
    print("\n1: List Products")
    print("2: Post a Sale")
    print("3: Search Sales")
    print("4: Search Users")
    print("5: 1-2 Follow-Up\n")

    print("(1-5): ")

    selection = customIn().lower()

    if(selection == "1"):
        print("\n--------------------------------")
        listProducts()

    elif(selection == "2"):
        print("\n--------------------------------")
        postSale()

    elif(selection == "3"):
        print("\n--------------------------------")
        searchSale()

    elif(selection == "4"):
        print("\n--------------------------------")
        searchUser()

    elif(selection == "5"):
        print("\n--------------------------------")
        followUp()

    else:
        print("\nInput not recognized, please try again")

    return True


if (__name__ == "__main__"):
    # Initialize and login
    global connection, cursor, currUser
    init()
    path = getPath()
    connect(path)

    # define_tables()
    # Inserting data from previously created table?

    # Keep trying until successful creation or login
    while(not checkSignInCmd()):
        pass


    while(mainMenu()):
        pass

    connection.commit()
    connection.close()
