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
    print('Type ".logout" at any time to be taken back to the sign in screen.')
    print('Type ".quit" at any time to quit NorthSaskatchewan')
    print('\nTo login, type "login"\nTo create a new account, type "signup"')

# Our implementation of the input() function so that we can exit/logout at any time
def customIn(prompt = ""):
    myInput = input(prompt)

    if(myInput == ".quit"):
        exit()
    elif(myInput == ".logout"):
        restartProgram()
    else:
        return myInput

# Verifies that the email does not exist yet
def VerifyNew(email):
    global connection, cursor
    CheckEmail = '''
		SELECT name
		FROM users
		WHERE email = :email;
        	'''
    cursor.execute(CheckEmail, {"email":email});
    Row = cursor.fetchone()

    # Email does not exist
    if Row is None:
        return True
    return False

# Verifies an existing users email and password
def VerifyExisting(email, password):
    global connection, cursor
    CheckEmail = '''
		SELECT name
		FROM users
		WHERE email = :email;
        	'''
    cursor.execute(CheckEmail, {"email":email});
    Row1 = cursor.fetchone()
    # Email does not exist
    if Row1 is None:
        return False

    # Check the password!
    else:
        CheckPwd = '''
		SELECT name
		FROM users u
		WHERE u.email = :email
		AND u.pwd = :password;
        	'''
        cursor.execute(CheckPwd, {"email":email, "password":password});
        Row2 = cursor.fetchone()

        # Incorrect password
        if Row2 is None:
            return False
	# Correct Email & Password
        else:
            print("\nAccount Found!")
            print("Signing in as " +  email + "...")
            print("Welcome back " + Row2[0] + "!")
            return True

# Adds an email and password for a new user
def CheckAccount():
    print("\nLogin to an Existing Account")

    usr = input('\nEmail: ').lower()

    pwd = input('\nPassword: ').lower()

    if VerifyExisting(usr,pwd):

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

            if(VerifyNew(usr)): # Email does not exist, continue!
                break

            else:
                print("\nThat email is already in use! Please use a different address.")

        print("\nPassword:")
        pwd = customIn()

        print("\nName:")
        name = customIn()

        print("\nCity:")
        city = customIn()


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
    cursor.execute(newUser, {"email":usr, "name":name, "pwd":pwd, "city":city, "gender":gender})
    connection.commit()
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


def printActiveListings(user):

    # searchData = '''
    # SELECT s.descr, count(bid), max(amount), s.rprice, cast(julianday(s.edate)-julianday('now') as int)
    # FROM sales s left outer join bids b using(sid), users u
    # WHERE s.edate > datetime('now')
    # AND s.lister = u.email
    # AND u.email = ?
    # ORDER BY s.edate desc;
    # '''

    searchData = '''
    SELECT s.descr, count(bid), max(amount), s.rprice, cast(julianday(s.edate)-julianday('now') as int)
    FROM sales s, bids b, users u
    WHERE s.edate > datetime('now')
    AND s.lister = u.email
    AND u.email = ?
    ORDER BY s.edate desc;
    '''

    cursor.execute(searchData, (user,));
    allSearchResults = cursor.fetchall()

    if(len(allSearchResults) == 0):
        print("No active listings.")

    else:
        print("\nIndex: Description | Max Bid / Res Price | Time Remaining")
        for result in range(0, len(allSearchResults)):
            if(allSearchResults[result][1] == 0):
                maxBidResPrice = allSearchResults[result][3]
            else:
                maxBidResPrice = allSearchResults[result][2]

            print(str(result) + ": " + allSearchResults[result][0] + " | " + str(maxBidResPrice) + " | " + str(allSearchResults[result][4]))


def listProducts():
    print("\nRun the List Products")

def postSale():
    print("\nRun the Post a Sale")

def searchSale():
    print("\nRun the Search Sales")

def searchUser(): # NOT DONE
    print('\nSearch Users - Type ".back" to return to Main Menu.')
    backFlag = False # Is set to true if we are breaking out of the program

    allSearchResults = None

    while(True):
        search = customIn("\nSearch: ")

        # Handle a .back request
        if(search == ".back"):
            break

        searchData = '''
        SELECT email, name, city
        FROM users
        WHERE email LIKE ?
        OR name LIKE ?
        OR city LIKE ?;
        '''

        cursor.execute(searchData, ("%" + search + "%", "%" + search + "%", "%" + search + "%"));
        allSearchResults = cursor.fetchall()

        if(len(allSearchResults) == 0):
            print("No results found. Please try a simpler search.")

        else:
            print("\nIndex: Email   |   Name   |   City")
            for result in range(0, len(allSearchResults)):
                print(str(result) + ": " + allSearchResults[result][0] + " | " + allSearchResults[result][1] + " | " + allSearchResults[result][2])


            # While loop for error checking
            selection = ""
            while(True):
                selection = customIn("\nSelect a user (0-" + str(len(allSearchResults) - 1) +"): ")

                # Handle a .back request
                if(selection == ".back"):
                    backFlag = True
                    break

                elif(int(selection) < len(allSearchResults) and int(selection) >= 0):
                    break

                else:
                    print("Invalid entry, please enter a number between 0 and " + str(len(allSearchResults) - 1) + ".")

            # Handle a .back request
            if(backFlag):
                break


            fetchUser = '''
    		SELECT *
    		FROM users
    		WHERE email = ?;
        	'''

            cursor.execute(fetchUser, (allSearchResults[int(selection)][0],));
            selectedUser = cursor.fetchone()

            print("\nYou have selected " + selectedUser[1] + ".")
            print("1: Write a review for " + selectedUser[1])
            print("2: View " + selectedUser[1] + "'s active listings")
            print("3: View other's reviews of " + selectedUser[1])

            while(True):
                selection = customIn("\n(1-3): ")

                # Handle a .back request
                if(selection == ".back"):
                    backFlag = True
                    break

                elif(int(selection) > 0 and int(selection) <= 3):
                    break

                else:
                    print("\nInput not valid, please enter a number between 1 and 3.")

            # Handle a .back request
            if(backFlag):
                break

            if(selection == "1"): # NOT DONE
                print("Write Review")
            elif(selection == "2"): # NOT DONE (In progress)
                print("\n" + selectedUser[1] + "'s Active listings")

                printActiveListings(selectedUser[0])

            else: # NOT DONE
                print("View review")

            break # We are done with searching, break out to main menu.



def followUp():
    print("\nRun the Follow Up")


# Main menu
def mainMenu():
    print("\n--------------------------------")
    print('\nMain Menu - Type ".logout" to log out.')
    print("\n1: List Products")
    print("2: Post a Sale")
    print("3: Search Sales")
    print("4: Search Users")
    print("5: 1-2 Follow-Up\n")

    selection = customIn("(1-5): ")

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
        print("\nInput not recognized, please enter a number between 1 and 5.")

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

    connection.commit()

    while(mainMenu()):
        pass

    connection.commit()
    connection.close()
