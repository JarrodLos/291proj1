import sqlite3
import time
import hashlib
import os
import sys
import datetime

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
		SELECT pwd
		FROM users u
		WHERE u.email = :email;
        	'''
        #cursor.execute(' PRAGMA case_sensitive_like=true; ')
        #connection.commit()
        cursor.execute(CheckPwd, {"email":email});

        Row2 = cursor.fetchone()

        # Correct Email & Password
        print(str(Row2[0]) + "VS" + password)
        if str(Row2[0]) ==  password:
            print("\nAccount Found!")
            print("Signing in as " +  email + "...")
            print("Welcome back " + Row1[0] + "!")
            return True
	# Incorrect password
        else:
            return False

# Adds an email and password for a new user
def CheckAccount():
    global connection, cursor, currUser

    print("\nLogin to an Existing Account")

    usr = input('\nEmail: ').lower()

    pwd = input('\nPassword: ')

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


def viewReviews(user):
    searchData = '''
    SELECT reviewer, rating, rtext, rdate
    FROM reviews
    WHERE reviewee = ?;
    '''

    cursor.execute(searchData, (user,));
    allSearchResults = cursor.fetchall()

    if(len(allSearchResults) == 0):
        print(user + " has no reviews.")

    else:
        print("\nIndex: Reviewer | Rating | Comments | Date")
        for result in range(0, len(allSearchResults)):
            if(allSearchResults[result][2] == ""):
                comment = "(No Comment)"
            else:
                comment = allSearchResults[result][2]

            print(str(result) + ": " + allSearchResults[result][0] + " | " + str(allSearchResults[result][1]) + " | " + comment + " | " + str(allSearchResults[result][2]) + str(allSearchResults[result][3]))


def showActiveListingsListProduct(product):

    searchData = '''
    SELECT s.descr, count(bid), max(amount), s.rprice,
            CAST((strftime('%s',s.edate) - strftime('%s', 'now')) /86400 AS TEXT),
            CAST(((strftime('%s', s.edate) - strftime('%s', 'now')) % (86400)) / (3600) AS TEXT),
            CAST((((strftime('%s', s.edate) - strftime('%s', 'now')) % (86400)) % (3600)) / 60 AS TEXT),
            p.pid
    FROM sales s left outer join bids b using (sid), products p
    WHERE s.edate > datetime('now')
    AND s.pid = p.pid
    AND p.pid = ?
    GROUP BY s.sid
    ORDER BY s.edate;
    '''

    cursor.execute(searchData, (product,));
    allSearchResults = cursor.fetchall()

    if(len(allSearchResults) == 0):
        print("No active listings of this product.")

    else:
        print("\nIndex: Description | Max Bid / Res Price | Days/Hours/Minutes Remaining")
        for result in range(0, len(allSearchResults)):
            if(allSearchResults[result][2] == None):
                maxBidResPrice = allSearchResults[result][3]
            else:
                maxBidResPrice = allSearchResults[result][2]

            print(str(result) + ": " + allSearchResults[result][0] + " | " + str(maxBidResPrice) + " | " + str(allSearchResults[result][4]) + "days, " + str(allSearchResults[result][5]) + "hours, " + str(allSearchResults[result][6]) + "minutes")


    # Now continue on to show more information
    # While loop for error checking
    selection = ""
    while(True):
        selection = customIn("\nSelect a sale (0-" + str(len(allSearchResults) - 1) +"): ")

        if(int(selection) < len(allSearchResults) and int(selection) >= 0):
            break

        else:
            print("Invalid entry, please enter a number between 0 and " + str(len(allSearchResults) - 1) + ".")

    # Where I left off, may need some testing

    fetchSale = '''
    SELECT s.lister, count(r.rating), avg(r.rating), s.descr, s.edate, s.cond, max(amount), s.rprice, p.descr, count(pr.rating), avg(pr.rating)
    FROM (sales s left outer join bids b using (sid)) left outer join products p using (pid), reviews r, previews pr
    WHERE p.pid = ?
    AND s.lister = r.reviewee
    AND p.pid = pr.pid
    GROUP BY s.lister;
    '''

    cursor.execute(fetchSale, (allSearchResults[int(selection)][7],));
    selectedSale = cursor.fetchone()

    print("\nLister's Email: " + selectedSale[0])
    print("Lister's Raings: " + str(selectedSale[1]))
    print("Lister's Average Rating: " + str(selectedSale[2]))
    print("Sale's Description: " + selectedSale[3])
    print("Sale's End Date: " + str(selectedSale[4]))
    print("Sale's End Time: " + "-----TODO----")
    print("Product's Contioion: " + str(selectedSale[5]))

    if(selectedSale[6] == None):
        print("Max Bid: " + str(selectedSale[7]))
    else:
        print("Reserved Price: " + str(selectedSale[6]) + " (This listing has no bids!)")

    if(selectedSale[8] != None):
        print("Product's Description: " + selectedSale[8])

    if(selectedSale[9] != None):
        print("Product's Raings: " + str(selectedSale[9]))
        print("Product's Average Rating: " + str(selectedSale[10]))
    else:
        print("This product has not yet been reviewed.")

    # More information shown! Now show what you can do with the sale
    print("\n1: Place a bid on " + selectedSale[3])
    print("2: View " + selectedSale[0] + "'s other active listings")
    print("3: View other's reviews of " + selectedSale[0])

    while(True):
        selection = customIn("\n(1-3): ")

        # Handle a .back request
        if(selection == ".back"):
            backFlag = True
            break

        elif(int(selection) > 0 and int(selection) <= 3):
            break

        else:
            print("Input not valid, please enter a number between 1 and 3.")

    if(selection == "1"): # TODO
        print("#####################Place Bid#####################")
    elif(selection == "2"):
        # Call this function again
        print("\n" + selectedSale[0] + "'s active listings")

        showActiveListings(selectedSale[0])
    else:
        viewReviews(selectedSale[0])


def showActiveListings(user):

    searchData = '''
    SELECT s.descr, count(bid), max(amount), s.rprice,
            CAST((strftime('%s',s.edate) - strftime('%s', 'now')) /86400 AS TEXT),
            CAST(((strftime('%s', s.edate) - strftime('%s', 'now')) % (86400)) / (3600) AS TEXT),
            CAST((((strftime('%s', s.edate) - strftime('%s', 'now')) % (86400)) % (3600)) / 60 AS TEXT),
            s.sid
    FROM sales s left outer join bids b using (sid), users u
    WHERE s.edate > datetime('now')
    AND s.lister = u.email
    AND u.email = ?
    GROUP BY s.sid
    ORDER BY s.edate;
    '''

    cursor.execute(searchData, (user,));
    allSearchResults = cursor.fetchall()

    if(len(allSearchResults) == 0):
        print("This user has no active listings.")

    else:
        print("\nIndex: Description | Max Bid / Res Price | Days/Hours/Minutes Remaining")
        for result in range(0, len(allSearchResults)):
            if(allSearchResults[result][2] == None):
                maxBidResPrice = allSearchResults[result][3]
            else:
                maxBidResPrice = allSearchResults[result][2]

            print(str(result) + ": " + allSearchResults[result][0] + " | " + str(maxBidResPrice) + " | " + str(allSearchResults[result][4]) + "days, " + str(allSearchResults[result][5]) + "hours, " + str(allSearchResults[result][6]) + "minutes")


        # Now continue on to show more information
        # While loop for error checking
        selection = ""
        while(True):
            selection = customIn("\nSelect a sale (0-" + str(len(allSearchResults) - 1) +"): ")

            if(int(selection) < len(allSearchResults) and int(selection) >= 0):
                break

            else:
                print("Invalid entry, please enter a number between 0 and " + str(len(allSearchResults) - 1) + ".")

        fetchSale = '''
        SELECT s.lister, count(r.rating), avg(r.rating), s.descr, s.edate, s.cond, max(amount), s.rprice, p.descr, count(pr.rating), avg(pr.rating)
        FROM (sales s left outer join bids b using (sid)) left outer join products p using (pid), reviews r, previews pr
        WHERE s.sid = ?
        AND s.lister = r.reviewee
        AND p.pid = pr.pid
        GROUP BY s.lister;
        '''

        cursor.execute(fetchSale, (allSearchResults[int(selection)][7],));
        selectedSale = cursor.fetchone()

        print("\nLister's Email: " + selectedSale[0])
        print("Lister's Raings: " + str(selectedSale[1]))
        print("Lister's Average Rating: " + str(selectedSale[2]))
        print("Sale's Description: " + selectedSale[3])
        print("Sale's End Date: " + str(selectedSale[4]))
        print("Sale's End Time: " + "-----TODO----")
        print("Product's Contioion: " + str(selectedSale[5]))

        if(selectedSale[6] == None):
            print("Max Bid: " + str(selectedSale[7]))
        else:
            print("Reserved Price: " + str(selectedSale[6]) + " (This listing has no bids!)")

        if(selectedSale[8] != None):
            print("Product's Description: " + selectedSale[8])

        if(selectedSale[9] != None):
            print("Product's Raings: " + str(selectedSale[9]))
            print("Product's Average Rating: " + str(selectedSale[10]))
        else:
            print("This product has not yet been reviewed.")

        # More information shown! Now show what you can do with the sale
        print("\n1: Place a bid on " + selectedSale[3])
        print("2: View " + selectedSale[0] + "'s other active listings")
        print("3: View other's reviews of " + selectedSale[0])

        while(True):
            selection = customIn("\n(1-3): ")

            # Handle a .back request
            if(selection == ".back"):
                backFlag = True
                break

            elif(int(selection) > 0 and int(selection) <= 3):
                break

            else:
                print("Input not valid, please enter a number between 1 and 3.")

        if(selection == "1"): # TODO
            print("#####################Place Bid#####################")
        elif(selection == "2"):
            # Call this function again
            print("\n" + selectedSale[0] + "'s active listings")

            showActiveListings(selectedSale[0])
        else:
            viewReviews(selectedSale[0])


def createProdReview(rating, text, pid):
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


def createSellerReview(rating, text, email):
    global connection, cursor, currUser

    # Create the new review
    newReview = '''
		INSERT INTO reviews(reviewer, reviewee, rating, rtext, rdate)
		VALUES(?, ?, ?, ?, DATETIME('now'));
        	'''
    cursor.execute(newReview, (currUser, email, rating, text))
    connection.commit()

def createSale(edate, descr, cond, rprice, pid):
    global connection, cursor, currUser

    # Get a unique sid
    allSids = '''
    SELECT sid
    FROM sales;
    '''

    cursor.execute(allSids);
    allSidsFound = cursor.fetchall()

    if(len(allSidsFound) == 0):
        sid = "S00"
    else:
        allSidsFoundStripped = [len(allSidsFound)]

        for sid in range(0, len(allSidsFound)):
            allSidsFoundStripped[0] = int(allSidsFound[sid][0].strip("S"))
    maxSid = str(max(allSidsFoundStripped) + 1)
    if len(maxSid) == 1:
        sid = "S" + "0" + maxSid
    else:
        sid = "S" + maxSid

    # Check for no input on pid & rprice
    if len(pid) == 0:
        pid = None
    if len(rprice) == 0:
        rprice = None
    
    # Create the new sale
    newReview = '''
		INSERT INTO sales(sid, lister, pid, edate, descr, cond, rprice)
		VALUES(:sid, :lister, :pid, :edate, :descr, :cond, :rprice);
        	'''
    cursor.execute(newReview, {"sid":sid, "lister":currUser, "pid":pid, "edate":edate, "descr":descr, "cond":cond, "rprice":rprice})
    print("Your sale has been created! Please use sale ID " + sid + " to find your sale")
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


def listSales(pid): # Possibly depreciated
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

def getcurrentDate():
    # Get the current date

    now = datetime.datetime.now()
    unparsedDate = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Parse into the date and time respectively
    Parse = unparsedDate.split(" ")       
    # Parse and check the date (0th index - year | 1st index - month | 2nd index - day)
    date = Parse[0]
    dateP = date.split("-")
            
    # Parse and check the time (0th index - hour | 1st index - min | 2nd index - sec)
    time = Parse[1]
    timeP = time.split(":")

    # Return the parsed input as year, month, day, hour, minute and second
    currDate = ["" for i in range(0,6)]
    for i in range(0, 3):
        currDate[i] = int(dateP[i])
    for j in range(0, 3):
        currDate[3 + j] = int(timeP[j])
    return currDate

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
            print("\nCreating a review for the selected product: " + Row[int(index)][0])
            print("\nPlease enter your rating (1-5): ")
            rating = customIn()
            while (0 >= int(rating)) or (int(rating) >= 6):
                print("\nPlease enter a rating between 1-5")
                rating = customIn()
            print("\nPlease enter your text (1-20 characters):")
            text = customIn()
            selectedPid = Row[int(index)][0]
            createProdReview(rating, text, selectedPid)
            print("\nThank-you for your review!")

            return

        elif cmd.lower() == "b": # List all reviews
            print("\nListing all reviews for the selected product: " + Row[int(index)][0])
            selectedPid = Row[int(index)][0]
            listReviews(selectedPid)

        elif cmd.lower() == "c": # NOT DONE
            print("\nListing all active sales for the selected product: " + Row[int(index)][0])
            selectedPid = Row[int(index)][0]
            showActiveListingsListProduct(selectedPid)
            # listSales(selectedPid)

        elif cmd.lower() == ".back":
            return

        else:
            print("That is an incorrect entry, please try again or enter 'menu' to go back to the main menu")
            return


def postSale(): # 2
    print("\nCreating a new sale!")
    # sid (Gen), lister (currUser), pid (optional), edate * (Future), descr, cond, rprice(Optional)
    
    print("\nPlease enter the sales end date: (yyyy-MM-dd HH:mm:ss)") # Date
    
    # Gets the current date to compare with the sales end date 
    currDate = None
    currDate = getcurrentDate()    

    while True:
        edate = customIn() # edate[4/7] = "-", edate[10/16] = ":"
        if (len(edate) == 19 and edate[4] == edate[7] and edate[10] == " " and edate[13] == edate[16]):

            # Split the entry into its respective date and time
            Parse = edate.split(" ")
            date = Parse[0]
            time = Parse[1]

            # Parse and check the date (0th index - year | 1st index - month | 2nd index - day)
            # Parse and check the time (0th index - hour | 1st index - min | 2nd index - sec)
            dateP = date.split("-")
            timeP = time.split(":")
            if int(dateP[0]) > currDate[0]: # Year > current Year
                break
            elif int(dateP[0]) == currDate[0]: # Year = current Year
                
                if int(dateP[1]) > currDate[1]: # Month > current Month
                    break
                elif int(dateP[1]) == currDate[1]: # Month = current Month
                    
                    if int(dateP[2]) > currDate[2]: # Day > current Day
                        break
                    elif int(dateP[2]) == currDate[2]: # Day = current Day
                        print(timeP[0] + "VS" + str(currDate[3]))
                        if int(timeP[0]) > currDate[3]: # Hour > current Hour
                            break
                        elif int(timeP[0]) == currDate[3]: # Hour = current Hour
                            print(timeP[1] + "VS" + str(currDate[4]))
                            if int(timeP[1]) > currDate[4]: # Minute > current Minute
                                break
        print("\nPlease enter a valid date in the future in the following format: yyyy-MM-dd HH:mm:ss")

    print("\nPlease enter the sales description: ") # desc
    while True:
        descr = customIn()
        if 20 >= len(descr) > 0:
            break
        print("\nPlease enter a valid description between 1-20 chars!")

    print("\nPlease enter the products condition: ") # cond
    while True:    
        cond = customIn()
        if 10 >= len(cond) > 0:
            break
        print("\nPlease enter a valid condition between 1-10 chars!")

    print("\n(Optional) Please enter the reserved price: ") # rprice
    rprice = customIn()

    print("\n(Optional) Please enter the product ID: ") # pid
    pid = customIn()

    createSale(edate, descr, cond, rprice, pid)

def searchSale(): # 3
    print("\nRun the Search Sales")

def searchUser(): # 4 - IN PROGRESS

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

            if(selection == "1"): # IN PROGHRESS
                # print("#####################Write Review#####################")
                print("Creating a review for " + selectedUser[1])
                print("\nPlease enter your rating")
                rating = customIn("\n(1-5): ")
                while (0 > int(rating)) or (int(rating) > 6):
                    print("Please enter a rating between 1-5")
                    rating = customIn("\n(1-5): ")
                print("\nPlease enter a comment")
                text = customIn("\n(1-20 characters): ")

                createSellerReview(rating, text, selectedUser[0])
                print("\nThank you for your review!")

            elif(selection == "2"):
                print("\n" + selectedUser[1] + "'s active listings")

                showActiveListings(selectedUser[0])

            else: # NOT DONE
                viewReviews(selectedUser[0])

            # We are done with searching, break out to main menu.
            break

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

            if(selection == "1"): # Write a user review
                print("Creating a review for the selected user: " + selectedUser[1])
                print("\nPlease enter your rating (1-5): ")
                rating = customIn()
                while (0 >= int(rating)) or (int(rating) >= 6):
                    print("\nPlease enter a rating between 1-5")
                    rating = customIn()
                print("\nPlease enter your text (1-20 characters):\n")
                text = customIn()
                email = selectedUser[0]
                createSellerReview(rating, text, email)
                print("\nThank-you for your review!")
                return

            elif(selection == "2"): # NOT DONE (In progress)
                print("\n" + selectedUser[1] + "'s Active listings")

                printActiveListings(selectedUser[0])

            else: # NOT DONE
                print("View review")

            break # We are done with searching, break out to main menu.

# Main menu
def mainMenu():
    print("\n--------------------------------")
    print('\nMain Menu - Type ".logout" to log out.')
    print("\n1: List Products")
    print("2: Post a Sale")
    print("3: Search Sales")
    print("4: Search Users\n")

    selection = customIn("(1-4): ")

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

    else:
        print("\nInput not recognized, please enter a number between 1 and 4.")

    return True


if (__name__ == "__main__"):
    # Initialize and login
    global connection, cursor, currUser
    currUser = None
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
