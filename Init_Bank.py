import mysql.connector
def create_database(username , password):
    try:
        mydb = mysql.connector.connect(host = "localhost" , user = username, passwd = password)
        myc = mydb.cursor()
        try:
            myc.execute("CREATE DATABASE Bank")
            myc.execute("USE Bank")
            myc.execute("CREATE TABLE User (UserID int NOT NULL PRIMARY KEY , Name varchar(40) NOT NULL , Email varchar(30) , Balance int NOT NULL , Card bigint , CVV smallint , Expiry date)")
            mydb.commit()
            myc.close()
            mydb.close()
            return 0
        except mysql.connector.errors.DatabaseError as d:
            myc.close()
            mydb.close()
            return d.errno
    except mysql.connector.errors.ProgrammingError as e:
        return (f"Error occurred: {e}")
if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    print(create_database(username , password))