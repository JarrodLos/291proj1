import sqlite3
import time
import hashlib
import os
import sys
currUser = ""
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
		AND u.pwd LIKE :password;
        	'''
        #cursor.execute(' PRAGMA case_sensitive_like=true; ')
        #connection.commit()
        cursor.execute(CheckPwd, {"email":email, "password":password});
        
        Row2 = cursor.fetchone()
        #cursor.execute(' PRAGMA case_sensitive_like=true; ')
        #connection.commit()
        # Incorrect password
        if Row2 is None:
            return False
	# Correct Email & Password
        else:
            print("\nSigning in as " +  email + "...")
            print("\nWelcome back " + Row2[0] + "!") 
            return True


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

def createReview(rating, text, pid):
    global connection, cursor, currUser
    # Get the most recent review id (rid)
    newRID = '''
		SELECT MAX(rid)
		FROM previews;
        	'''
    cursor.execute(newRID)
    Row = cursor.fetchone()
    rid = Row[0] + 1 # Max + 1
    
    # Create the new review
    newReview = '''
		INSERT INTO previews(rid, pid, reviewer, rating, rtext, rdate)
		VALUES(:rid, :pid, :reviewer, :rating, :rtext, DATETIME('now'));
        	'''
    cursor.execute(newReview, {"rid":rid, "pid":pid, "reviewer":currUser, "rating":rating, "rtext":text})
    connection.commit()

def listReviews(pid):
    global connection, cursor
    # Get all the product reviews of PID
    retrieveReviews = '''
		SELECT rtext
		FROM previews
		WHERE pid = :pid;
        	'''
    cursor.execute(retrieveReviews, {"pid":pid})
    Row = cursor.fetchall()
    for i in range(0, len(Row)):
        print("Review #" + str(i + 1) + " " + Row[i][0])

def listSales(pid):
    global connection, cursor
    # Get all the product reviews of PID
    retrieveSales = '''
		SELECT rtext
		FROM sales s
		WHERE s.edate > DATETIME('now')
		ORDER BY (s.edate - DATETIME('now') ASC;
        	'''
    cursor.execute(retrieveReviews, {"pid":pid})
    Row = cursor.fetchall()
    for i in range(0, len(Row)):
        print("Review #" + str(i + 1) + " " + Row[i][0])

def listProducts(): # 1
    global connection, cursor, currUser
    print("\nRun the List Products")
    activeSales = '''
		SELECT DISTINCT p.pid, p.descr, COUNT(r.rating), AVG(r.rating), COUNT(s.sid)
		FROM products p,previews r, sales s
		WHERE s.edate > DATETIME('now')
		AND s.pid = p.pid
		AND s.pid = r.pid
		AND p.pid = r.pid
		ORDER BY COUNT(s.sid) DESC;
        	'''

    cursor.execute(activeSales);
        
    Row = cursor.fetchall()
    
    print("Index | PID |    Desc.    | R# |  AR  | #S")
    for i in range(0, len(Row)):
        print("  " + str(i) + "   | " + Row[i][0] + " | " + Row[i][1] + " | " + str(Row[i][2]) + "  |  " + str(Row[i][3]) + " | " + str(Row[i][4]))
    print("\nNOTE: R#: Number of ratings, AR: Avg Rating, #S: # of active sales!\n")
    print("Please enter the products index of interest")
    print("To go back to the main menu, enter '.back'\n")
    
    # Listen for user commands for the list of Products
    index = customIn()
    #while not (i > int(index)):
            #print("Please enter a valid product index!")
            #cmd = ""
            #cmd = customIn()

    if index.lower() == ".back":
        return
    else:
        print("\nTo write a review: 'a'")
        print("To list all reviews: 'b'")
        print("To list all active sales: 'c'\n")
        
        cmd = customIn()
        if cmd.lower() == "a": # Create a rating (Needs char limit)
            print("Creating a review for the selected product: " + Row[index][0])
            print("\nPlease enter your rating (1-5): ")
            rating = customIn()
            while (0 > int(rating)) or (int(rating) > 6):
                print("Please enter a rating between 1-5")
                rating = customIn()
            print("\nPlease enter your text (1-20 characters):\n")
            text = customIn()
            selectedPid = Row[int(index)][0]
            createReview(rating, text, selectedPid)
            print("Thank-you for your review!\n")
            return
        
        elif cmd.lower() == "b": # List all reviews
            print("\nListing all reviews for the selected product: " + Row[int(index)][0])
            selectedPid = Row[int(index)][0]
            listReviews(selectedPid)
        
        elif cmd.lower() == "c": # NOT DONE
            print("\nListing all active sales for the selected product: " + Row[int(index)][0])
            selectedPid = Row[int(index)][0]
            listSales(selectedPid)

        elif cmd.lower() == ".back":
            return

        else:
            print("That is an incorrect entry, please try again or enter 'menu' to go back to the main menu")
            return
        

def postSale(): # 2
    print("\nRun the Post a Sale")

def searchSale(): # 3
    print("\nRun the Search Sales")

def searchUser(): # 4
    print("\nRun the Search Users")

def followUp(): # 5
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

    selection = customIn()

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
    connection.commit()

    while(mainMenu()):
        pass

    connection.commit()
    connection.close()
