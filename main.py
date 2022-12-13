import os
from dotenv import load_dotenv
load_dotenv()

# Environment Variables
SQLUSERNAME = os.getenv("SQLUSERNAME")
SQLPASSWORD = os.getenv("SQLPASSWORD")
DEFAULT_DB = os.getenv("DEFAULT_DB")


# Functions

def sql_ImportandConnect(sqlusername=SQLUSERNAME,sqlpasswd=SQLPASSWORD,db=DEFAULT_DB):
    import mysql.connector as sqltor
    global mycon
    global curobj
    try:
        mycon=sqltor.connect(host="",user=sqlusername,passwd=sqlpasswd,database=db)
        curobj=mycon.cursor()
        print("**********Connection Successfully Established!**********")
    except:
        print("**********Connection to the SQL Server Failed. Please Contact Authorized Personnel**********")

def sql_CreateDB(dbname):
    try:
        exest='CREATE DATABASE IF NOT EXISTS {}'.format(dbname)
        curobj.execute(exest)
        mycon.commit
        print("Database,",dbname,"Successfully Created!")
    except:
        print("An Error Occurred while creating the database")

# sql_ImportandConnect()
# sql_CreateDB('practicalrecord')

def sql_createTable(tname):
    try:
        exest='CREATE TABLE IF NOT EXISTS {} ('.format(tname) # IF NOT EXISTS
        for i in range(int(input("Enter how many columns in, "+tname))):
            col=input('Enter the column name SPACE the column datatype SPACE parameters(if needed):')+','
            exest+=col
        else:
            exest=exest[:-1]+')'
            curobj.execute(exest)
    except:
        print("An Error Occurred While Creating the table")

# sql_createTable("Test2")

def sql_descTable(tname):
    try:
        exest='DESCRIBE {}'.format(tname)
        curobj.execute(exest)
        tb=curobj.fetchall()
        for i in tb:
            print(i)
    except:
        print("An Error Occurred while describing the table")

# sql_descTable('Test2')

def sql_insertTable(tname,n=1): #Default arguement =1 for number of records to be entered into tname
    for i in range(n):
        try:
            #To find number of columns to be entered:
            exest='DESCRIBE {}'.format(tname)
            curobj.execute(exest)
            res=curobj.fetchall()
            #Creating the query
            exest='INSERT INTO {} VALUES ('.format(tname)
            print("Enter the values for entry",i+1)
            for x in res:
                exest=exest+input("Enter value of field "+str(x[0]))+','
            else:
                exest=exest[:-1]+')'
                # print(exest)
                curobj.execute(exest)
                mycon.commit()
        except:
             print("An Error Occurred while inserting into the table")

# sql_insertTable('Test2',3)

def sql_retrieveTableContents(tname):
    try:
        exest='SELECT * FROM {}'.format(tname)
        curobj.execute(exest)
        res=curobj.fetchall()
        for x in res:
            print(x)
    except:
        print("An Error Occurred while retrieving the data")

# sql_retrieveTableContents('Test2')

def sql_updateDataTable(tname):
    # UPDATE TABLE TNAME SET PARAS WHERE CONDITION;
    # Choice for PARAS (select from list)
    # Choice for condition
    try:
        #To find number of columns to be entered:
        exest='DESCRIBE {}'.format(tname)
        curobj.execute(exest)
        res=curobj.fetchall()
        #Creating the query
        l=[]
        for x in res:
            l.append(x[0].strip("'"))  #List of column names
        exest="UPDATE {} SET ".format(tname)
        # print(l)
        while True:
            try:
                print("Chose a column field to change:")
                print('*'*30)
                for x in l:
                    print(x) #Showing the column names to chose from
                print('*'*30)
                i=input("Enter a choice from the above list(CASE SENSITIVE):")
                if i in l:
                    print(exest+i+'_____')
                    cond1=input("[NEW VALUE] Enter the change:(IN SQL SYNTAX eg:=6):")
                    break
                else:
                    print("Please input it properly")
            except:
                print("An Error Occurred")
        exest=exest+i+cond1+' WHERE '
        print(exest+'______')
        condn=input("[CONDITION] Enter the column name and the condition:")
        exest+=condn
        # print(exest)
        curobj.execute(exest)
        mycon.commit()
    except:
        print("An Error Occurred while updating the record")

# sql_updateDataTable('Test2')

