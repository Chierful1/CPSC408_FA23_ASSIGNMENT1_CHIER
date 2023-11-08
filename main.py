"""
Eric Chier
2369498
echier@chapman.edu
CPSC-408-02
Assignment 1
"""
"""
A python program which connects to a student SQLite database and provides the user with a variety of functions to
view and edit said database.
"""
import sqlite3
import csv

# Connect to the database and make a cursor
conn = sqlite3.connect('./StudentDB.db')
mycursor = conn.cursor()

# Deletes and re-creates the Student table, giving a "clean slate"
def cleanslate():
    mycursor.execute("DROP TABLE Student")
    mycursor.execute("CREATE TABLE Student ("
                     "StudentId INTEGER PRIMARY KEY,"
                     "FirstName TEXT,"
                     "LastName TEXT,"
                     "GPA REAL,"
                     "Major TEXT,"
                     "FacultyAdvisor TEXT,"
                     "Address TEXT,"
                     "City TEXT,"
                     "State TEXT,"
                     "ZipCode TEXT,"
                     "MobilePhoneNumber TEXT,"
                     "isDeleted INTEGER DEFAULT 0"
                     "                );")


# The definition of the student object which is used for the add student functionality
class Student:
    FirstName = ''
    LastName = ''
    GPA = 0.0
    Major = ''
    FacultyAdvisor = ''
    Address = ''
    City = ''
    State = ''
    ZipCode = ''
    MobilePhoneNumber = ''


# A list of "advisors" who are just celebrity chefs
advisors = ('Robert Irvine', 'Gordan Ramsay', 'Bobby Flay', 'Guy Fieri', 'Brian Tsao')
# Imports the data from students.csv to the Student table
def import_data():
    randomizer = 0
    with open('./students.csv', 'r') as csvfile:
        buffer = csv.DictReader(csvfile)
        for row in buffer:
            # mycursor.execute("INSERT INTO Person('first_name','last_name','email','phone_number', 'job', 'company', 'date_of_birth', 'ssn', 'credit_card_number') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (row['first_name'], row['last_name'], row['email'], row['phone_number'], row['job'], row['company'], row['date_of_birth'], row['ssn'], row['credit_card_number'],))
            mycursor.execute(
                "INSERT INTO Student('FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber') VALUES (?,?,?,?,?,?,?,?,?,?)",
                (row['FirstName'], row['LastName'], row['GPA'], row['Major'], advisors[randomizer % 5], row['Address'], row['City'], row['State'], row['ZipCode'], row['MobilePhoneNumber'],))
            randomizer += 1
        conn.commit()
        return 0


# Displays all students who are not deleted
def display_allstudents():
    mycursor.execute(
        "SELECT StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student "
        "WHERE isDeleted < 1")
    rows = mycursor.fetchall()
    for row in rows:
        print(row)
    return 0


# Takes in a Student object and adds it to the Student table
def add_student(inStudent):
    mycursor.execute(
        "INSERT INTO Student('FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNumber') VALUES (?,?,?,?,?,?,?,?,?,?)",
        (inStudent.FirstName, inStudent.LastName, inStudent.GPA, inStudent.Major, inStudent.FacultyAdvisor, inStudent.Address, inStudent.City, inStudent.State, inStudent.ZipCode, inStudent.MobilePhoneNumber,))
    conn.commit()
    return 0


# Checks the Student table for whether a certain ID is present and not deleted, returning a boolean of if the student exists
def check_student(checkId):
    mycursor.execute(
        "SELECT StudentId FROM Student "
        "WHERE StudentId == ? AND isDeleted < 1", (checkId,))
    rows = mycursor.fetchall()
    if (rows == []):
        return False
    else:
        return True


# Functionally identical to check_student, but includes deleted student records
def check_all(checkId):
    mycursor.execute(
        "SELECT StudentId FROM Student "
        "WHERE StudentId == ?", (checkId,))
    rows = mycursor.fetchall()
    if (rows == []):
        return False
    else:
        return True


