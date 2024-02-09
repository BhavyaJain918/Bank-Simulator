import mysql.connector
import random
from sys import exit
import datetime
from Init_Bank import create_database
from credit_card_info_generator import generate_credit_card
from Bank_Mail import email_bank
format = "%m-%Y"
date = datetime.date.today()
email_from = ""     # Your own mail address you wish to send users mails from
password = ""       # Above mail address's password
def credit(UserID , amt):
    try:
        print(f"Your deposit amount is {amt}")
        confirm = input("Press Y to confirm , N to quit: ")
        if confirm == "Y":
            myc.execute("UPDATE User SET Balance = Balance + %s WHERE UserID = %s" , (amt , UserID))
            mydb.commit()
            print("Your deposit was successful")
        else:
            print("You chose to quit")
    except ValueError as valerr:
        print(f"Error occurred: {valerr}")

def debit(UserID , amount):
    try:
        confirm = input("Press Y to confirm , N to quit: ")
        if confirm == "Y":
            myc.execute("SELECT Balance FROM User WHERE UserID = %s" , (UserID , ))
            bal = myc.fetchone()
            if bal != None:
                for b in bal:
                    if amount <= b and amount > 0:
                        myc.execute("UPDATE User SET Balance = Balance - %s WHERE UserID = %s" , (amount , UserID))
                        mydb.commit()
                        return 0
                    else:
                        return ("Insufficient balance")   
            else:
                return ("You have zero balance in your account")
        else:
            return ("You chose to quit")
    except ValueError as err:
        return (f"Error occurred: {err}")

def register(Name , Email):
    try:
        ids = set()
        myc.execute("SELECT UserID FROM User")
        user_id = myc.fetchall()
        for id in user_id:
            for id_ in id:
                ids.add(id_)
        rand_id = random.randint(10000 , 99999)
        while rand_id in ids:
            rand_id = random.randint(10000 , 99999)
        ids.add(rand_id)
        myc.execute("INSERT INTO User VALUES (%s , %s , %s , 0 , NULL , NULL ,NULL)" , (rand_id , Name , Email))
        mydb.commit()
        print(f"You are successfully registered and your User ID is {rand_id}")
    except mysql.connector.errors.DataError as de:
        print(f"Error occurred: {de}")
    except mysql.connector.errors.DatabaseError as e:
        print(f"Error occurred: {e}")

def transaction(user):
    try:
        myc.execute("SELECT EXISTS (SELECT 1 FROM User WHERE UserID = %s)" , (user , ))
        num = myc.fetchall()
        if num != [(0 , )]:
            print("Press\n1. To deposit money\n2. To withdraw money\n")
            ch = int(input("Please enter your choice: "))
            match(ch):
                case 1:
                    amt_ = int(input("Please enter the amount: "))
                    credit(user , amt_)
                case 2:
                    status = payment(user)
                    if status == 0:
                        print("Your withdrawal was successful")
                    else:
                        print(status)
                case _:
                    print("Please enter appropriate option")
        else:
            print(f"No user with User ID {user} found")
    except ValueError as v:
        print(f"Error occurred: {v}")

def card(inp):
    try:
        print("Welcome to card apllication utility")
        myc.execute("SELECT EXISTS (SELECT 1 FROM User WHERE UserID = %s)" , (inp , ))
        number = myc.fetchall()
        if number != [(0 , )]:
            myc.execute("SELECT Email FROM User WHERE UserID = %s" , (inp , ))
            email = myc.fetchone()
            if email != None:
                add = email[0] # type: ignore
                print("Press\n1. For Visa\n2. For RuPay")
                card_ch = int(input("Please enter your choice: "))
                c_card = {}
                match(card_ch):
                    case 1:
                        c_card = generate_credit_card("Visa")
                    case 2:
                        c_card = generate_credit_card("RuPay")
                    case _:
                        print("Please enter appropriate option")
                date_exp = c_card["expiry_date"].replace("/" , "-")
                date_ = datetime.datetime.strptime(date_exp , format)
                myc.execute("UPDATE User SET Card = %s , CVV = %s , Expiry = %s WHERE UserID = %s" , (c_card["card_number"] , int(c_card["cvv"]) , date_ , inp))
                mydb.commit()
                status = email_bank(email_from , password , add , date , inp , c_card["card_number"])
                print(status)
            else:
                print(f"No Email address was provided against User ID {inp}")
        else:
            print(f"No user with User ID {inp} found")  
    except ValueError as ve:
        print(f"Error occurred: {ve}")

def payment(ID):
    try:
        list_user = []
        details = []
        myc.execute("SELECT UserID FROM User")
        id_user = myc.fetchall()
        if id_user != None:
            for i in id_user:
                for j in i:
                    list_user.append(j)
            if ID in list_user:
                card_no = int(input("Please enter your card number: "))
                myc.execute("SELECT Card , CVV , Expiry FROM User WHERE UserID = %s" , (ID , ))
                card_u = myc.fetchone()
                if card_u != None:
                    for c in card_u:
                        details.append(c)
                    if date != details[2]:
                        if details[0] == card_no:
                            cvv = int(input("Please enter CVV: "))
                            if details[1] == cvv:
                                pay = int(input("Please enter amount: "))
                                status_ = debit(ID , pay)
                                if status_ == 0:
                                    return 0
                                else:
                                    return (status_)
                            else:
                                print("Incorrect CVV")
                        else:
                            print("Please enter correct card number")
                    else:
                        print("Your card has expired. Please renew it for hassel-free experience")
                else:
                    print(f"No Debit Card was issued against User ID {ID}")
            else:
                print(f"No user with User ID {ID} found") 
        else:
            print("Database is empty")
    except ValueError as val:
        print(f"Error occurred: {val}")
        
user_my = input("Enter username: ")
passw = input("Enter password: ")
stat = create_database(user_my , passw)
try:
    mydb = mysql.connector.connect(host = "localhost" , user = user_my , passwd = passw , database = "Bank")
    myc = mydb.cursor()
except mysql.connector.errors.ProgrammingError as e:
        print(f"Error occurred: {e}")
        exit()

def init():
    if stat == 0 or stat == 1007:
        print("Welcome to ABC Bank. Please choose from options provided below.\n")
        print("Press\n1. To register as new user\n2. To perform transactions\n3. To apply for a Debit card\n4. For payment via card\n0. To quit")
        while True:
            ch = int(input("Please enter your choice: "))
            if ch == 1:
                name = input("Please enter your name: ")
                mail = input("Please enter your email: ")
                register(name , mail)
            else:
                match(ch):
                    case 2:
                        id = int(input("Enter your User ID: "))
                        transaction(id)
                    case 3:
                        id = int(input("Enter your User ID: "))
                        card(id)
                    case 4:
                        id = int(input("Enter your User ID: "))
                        ret = payment(id)
                        if ret == 0:
                            print("Your payment was successful")
                        else:
                            print(ret)
                    case 0:
                        break
                    case _:
                        print("Enter appropriate option")
    else:
        print(stat)

    myc.close()
    mydb.close()

if __name__ == "__main__":
    init()