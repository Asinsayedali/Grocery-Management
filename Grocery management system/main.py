import streamlit as st
import pandas as pd
from PIL import Image
#from drug_db import *
import random

## SQL DATABASE CODE
import sqlite3


conn = sqlite3.connect("grocery_data.db",check_same_thread=False)
c = conn.cursor()

def cust_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Customers(
                    C_Name VARCHAR(50) NOT NULL,
                    C_Password VARCHAR(50) NOT NULL,
                    C_Email VARCHAR(50) PRIMARY KEY NOT NULL, 
                    C_State VARCHAR(50) NOT NULL,
                    C_Number VARCHAR(50) NOT NULL 
                    )''')
    print('Customer Table create Successfully')

def customer_add_data(Cname,Cpass, Cemail, Cstate,Cnumber):
    c.execute('''INSERT INTO Customers (C_Name,C_Password,C_Email, C_State, C_Number) VALUES(?,?,?,?,?)''', (Cname,Cpass,  Cemail, Cstate,Cnumber))
    conn.commit()

def customer_view_all_data():
    c.execute('SELECT * FROM Customers')
    customer_data = c.fetchall()
    return customer_data
def customer_update(Cemail,Cnumber):
    c.execute(''' UPDATE Customers SET C_Number = ? WHERE C_Email = ?''', (Cnumber,Cemail,))
    conn.commit()
    print("Updating")
def customer_delete(Cemail):
    c.execute(''' DELETE FROM Customers WHERE C_Email = ?''', (Cemail,))
    conn.commit()

def item_update(Duse, Did):
    c.execute(''' UPDATE Items SET D_Use = ? WHERE D_id = ?''', (Duse,Did))
    conn.commit()
def item_delete(itemid):
    c.execute(''' DELETE FROM Items WHERE item_id = ?''', (itemid,))
    conn.commit()

def item_create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS Items(
                item_Name VARCHAR(50) NOT NULL,
                item_ExpDate DATE NOT NULL, 
                item_category VARCHAR(50) NOT NULL,
                item_Qty INT NOT NULL, 
                item_id INT PRIMARY KEY NOT NULL)
                ''')
    print('ITEM Table create Successfully')

def item_add_data(itemname, itemexpdate, itemuse, itemqty, itemid):
    c.execute('''INSERT INTO Items (item_Name, item_Expdate, item_category, item_Qty, item_id) VALUES(?,?,?,?,?)''', (itemname, itemexpdate, itemuse, itemqty, itemid))
    conn.commit()

def item_view_all_data():
    c.execute('SELECT * FROM Items')
    item_data = c.fetchall()
    return item_data