def sql_retrieveTableContentsWithConditions(tname):
    try:
        #To find number of columns to be entered:
        exest='DESCRIBE {}'.format(tname)
        curobj.execute(exest)
        res=curobj.fetchall()
        #Creating the query
        l=[]
        for x in res:
            l.append(x[0].strip("'"))  #List of column names
        exest="SELECT "
        while True:
            try:
                print("Chose a column field(s) to display:")
                print('*'*30)
                for x in l:
                    print(x) #Showing the column names to chose from
                print('*'*30)
                print(exest+'____')
                i=input("Enter choice(s) from the above list(CASE SENSITIVE)(For multiple choices use a comma):")
                fl=False
                if i=='*':
                    fl=True
                else:
                    for c in i.split(','):  #Checking if all the columns inserted by the user are valid
                        if c not in l:
                            print("Enter it Properly")
                            break
                    else:
                        fl=True
                if fl:
                    exest=exest+i+' FROM {} WHERE '.format(tname)
                    break
            except:
                print("An Error Occurred. Please Try Again")
        #Conditions
        print(exest+'____')
        i=input("[CONDITION] Enter the column name and the condition:")
        exest+=i
        print(exest)
        curobj.execute(exest)
        for i in curobj.fetchall():
            print(i)
    except:
        print("An Error Occurred while searching and retrieving as per the given conditions")

# sql_retrieveTableContentsWithConditions('Test2')

def sql_deleteTableContentsWithConditions(tname):
    try:
        #To find number of columns to be entered:
        exest='DESCRIBE {}'.format(tname)
        curobj.execute(exest)
        res=curobj.fetchall()
        #Creating the query
        l=[]
        for x in res:
            l.append(x[0].strip("'"))  #List of column names
        exest="DELETE FROM {} WHERE ".format(tname)
        # print(l)
        while True:
            try:
                print("Chose a column name to type in the delete condition::")
                print('*'*30)
                for x in l:
                    print(x) #Showing the column names to chose from
                print('*'*30)
                print(exest+' ____')
                i=input("Enter the delete condition(or type '*' or 'all' to delete all records):")
                if i=='*' or i.lower()=='all':
                    exest="DELETE FROM {}".format(tname)
                    print(exest)
                    break
                else:
                    exest=exest+i
                    print(exest)
                    break
            except:
                print("An Error Occurred. Please Try Again")
        curobj.execute(exest)
        mycon.commit()
        print("Executed.")
    except:
        print("An Error Occurred While Deleting The Records.")

# sql_deleteTableContentsWithConditions('Test2')

#MySQL Interactive Menu:
def sqlmenu():
    conn=False
    db1=None
    while True:
        try:
            print('*'*80)
            print("********** Welcome to the MySQL CLI Tool **********")
            print("Connected? -",conn)
            print("Database-",db1)
            print("*"*80)
            print("\t Press 0 to connect to a database")
            print("\t Press 1 create a database")
            print("\t Press 2 to create a table into the database")
            print("\t Press 3 to display the structure of a table")
            print("\t Press 4 to insert records into a table")
            print("\t Press 5 to modify a record in a table")
            print("\t Press 6 to display all records in a table")
            print("\t Press 7 to display records from a table based on conditions")
            print("\t Press 8 to delete record(s)")
            print("\t Press 9 to exit")
            print("*"*80)
            c=int(input("Enter an option:"))
            if c==9:
                break
            elif c==0:
                while True:
                    ci=int(input("Do you want to insert login credentials yourself?(1=Yes,0=No)"))
                    if ci==1:
                        try:
                            db1=input("Enter your database name:")
                            sql_ImportandConnect(db=db1,sqlusername=input("Enter your MySQL username:"),sqlpasswd=input("Enter your MySQL password:"))
                            conn=True
                        except:
                            print("An Error Occurred Please Try Again")
                        break
                    elif ci==0:
                        try:
                            sql_ImportandConnect(sqlusername=SQLUSERNAME,sqlpasswd=SQLPASSWORD,db=DEFAULT_DB)
                            db="practicalrecord"
                            conn=True
                        except:
                            print("An Error Occurred Please Try Again")
                        break
                    else:
                        print("Please enter a valid answer")
            elif c==1:
                sql_CreateDB(input('Enter the Database name:'))
            elif c==2:
                sql_createTable(input('Enter the new tablename:'))
            elif c==3:
                sql_descTable(input("Enter the table's name:"))
            elif c==4:
                sql_insertTable(input("Enter the table's name:"),n=int(input("Enter how many records you want to input:")))
            elif c==5:
                sql_updateDataTable(input("Enter the table's name:"))
            elif c==6:
                sql_retrieveTableContents(input("Enter the table's name:"))
            elif c==7:
                sql_retrieveTableContentsWithConditions(input("Enter the table's name:"))
            elif c==8:
                sql_deleteTableContentsWithConditions(input("Enter the table's name:"))
            else:
                print("Please Enter a Corrrect Reply.")
        except:
            print("An Error Occurred in the functions compiler/menu")

if __name__ == "__main__":
    sqlmenu()