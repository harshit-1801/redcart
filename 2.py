import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root"
)

sql=mydb.cursor()
sql.execute("use redcart")

import random
import re
from datetime import date


def check(email):
    # check whether email is like ' ___@___.___'
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        return 1
          
    else:  
        return 0


def contactcheck(contact):
    # check whether the length of contact is 10 i.e valid or not
    if len(contact.rstrip("\n"))==10:
        return 1
    else:
        return 0
    


def passcheck():
    # check whether password contains a digit,special symbol($,%,@) and have upto 8 character
    password=input("Password--> ")
    
    digit=0
    symbol=0
    
    for i in password:
        if i in "1234567890":
            digit+=1
        elif i in "@$%":
            symbol+=1
            
        # if digit found add 1 to digit and same for special symbol
        # if atleast 1 digit and 1 special symbol found break loop and return 1 in digit
        
        if digit>=1 and symbol>=1:
            digit=1
            break
        
    if digit!=1 or len(password)<9:
        print("Password must contains a digit,special symbol($,%,@) and must have upto 8 character") 
        return(passcheck())
    else:
        return(password)



def Signup():
    sql.execute("create table if not exists supplier (name varchar(50) not null,contact bigint(10) not null,email varchar(50) primary key not null,password varchar(50) not null);")
    name = input("Name--> ")
    while True:
        contact = input("Contact--> ")
        if contactcheck(contact)==1:
            break
        else:
            print("Invalid Contact")
            
    while True:
        email = input("Email id--> ")
        if check(email)==1:
            break
        else:
            print("Invalid email")
        
        
    
    password = passcheck()
    a="insert into supplier(name,contact,email,password) values(%s,%s,%s,%s);"
    b=(name,int(contact),email,password)
    try:
        sql.execute(a,b)
    except:
        print("Email already exist")
    mydb.commit()
    

def Validation():
    
    while True:
        email = input("Email id--> ")
        password = input("Password--> ")
        sql.execute("select password from supplier where email=%s",(email,))
        mail=sql.fetchall()
        try:
            if mail[0][0]==password:
                sql.execute("select name from supplier where email=%s",(email,))
                name=sql.fetchall()
                print("Welcome",name[0][0]," to Redcart\n")
                user.append(email)
                user.append(name[0][0])
                break
            else:
                print("Invalid credentials")
        except IndexError:
            print("Invalid credentials")


def Product():
    sql.execute("create table if not exists product (email varchar(50) not null,Date_of_supply varchar(50) not null,Product_name varchar(50) not null,price int not null,quantity int not null);")
    name=input("Enter the product name  ")
    price=int(input("Enter the price per piece  "))
    quantity=int(input("Enter the quantity "))
    sql.execute("insert into product values(%s,%s,%s,%s,%s);",(user[0],date.today(),name,price,quantity))
    mydb.commit()
        
def Logout():
    # delete the email of user currently login from user list
    user.pop()

user=[]
while True:
    try: 
        user[0]==None
        print("    Press 1 for Add Product")
        print("    Press 0 to Quit\n")
        ch=input("Enter your choice ")
        if ch=='1':
            Product()
        elif ch=='0':
            break
        else:
            print("Invalid choice \n")


    except:
        print("    Press 1 for Signup")
        print("    Press 2 for Login")
        print("    Press 0 to Quit\n")
        
        ch=input("Enter your choice ")
        if ch=='1':
            Signup()
        elif ch=='2':
            Validation()
        elif ch=='0':
            break
        else:
            print("Invalid choice \n")