# Takes in a student ID and updates the Student table so that the record associated with that ID has its isDeleted value set to 1
def delete_student(gallowsId):
    gallowsId = int(gallowsId)
    mycursor.execute(
        "UPDATE Student SET isDeleted = 1 WHERE StudentId = ? AND isDeleted < 1", (gallowsId,))
    conn.commit()
    return 0


# Takes in a student ID and updates the Student table so that the record associated with that ID has its isDeleted value set to 0
def recover_student(revivalId):
    revivalId = int(revivalId)
    mycursor.execute(
        "UPDATE Student SET isDeleted = 0 WHERE StudentId = ?", (revivalId,))
    conn.commit()
    return 0


# Searches and prints all students with majors containing the inputMajor value passed in
def searchby_Major(inputMajor):
    likeWrapper = '%' + inputMajor + '%'
    # print(inputMajor)
    mycursor.execute(
        "SELECT StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student "
        "WHERE Major LIKE ? AND isDeleted < 1", (likeWrapper,))
    rows = mycursor.fetchall()
    if (rows == []):
        print('No students found with ' + inputMajor + ' as their major')
        return -1
    else:
        for row in rows:
            print(row)
        return 0


# Searches and prints all students with GPAs containing the inputGPA value passed in
def searchby_GPA(inputGPA):
    likeWrapper = '%' + inputGPA + '%'
    mycursor.execute(
        "SELECT StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student "
        "WHERE GPA LIKE ? AND isDeleted < 1", (likeWrapper,))
    rows = mycursor.fetchall()
    if (rows == []):
        print('No students found with a ' + inputGPA + ' GPA')
        return -1
    else:
        for row in rows:
            print(row)
        return 0


# Searches and prints all students with cities containing the inputCity value passed in
def searchby_City(inputCity):
    likeWrapper = '%' + inputCity + '%'
    mycursor.execute(
        "SELECT StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student "
        "WHERE City LIKE ? AND isDeleted < 1", (likeWrapper,))
    rows = mycursor.fetchall()
    if (rows == []):
        print('No students found from ' + inputCity)
        return -1
    else:
        for row in rows:
            print(row)
        return 0


# Searches and prints all students with states containing the inputState value passed in
def searchby_State(inputState):
    likeWrapper = '%' + inputState + '%'
    mycursor.execute(
        "SELECT StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student "
        "WHERE State LIKE ? AND isDeleted < 1", (likeWrapper,))
    rows = mycursor.fetchall()
    if (rows == []):
        print('No students found from ' + inputState)
        return -1
    else:
        for row in rows:
            print(row)
        return 0


# Searches and prints all students with faculty advisors containing the inputAdvisor value passed in
def searchby_Advisor(inputAdvisor):
    likeWrapper = '%' + inputAdvisor + '%'
    mycursor.execute(
        "SELECT StudentId, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student "
        "WHERE FacultyAdvisor LIKE ? AND isDeleted < 1", (likeWrapper,))
    rows = mycursor.fetchall()
    if (rows == []):
        print('No students found with ' + inputAdvisor + ' as their advisor')
        return -1
    else:
        for row in rows:
            print(row)
        return 0


# Updates the record in the Student table with the sId StudentId so that their major becomes the newMajor value passed in
def update_Major(sId, newMajor):
    if (check_student(sId)):
        mycursor.execute(
            "UPDATE Student SET Major = ? WHERE StudentId = ? AND isDeleted < 1", (newMajor, sId))
        conn.commit()
        # print('Student major updated')
        return 0
    else:
        print('No student found with the student ID ' + str(sId))
        print('This shouldn\'t be possible to get to but I believe in miracles')
        return -1


