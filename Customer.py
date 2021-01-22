import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root"
)

sql=mydb.cursor()
sql.execute("create database if not exists redcart")
sql.execute("use redcart")

import random
import re



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
    sql.execute("create table if not exists consumer (name varchar(50) not null,contact bigint(10) not null,email varchar(50) primary key not null,password varchar(50) not null);")
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
    a="insert into consumer(name,contact,email,password) values(%s,%s,%s,%s);"
    b=(name,int(contact),email,password)
    sql.execute(a,b)
    mydb.commit()
    print("\nSignup sucessful")
    

def Validation():
    
    while True:
        email = input("Email id--> ")
        password = input("Password--> ")
        sql.execute("select password from consumer where email=%s",(email,))
        mail=sql.fetchall()
        try:
            if mail[0][0]==password:
                sql.execute("select name from consumer where email=%s",(email,))
                name=sql.fetchall()
                print("\nWelcome",name[0][0]," to Redcart\n")
                user.append(email)
                break
            else:
                print("Invalid credentials")
        except IndexError:
            print("Invalid credentials")


def addtocart():
    sql.execute("select Product_name,price,quantity,email from product;")
    x=sql.fetchall()
    if x != []:
        for i in range(0,len(x)):
            sql.execute("select name from supplier where email=%s",(x[i][3],))
            name=sql.fetchall()
            if x[i][2]<=5:
                print(f"{i+1}) {x[i][0]}\nRs. {x[i][1]}\nHurry only {x[i][2]} left\nSeller name {name[0][0]}\n")
            else:
                print(f"{i+1}) {x[i][0]}\nRs. {x[i][1]}\nSeller name {name[0][0]}\n")
        choice=int(input("Enter your choice "))
        add = True
        while add:
            quantity=int(input("Enter the quantity "))
            if quantity > x[i][2]:
                print(f"Only {x[i][2]} available, can't add that many.")
            else:
                add = False
        sql.execute("create table if not exists cart(email varchar(50) not null,Product_name varchar(50) not null,price varchar(50) not null,quantity bigint not null,seller_mail varchar(50) not null);")
        sql.execute("select quantity from cart where email=%s and Product_name=%s and seller_mail=%s",(user[0],x[choice-1][0],x[choice-1][3]))
        qty=sql.fetchall()
        if qty==[]:
            sql.execute("insert into cart values(%s,%s,%s,%s,%s)",(user[0],x[choice-1][0],x[choice-1][1],quantity,x[choice-1][3]))
            mydb.commit()
        else:
            sql.execute("update cart set quantity=quantity+%s where Product_name=%s and email=%s and seller_mail=%s",(quantity,x[choice-1][0],user[0],x[choice-1][3]))
            mydb.commit()
        sql.execute("update product set quantity=quantity-%s where Product_name=%s and email=%s",(quantity,x[choice-1][0],x[choice-1][3]))
        mydb.commit()
        print("\nItem added to cart successfully\n")

    else:
        print("\nNo products available")

def cart():
    sql.execute("select Product_name,price,quantity,seller_mail from cart where email=%s",(user[0],))
    x=sql.fetchall()
    if x != []:
        print("\nItems in your cart are \n")
        for i in range(len(x)):
            sql.execute("select name from supplier where email=%s",(x[i][3],))
            name=sql.fetchall()
            print(f"{i+1}) {x[i][0]}\nRs. {x[i][1]}\nQuantity {x[i][2]}\nSeller name {name[0][0]}\n")
        return x

    else:
        print("\nCart is empty")

def delete():
    x=cart()
    if x != None:
        choice=int(input("Enter the item you want to delete "))
        quantity=int(input("Enter the quantity "))
        sql.execute("update cart set quantity=quantity-%s where email=%s and Product_name=%s and seller_mail=%s",(quantity,user[0],x[choice-1][0],x[choice-1][3]))
        mydb.commit()
        sql.execute("select quantity from cart where email=%s and Product_name=%s and seller_mail=%s",(user[0],x[choice-1][0],x[choice-1][3]))
        qty=sql.fetchall()
        if qty[0][0]==0:
            sql.execute("delete from cart where email=%s and Product_name=%s and seller_mail=%s",(user[0],x[choice-1][0],x[choice-1][3]))  
            mydb.commit()
        sql.execute("update product set quantity=quantity+%s where email=%s and Product_name=%s",(quantity,x[choice-1][3],x[choice-1][0]))
        mydb.commit()

def order():
    x=cart()
    sql.execute("create table if not exists orders(email varchar(50) not null,Product varchar(100) not null,address varchar(100) not null);")
    address=input("Enter your address ")
    city=input("Enter your city ")
    pincode=input("Enter pincode ")
    state=input("Enter the state ")
    sql.execute("insert into orders values(%s,%s,%s)",(user[0],x[0][0]+" "+x[0][1]+" "+str(x[0][2])+" "+x[0][3],address+" "+city+" "+state))
    mydb.commit()
    print("Order placed successfully")
    odid=random.randint(10000,15000)
    print("Your order id is",odid,"\n")
    print("Order will be delivered to\n",address,"\n",city,",",pincode,"\n",state)
    sql.execute("delete from cart where email=%s and Product_name=%s and seller_mail=%s",(user[0],x[0][0],x[0][3])) 
    mydb.commit()

def myorder():
    sql.execute("select * from orders where email=%s",(user[0],))
    x=sql.fetchall()
    if x == []:
        print("\nNo orders yet")
    else:
        for i in range(0,len(x)):
            order=x[i][1]
            order=order.split(" ")
            print(f"{i+1}) {order[0]}\nRs. {order[1]}\nQuantity {order[2]}\n")

    
def logout():
    # delete the email of user currently login from user list
    user.pop()

user=[]
while True:
    print("\nMain Menu\n")
    try: 
        user[0]==None
        print("    Press 1 to Add Items To Cart")
        print("    Press 2 to View Your Cart")
        print("    Press 3 to Order")
        print("    Press 4 to Delete Item From Cart")
        print("    Press 5 to See Your Orders")
        print("    Press 6 to Logout")
        print("    Press 0 to Quit\n")
        ch=input("Enter your choice ")
        if ch=='1':
            addtocart()
        elif ch=='2':
            cart()
        elif ch=='3':
            order()
        elif ch=='4':
            delete()
        elif ch=='5':
            myorder()
        elif ch=='6':
            logout()
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