def order_create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS Orders(
                O_Name VARCHAR(100) NOT NULL,
                O_Items VARCHAR(100) NOT NULL,
                O_Qty VARCHAR(100) NOT NULL,
                O_id VARCHAR(100) PRIMARY KEY NOT NULL)
    ''')
    print('Order Table create Successfully')

def order_delete(Oid):
    c.execute(''' DELETE FROM Orders WHERE O_id = ?''', (Oid,))

def order_add_data(O_Name,O_Items,O_Qty,O_id):
    c.execute('''INSERT INTO Orders (O_Name, O_Items,O_Qty, O_id) VALUES(?,?,?,?)''',
              (O_Name,O_Items,O_Qty,O_id))
    conn.commit()


def order_view_data(customername):
    c.execute('SELECT * FROM ORDERS Where O_Name == ?',(customername,))
    order_data = c.fetchall()
    return order_data

def order_view_all_data():
    c.execute('SELECT * FROM ORDERS')
    order_all_data = c.fetchall()
    return order_all_data






#__________________________________________________________________________________







def admin():


    st.title("Grocery Database Dashboard")
    menu = ["Items", "Customers", "Orders", "About"]
    choice = st.sidebar.selectbox("Menu", menu)



    ## DRUGS
    if choice == "Items":

        menu = ["Add", "View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "Add":

            st.subheader("Add Grocery Item")

            col1, col2 = st.columns(2)

            with col1:
                item_name = st.text_area("Enter the Item Name")
                item_expiry = st.date_input("Expiry Date of the item (YYYY-MM-DD)")
                item_mainuse = st.text_area("Category")
            with col2:
                item_quantity = st.text_area("Enter the quantity")
                item_id = st.text_area("Enter the item id (example:#D1)")

            if st.button("Add Item"):
                item_add_data(item_name,item_expiry,item_mainuse,item_quantity,item_id)
                st.success("Successfully Added Data")
        if choice == "View":
            st.subheader("Grocery Item Details")
            drug_result = item_view_all_data()
            #st.write(drug_result)
            with st.expander("View All Item Data"):
                item_clean_df = pd.DataFrame(drug_result, columns=["Name", "Expiry Date", "Use", "Quantity", "ID"])
                st.dataframe(item_clean_df)
            with st.expander("View Item Quantity"):
                item_name_quantity_df = item_clean_df[['Name','Quantity']]
                #drug_name_quantity_df = drug_name_quantity_df.reset_index()
                st.dataframe(item_name_quantity_df)
        if choice == 'Update':
            st.subheader("Update Item Details")
            item_id = st.text_area("Item ID")
            item_use = st.text_area("Item Use")
            if st.button(label='Update'):
                item_update(item_use,item_id)

        if choice == 'Delete':
            st.subheader("Delete Item")
            did = st.text_area("Item ID")
            if st.button(label="Delete"):
                item_delete(did)



    ## CUSTOMERS
    elif choice == "Customers":

        menu = ["View", "Update", "Delete"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Customer Details")
            cust_result = customer_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Customer Data"):
                cust_clean_df = pd.DataFrame(cust_result, columns=["Name", "Password","Email-ID" ,"Area", "Number"])
                st.dataframe(cust_clean_df)

        if choice == 'Update':
            st.subheader("Update Customer Details")
            cust_email = st.text_area("Email")
            cust_number = st.text_area("Phone Number")
            if st.button(label='Update'):
                customer_update(cust_email,cust_number)

        if choice == 'Delete':
            st.subheader("Delete Customer")
            cust_email = st.text_area("Email")
            if st.button(label="Delete"):
                customer_delete(cust_email)

    elif choice == "Orders":

        menu = ["View"]
        choice = st.sidebar.selectbox("Menu", menu)
        if choice == "View":
            st.subheader("Order Details")
            order_result = order_view_all_data()
            #st.write(cust_result)
            with st.expander("View All Order Data"):
                order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items","Qty" ,"ID"])
                st.dataframe(order_clean_df)
    elif choice == "About":
        st.subheader("DBMS Mini Project")
        st.subheader("By Asin, Ashba, Aarcha")

##Edited code

def getauthenicate(username, password):
    c.execute('SELECT C_Password FROM Customers WHERE C_Name = ?', (username,))
    cust_password = c.fetchall()
    if cust_password[0][0] == password:
        return True
    else:
        return False

def show_customer_page():
    st.title("Welcome to Online Grocery Store")

    st.subheader("Your Order Details")
    order_result = order_view_data(st.session_state.username)
    with st.expander("View All Order Data"):
        order_clean_df = pd.DataFrame(order_result, columns=["Name", "Items", "Qty", "ID"])
        st.dataframe(order_clean_df)

    item_result = item_view_all_data()
    items_container = st.container()
    
    with items_container:
        # Initialize quantities in session state if not exists
        if 'quantities' not in st.session_state:
            st.session_state.quantities = {
                'Apple': 0,
                'Orange': 0,
                'Potato': 0
            }
        
        # Item 1: Apple
        st.subheader("Item: " + item_result[0][0])
        img = Image.open('images/Apple.jpg')
        st.image(img, width=100, caption="Rs. 150/-")
        st.session_state.quantities['Apple'] = st.slider(
            label="Quantity",
            min_value=0,
            max_value=5,
            value=st.session_state.quantities['Apple'],
            key="apple_slider"
        )
        st.info("Category: " + str(item_result[0][2]))

        # Item 2: Orange
        st.subheader("Item: " + item_result[1][0])
        img = Image.open('images/Orange.JPG')
        st.image(img, width=100, caption="Rs. 100/-")
        st.session_state.quantities['Orange'] = st.slider(
            label="Quantity",
            min_value=0,
            max_value=5,
            value=st.session_state.quantities['Orange'],
            key="orange_slider"
        )
        st.info("Category: " + str(item_result[1][2]))

        # Item 3: Potato
        st.subheader("Item: " + item_result[2][0])
        img = Image.open('images/Potato.JPG')
        st.image(img, width=100, caption="Rs. 65/-")
        st.session_state.quantities['Potato'] = st.slider(
            label="Quantity",
            min_value=0,
            max_value=5,
            value=st.session_state.quantities['Potato'],
            key="potato_slider"
        )
        st.info("Category: " + str(item_result[2][2]))

        if st.button(label="Buy now"):
            O_items = []
            O_Qty = []
            
            for item, qty in st.session_state.quantities.items():
                if qty > 0:
                    O_items.append(item)
                    O_Qty.append(str(qty))
            
            if O_items:
                O_id = st.session_state.username + "#O" + str(random.randint(0,1000000))
                order_add_data(
                    st.session_state.username, 
                    ",".join(O_items), 
                    ",".join(O_Qty), 
                    O_id
                )
                st.success("Order placed successfully!")
            else:
                st.warning("Please select at least one item")

def main():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None

    menu = ["Login", "SignUp", "Admin"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        
        # Login button
        if st.sidebar.button("Login"):
            if username and password:
                try:
                    if getauthenicate(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.sidebar.success("Logged in successfully!")
                    else:
                        st.sidebar.error("Invalid username or password")
                except IndexError:
                    st.sidebar.error("Invalid username or password")
            else:
                st.sidebar.warning("Please enter both username and password")
        
        # Show logout button if authenticated
        if st.session_state.authenticated:
            if st.sidebar.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.username = None
                st.session_state.quantities = {
                    'Apple': 0,
                    'Orange': 0,
                    'Potato': 0
                }
                st.experimental_rerun()

        # Show customer page if authenticated
        if st.session_state.authenticated:
            show_customer_page()

    elif choice == "SignUp":
        st.subheader("Create New Account")
        cust_name = st.text_input("Name")
        cust_password = st.text_input("Password", type='password', key=1000)
        cust_password1 = st.text_input("Confirm Password", type='password', key=1001)
        col1, col2, col3 = st.columns(3)

        with col1:
            cust_email = st.text_area("Email ID")
        with col2:
            cust_area = st.text_area("State")
        with col3:
            cust_number = st.text_area("Phone Number")

        if st.button("Signup"):
            if cust_password == cust_password1:
                customer_add_data(cust_name, cust_password, cust_email, cust_area, cust_number)
                st.success("Account Created!")
                st.info("Go to Login Menu to login")
            else:
                st.warning('Passwords don\'t match')

    elif choice == "Admin":
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if username == 'admin' and password == 'admin':
            admin()

if __name__ == '__main__':
    item_create_table()
    cust_create_table()
    order_create_table()
    main()