# Updates the record in the Student table with the sId StudentId so that their faculty advisor becomes the newAdvisor value passed in
def update_Advisor(sId, newAdvisor):
    if (check_student(sId)):
        mycursor.execute(
            "UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ? AND isDeleted < 1", (newAdvisor, sId))
        conn.commit()
        # print('Student advisor updated')
        return 0
    else:
        print('No student found with the student ID ' + str(sId))
        print('This shouldn\'t be possible to get to but I believe in miracles')
        return -1


# Updates the record in the Student table with the sId StudentId so that their mobile phone number becomes the newMobilePhoneNumber value passed in
def update_MobilePhoneNumber(sId, newMobilePhoneNumber):
    if (check_student(sId)):
        mycursor.execute(
            "UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ? AND isDeleted < 1", (newMobilePhoneNumber, sId))
        conn.commit()
        # print('Student phone number updated')
        return 0
    else:
        print('No student found with the student ID ' + str(sId))
        print('This shouldn\'t be possible to get to but I believe in miracles')
        return -1


# The main body of the program. The program is split into pages with prompts within, detailed as they come.
stillRunning = True
while stillRunning:
    goBack = False
    print("\n***MAIN MENU***\nOptions:\n<1> Import Students from CSV file\n<2> Display All Students\n<3> Add New Student\n<4> Update Student Information\n<5> Delete or Restore Student Record\n<6> Search for Students\n<QUIT> Quit Program")
    buffer = input("Enter the term within the <> brackets to select that option: ")
    buffer = buffer.lower()

    # Quits the program entirely
    if (buffer == 'quit'):
        stillRunning = False

    # The import students menu, containing options to either import students.csv to a blank Student table or add them
    # to the existing Student table.
    elif (buffer == '1'):
        while (not goBack):
            print('\n***IMPORT STUDENTS***\nThis version does not support custom CSV files. Would you like to begin the Student table from <scratch> or <add> students.csv to existing table?')
            buffer = input("Enter the term within the <> brackets to select that option, or enter <back> to exit to main menu: ")
            buffer = buffer.lower()
            if (buffer == 'back'):
                goBack = True
            elif (buffer == 'scratch'):
                cleanslate()
                import_data()
                print('Student table successfully started from scratch')
                input('Press enter to continue')
                goBack = True
            elif (buffer == 'add'):
                import_data()
                print('CSV file students.csv successfully added to Student table')
                input('Press enter to continue')
                goBack = True
            else:
                print('Input not recognized, please try again')
                input('Press enter to continue')

    # The display all students menu. Not particularly complex, as it just calls the display_allstudents() method.
    elif (buffer == '2'):
        print('\n***DISPLAY ALL STUDENTS***')
        display_allstudents()
        input('Press enter to continue')

    # The ugly duckling. The add new student record menu. Although ugly as sin, it is functionally very linear, just
    # allowing the user to move forward or backward through the creation of a Student object, checking input values all
    # the way, and finally feeds the Student object into the add_student() method.
    elif (buffer == '3'):
        tempStudent = Student()
        while (not goBack):
            gettingLastName = True
            print('\n***ADD NEW STUDENT***')
            buffer = input("Enter the first name of the new student record you would like to create, or enter <back> to exit to main menu: ")
            if (buffer.lower() == 'back'):
                goBack = True
            elif (all(x.isalpha() or x.isspace() or x == '\'' or x == '-' for x in buffer)):
                tempStudent.FirstName = buffer
                while (gettingLastName):
                    gettingGPA = True
                    print('\n***ADD NEW STUDENT***')
                    buffer = input("Enter the last name of the new student record you would like to create, or enter <back> to return to first name input: ")
                    if (buffer.lower() == 'back'):
                        gettingLastName = False
                    elif (all(x.isalpha() or x.isspace() or x == '\'' or x == '-' for x in buffer)):
                        tempStudent.LastName = buffer
                        while (gettingGPA):
                            gettingMajor = True
                            print('\n***ADD NEW STUDENT***')
                            buffer = input(
                                "Enter the GPA of the new student record you would like to create, or enter <back> to return to last name input: ")
                            if (buffer.lower() == 'back'):
                                gettingGPA = False
                            elif (buffer.count('.') == 1 and all(x.isdigit() or x == '.' for x in buffer)):
                                tempStudent.GPA = buffer
                                while (gettingMajor):
                                    gettingFacultyAdvisor = True
                                    print('\n***ADD NEW STUDENT***')
                                    buffer = input("Enter the major of the new student record you would like to create, or enter <back> to return to GPA input: ")
                                    if (buffer.lower() == 'back'):
                                        gettingMajor = False
                                    elif (all(x.isalpha() or x.isspace() for x in buffer)):
                                        tempStudent.Major = buffer
                                        while (gettingFacultyAdvisor):
                                            gettingAddress = True
                                            print('\n***ADD NEW STUDENT***')
                                            buffer = input("Enter the faculty advisor of the new student record you would like to create, or enter <back> to return to major input: ")
                                            if (buffer.lower() == 'back'):
                                                gettingFacultyAdvisor = False
                                            elif (all(x.isalpha() or x.isspace() or x == '\'' or x == '-' for x in buffer)):
                                                tempStudent.FacultyAdvisor = buffer
                                                while (gettingAddress):
                                                    gettingCity = True
                                                    print('\n***ADD NEW STUDENT***')
                                                    buffer = input("Enter the address of the new student record you would like to create, or enter <back> to return to faculty advisor input: ")
                                                    if (buffer.lower() == 'back'):
                                                        gettingAddress = False
                                                    elif (all(x.isalpha() or x.isspace() or x.isdigit() or x == '\'' or x == '-' for x in buffer)):
                                                        tempStudent.Address = buffer
                                                        while (gettingCity):
                                                            gettingState = True
                                                            print('\n***ADD NEW STUDENT***')
                                                            buffer = input("Enter the city of the new student record you would like to create, or enter <back> to return to address input: ")
                                                            if (buffer.lower() == 'back'):
                                                                gettingCity = False
                                                            elif (all(x.isalpha() or x.isspace() or x == '\'' or x == '-' for x in buffer)):
                                                                tempStudent.City = buffer
                                                                while (gettingState):
                                                                    gettingZipCode = True
                                                                    print('\n***ADD NEW STUDENT***')
                                                                    buffer = input("Enter the state of the new student record you would like to create, or enter <back> to return to city input: ")
                                                                    if (buffer.lower() == 'back'):
                                                                        gettingState = False
                                                                    elif (all(x.isalpha() or x.isspace() or x == '\'' or x == '-' for x in buffer)):
                                                                        tempStudent.State = buffer
                                                                        while (gettingZipCode):
                                                                            gettingMobilePhoneNumber = True
                                                                            print('\n***ADD NEW STUDENT***')
                                                                            buffer = input("Enter the zip code of the new student record you would like to create, or enter <back> to return to state input: ")
                                                                            if (buffer.lower() == 'back'):
                                                                                gettingZipCode = False
                                                                            elif (buffer.isdigit() and len(buffer) > 3 and len(buffer) < 6):
                                                                                tempStudent.ZipCode = buffer
                                                                                while (gettingMobilePhoneNumber):
                                                                                    print('\n***ADD NEW STUDENT***')
                                                                                    buffer = input("Enter the mobile phone number of the new student record you would like to create, or enter <back> to return to zip code input: ")
                                                                                    if (buffer.lower() == 'back'):
                                                                                        gettingMobilePhoneNumber = False
                                                                                    elif (all(x == 'x' or not x.isalpha() for x in buffer)):
                                                                                        tempStudent.MobilePhoneNumber = buffer
                                                                                        if (add_student(tempStudent) == 0):
                                                                                            print('Student record successfully added')
                                                                                            input('Press enter to continue')
                                                                                        else:
                                                                                            print('Sorry pal, something went real wrong')
                                                                                            input('Press enter to continue')
                                                                                        gettingMobilePhoneNumber = False
                                                                                        gettingZipCode = False
                                                                                        gettingState = False
                                                                                        gettingCity = False
                                                                                        gettingAddress = False
                                                                                        gettingFacultyAdvisor = False
                                                                                        gettingMajor = False
                                                                                        gettingGPA = False
                                                                                        gettingLastName = False
                                                                                        goBack = True
                                                                                    else:
                                                                                        print('Input is not a valid mobile phone number, please try again')
                                                                                        input('Press enter to continue')
                                                                            else:
                                                                                print('Input is not a valid zip code, please try again')
                                                                                input('Press enter to continue')
                                                                    else:
                                                                        print('Input is not a valid state, please try again')
                                                                        input('Press enter to continue')
                                                            else:
                                                                print('Input is not a valid city, please try again')
                                                                input('Press enter to continue')
                                                    else:
                                                        print('Input is not a valid address, please try again')
                                                        input('Press enter to continue')
                                            else:
                                                print('Input is not a valid faculty advisor, please try again')
                                                input('Press enter to continue')
                                    else:
                                        print('Input is not a valid student major, please try again')
                                        input('Press enter to continue')
                            else:
                                print('Input is not a valid student GPA, please try again')
                                input('Press enter to continue')
                    else:
                        print('Input is not a valid student last name, please try again')
                        input('Press enter to continue')
            else:
                print('Input is not a valid student first name, please try again')
                input('Press enter to continue')

    # The update student information menu. Allows the user to update a student record's major, advisor, or mobile phone
    # number via their ID passed into the update methods above, validating inputs just as the add new students menu
    # does.
    elif (buffer == '4'):
        while (not goBack):
            updating = True
            print('\n***UPDATE STUDENT INFORMATION***\nWould you like to update a student\'s <major>, <advisor>, or <phone number>?')
            buffer = input("Enter the term within the <> brackets to select that option, or enter <back> to exit to main menu: ")
            buffer = buffer.lower()
            if (buffer == 'back'):
                goBack = True
            elif (buffer == 'major'):
                while (updating):
                    updatingMajor = True
                    print('\n***UPDATE MAJOR***')
                    buffer = input("Enter the student ID of the student record you would like to update, or enter <back> to return to update options: ")
                    buffer = buffer.lower()
                    if (buffer == 'back'):
                        updating = False
                    elif (buffer.isdigit()):
                        if (check_student(buffer)):
                            updateID = buffer
                            while (updatingMajor):
                                print('Student ID ' + updateID + ' verified')
                                buffer = input("Enter the new major for the student record you would like to update, or enter <back> to return to student ID input: ")
                                if (buffer.lower() == 'back'):
                                    updatingMajor = False
                                elif (all(x.isalpha() or x.isspace() for x in buffer)):
                                    update_Major(updateID, buffer)
                                    updatingMajor = False
                                    updating = False
                                    goBack = True
                                    print('Student record updated')
                                    input('Press enter to continue')
                                else:
                                    print('Input is not a valid new major, please try again')
                                    input('Press enter to continue')
                        else:
                            print('Input is not a valid student ID, please try again')
                            input('Press enter to continue')
                    else:
                        print('Input is not a valid student ID, please try again')
                        input('Press enter to continue')
            elif (buffer == 'advisor'):
                while (updating):
                    updatingAdvisor = True
                    print('\n***UPDATE ADVISOR***')
                    buffer = input("Enter the student ID of the student record you would like to update, or enter <back> to return to update options: ")
                    buffer = buffer.lower()
                    if (buffer == 'back'):
                        updating = False
                    elif (buffer.isdigit()):
                        if (check_student(buffer)):
                            updateID = buffer
                            while (updatingAdvisor):
                                print('Student ID ' + updateID + ' verified')
                                buffer = input("Enter the new advisor for the student record you would like to update, or enter <back> to return to student ID input: ")
                                if (buffer.lower() == 'back'):
                                    updatingAdvisor = False
                                elif (all(x.isalpha() or x.isspace() for x in buffer)):
                                    update_Advisor(updateID, buffer)
                                    updatingAdvisor = False
                                    updating = False
                                    goBack = True
                                    print('Student record updated')
                                    input('Press enter to continue')
                                else:
                                    print('Input is not a valid new advisor, please try again')
                                    input('Press enter to continue')
                        else:
                            print('Input is not a valid student ID, please try again')
                            input('Press enter to continue')
                    else:
                        print('Input is not a valid student ID, please try again')
                        input('Press enter to continue')
            elif (buffer == 'phone number' or buffer == 'phone' or buffer == 'number'):
                while (updating):
                    updatingPhoneNumber = True
                    print('\n***UPDATE MOBILE PHONE NUMBER***')
                    buffer = input("Enter the student ID of the student record you would like to update, or enter <back> to return to update options: ")
                    buffer = buffer.lower()
                    if (buffer == 'back'):
                        updating = False
                    elif (buffer.isdigit()):
                        if (check_student(buffer)):
                            updateID = buffer
                            while (updatingPhoneNumber):
                                print('Student ID ' + updateID + ' verified')
                                buffer = input("Enter the new mobile phone number for the student record you would like to update, or enter <back> to return to student ID input: ")
                                if (buffer.lower() == 'back'):
                                    updatingPhoneNumber = False
                                elif (all(x == 'x' or not x.isalpha() for x in buffer)):
                                    update_MobilePhoneNumber(updateID, buffer)
                                    updatingPhoneNumber = False
                                    updating = False
                                    goBack = True
                                    print('Student record updated')
                                    input('Press enter to continue')
                                else:
                                    print('Input is not a valid new mobile phone number, please try again')
                                    input('Press enter to continue')
                        else:
                            print('Input is not a valid student ID, please try again')
                            input('Press enter to continue')
                    else:
                        print('Input is not a valid student ID, please try again')
                        input('Press enter to continue')
            else:
                print('Input not recognized, please try again')
                input('Press enter to continue')

    # The delete/restore menu. Allows the user to delete a student record, passing a student ID into the
    # delete_student() method, or recover a student record by doing the same with the recover_student() method. Uses
    # the check_student() and check_all() methods to validate the ID fed in.
    elif (buffer == '5'):
        while (not goBack):
            deletingrestoring = True
            print('\n***DELETE/RESTORE STUDENT***\nWould you like to <delete> a student record or <restore> a deleted student record?')
            buffer = input("Enter the term within the <> brackets to select that option, or enter <back> to exit to main menu: ")
            buffer = buffer.lower()
            if (buffer == 'back'):
                goBack = True
            elif (buffer == 'delete'):
                while (deletingrestoring):
                    print('\n***DELETE STUDENT RECORD***')
                    buffer = input("Enter the student ID of the student record you wish to delete, or enter <back> to return to the restore/delete page: ")
                    buffer = buffer.lower()
                    if (buffer == 'back'):
                        deletingrestoring = False
                    elif (buffer.isdigit()):
                        if (check_student(buffer)):
                            delete_student(buffer)
                            print('Student record deleted')
                            input('Press enter to continue')
                            deletingrestoring = False
                        else:
                            print('Input is not a valid student ID, please try again')
                            input('Press enter to continue')
                    else:
                        print('Input is not a valid student ID, please try again')
                        input('Press enter to continue')
            elif (buffer == 'restore'):
                while (deletingrestoring):
                    print('\n***RESTORE DELETED STUDENT RECORD***')
                    buffer = input("Enter the student ID of the deleted student record you wish to restore, or enter <back> to return to the restore/delete page: ")
                    buffer = buffer.lower()
                    if (buffer == 'back'):
                        deletingrestoring = False
                    elif (buffer.isdigit()):
                        if (check_all(buffer)):
                            recover_student(buffer)
                            print('Student record restored')
                            input('Press enter to continue')
                            deletingrestoring = False
                        else:
                            print('Input is not a valid student ID, please try again')
                            input('Press enter to continue')
                    else:
                        print('Input is not a valid student ID, please try again')
                        input('Press enter to continue')
            else:
                print('Input not recognized, please try again')
                input('Press enter to continue')

    # The search menu. Uses the searchby methods to allow the user to search by major, GPA, city, state, or advisor.
    elif (buffer == '6'):
        while (not goBack):
            searching = True
            print('\n***SEARCH FOR STUDENTS***\nWould you like to search for students by <Major>, <GPA>, <City>, <State>, or <Advisor>?')
            buffer = input("Enter the term within the <> brackets to select that option, or enter <back> to exit to main menu: ")
            buffer = buffer.lower()
            if (buffer == 'back'):
                goBack = True
            elif (buffer == 'major'):
                while(searching):
                    print('\n***SEARCH BY MAJOR***')
                    buffer = input("Enter the major by which you would like to search, or enter <back> to return to search options: ")
                    buffer = buffer.lower()
                    if (buffer == 'back'):
                        searching = False
                    elif (all(x.isalpha() or x.isspace() for x in buffer)):
                        searchby_Major(buffer)
                        searching = False
                        input('Press enter to continue')
                    else:
                        print('Input is not in line with what you are searching by, please try again')
                        input('Press enter to continue')
            elif (buffer == 'gpa'):
                while (searching):
                    print('\n***SEARCH BY GPA***')
                    buffer = input("Enter the GPA you would like to search for students with, or enter <back> to return to search options: ")
                    buffer = buffer.lower()
                    if (buffer == 'back'):
                        searching = False
                    elif (all(x.isdigit() or x == '.' for x in buffer)):
                        searchby_GPA(buffer)
                        searching = False
                        input('Press enter to continue')
                    else:
                        print('Input is not in line with what you are searching by, please try again')
                        input('Press enter to continue')
            elif (buffer == 'city'):
                while (searching):
                    print('\n***SEARCH BY CITY***')
                    buffer = input("Enter the city by which you would like to search, or enter <back> to return to search options: ")
                    buffer = buffer.lower()
                    if (buffer == 'back'):
                        searching = False
                    elif (all(x.isalpha() or x.isspace() for x in buffer)):  # Assumes that no cities have numbers in their names
                        searchby_City(buffer)
                        searching = False
                        input('Press enter to continue')
                    else:
                        print('Input is not in line with what you are searching by, please try again')
                        input('Press enter to continue')
            elif (buffer == 'state'):
                while (searching):
                    print('\n***SEARCH BY STATE***')
                    buffer = input("Enter the state by which you would like to search, or enter <back> to return to search options: ")
                    buffer = buffer.lower()
                    if (buffer == 'back'):
                        searching = False
                    elif (all(x.isalpha() or x.isspace() for x in buffer)):  # Assumes that no states have numbers in their names
                        searchby_State(buffer)
                        searching = False
                        input('Press enter to continue')
                    else:
                        print('Input is not in line with what you are searching by, please try again')
                        input('Press enter to continue')
            elif (buffer == 'advisor'):
                while (searching):
                    print('\n***SEARCH BY ADVISOR***')
                    buffer = input("Enter the advisor by which you would like to search, or enter <back> to return to search options: ")
                    buffer = buffer.lower()
                    if (buffer == 'back'):
                        searching = False
                    elif (all(x.isalpha() or x.isspace() for x in buffer)):  # Assumes that no advisors have numbers in their names
                        searchby_Advisor(buffer)
                        searching = False
                        input('Press enter to continue')
                    else:
                        print('Input is not in line with what you are searching by, please try again')
                        input('Press enter to continue')
            else:
                print('Input not recognized, please try again')
                input('Press enter to continue')

    # If the user goofs up. All user input requests have this else statement.
    else:
        print('Input not recognized, please try again')
        input('Press enter to continue')

# Gotta close that cursor.
mycursor.close()