#!/usr/bin/env python3
import sqlite3

class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Book:
    def __init__(self, title, author, genre):
        self.title = title
        self.author = author
        self.genre = genre

class Lease:
    def __init__(self, customer, book):
        self.customer = customer
        self.book = book

## Customer data in the form of an object
customers_data = [
    ('Joy Wambui', 'joywambui@gmail.com'),
    ('Moreen Wanjira', 'moreenwanjira@gmail.com'),
    ('Chep Kipkorir', 'chep@gmail.com'),
    ('Miriam Odhiambo', 'miriam@gmail.com'),
    ('Tabby Nyawira', 'tabby@gmail.com'),
    ('Stella Mumbi', 'stella@gmail.com')
]

### Book data with authors in the form of an object
books_data = [
    ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy'),
    ('Dune', 'Frank Herbert', 'Science Fiction'),
    ('The Girl with the Dragon Tattoo', 'Stieg Larsson', 'Mystery/Thriller'),
    ('Pride and Prejudice', 'Jane Austen', 'Romance'),
    ('The Nightingale', 'Kristin Hannah', 'Historical Fiction'),
    ('The Shining', 'Stephen King', 'Horror'),
    ('Treasure Island', 'Robert Louis Stevenson', 'Adventure'),
    ('Steve Jobs', 'Walter Isaacson', 'Biography'),
    ('Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'Non-fiction'),
    ('To Kill a Mockingbird', 'Harper Lee', 'Classic Literature')
]

##THis connects to the database 
conn = sqlite3.connect('leasing.db')
cur = conn.cursor()

###Droping existing tables that had some errors
cur.execute("DROP TABLE IF EXISTS customers")
cur.execute("DROP TABLE IF EXISTS books")
cur.execute("DROP TABLE IF EXISTS leases")

###Creating the customers table
cur.execute('''CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE
            )''')

###Creating the books table
cur.execute('''CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT UNIQUE,
                author TEXT,
                genre TEXT
            )''')

##Creating the leases table
cur.execute('''CREATE TABLE IF NOT EXISTS leases (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                customer_name TEXT,
                customer_email TEXT UNIQUE,
                book_id INTEGER,
                FOREIGN KEY(customer_id) REFERENCES customers(id),
                FOREIGN KEY(book_id) REFERENCES books(id)
            )''')

###Inserting customers into the customers table, avoiding duplicates based on email
for name, email in customers_data:
    cur.execute("INSERT OR IGNORE INTO customers (name, email) VALUES (?, ?)", (name, email))

###Inserting books into the books table, avoiding duplicates based on title
for title, author, genre in books_data:
    cur.execute("INSERT OR IGNORE INTO books (title, author, genre) VALUES (?, ?, ?)", (title, author, genre))

###CReating lease instances in the form of an object
leases_instances = [
    Lease(Customer('Joy Wambui', 'joywambui@gmail.com'), Book('The Hobbit', 'J.R.R. Tolkien', 'Fantasy')),
    Lease(Customer('Moreen Wanjira', 'moreenwanjira@gmail.com'), Book('Dune', 'Frank Herbert', 'Science Fiction')),
    Lease(Customer('Chep Kipkorir', 'chep@gmail.com'), Book('The Girl with the Dragon Tattoo', 'Stieg Larsson', 'Mystery/Thriller')),
    Lease(Customer('Miriam Odhiambo', 'miriam@gmail.com'), Book('Pride and Prejudice', 'Jane Austen', 'Romance')),
    Lease(Customer('Tabby Nyawira', 'tabby@gmail.com'), Book('The Nightingale', 'Kristin Hannah', 'Historical Fiction')),
    Lease(Customer('Stella Mumbi', 'stella@gmail.com'), Book('The Shining', 'Stephen King', 'Horror'))
]

###Inserting lease instances into the leases table
for lease in leases_instances:
    customer_id = cur.execute("SELECT id FROM customers WHERE name = ?", (lease.customer.name,)).fetchone()[0]
    customer_name = lease.customer.name  # Add this line to get customer name
    customer_email = lease.customer.email
    book_id = cur.execute("SELECT id FROM books WHERE title = ?", (lease.book.title,)).fetchone()[0]
    cur.execute("INSERT INTO leases (customer_id, customer_name, customer_email, book_id) VALUES (?,?,?,?)", (customer_id, customer_name, customer_email, book_id))


## Committing the changes to the database
conn.commit()

### Close connection
conn.close()

def list_all_customers():
    conn = sqlite3.connect('leasing.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()
    for customer in customers:
        print(customer)
    conn.commit() 
    conn.close()

def list_all_books():
    conn = sqlite3.connect('leasing.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    for book in books:
        print(book)
    conn.commit() 
    conn.close()

def list_all_genres():
    conn = sqlite3.connect('leasing.db')
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT genre FROM books")
    genres = cur.fetchall()
    for genre in genres:
        print(genre[0])
    conn.commit() 
    conn.close()

def create_new_customer(name, email):
    conn = sqlite3.connect('leasing.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    print("Customer added successfully.")
    conn.commit() 
    conn.close()

def create_new_book(title, author, genre):
    conn = sqlite3.connect('leasing.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author, genre) VALUES (?, ?, ?)", (title, author, genre))
    conn.commit()
    print("Book added successfully.")
    conn.commit() 
    conn.close()

def assign_book_to_customer(customer_name, customer_email, book_title):
    conn = sqlite3.connect('leasing.db')
    cur = conn.cursor()
    customer_id = cur.execute("SELECT id FROM customers WHERE name = ?", (customer_name,)).fetchone()
    if not customer_id:
        print("Customer not found.")
        conn.close()
        return
    book_id = cur.execute("SELECT id FROM books WHERE title = ?", (book_title,)).fetchone()
    if not book_id:
        print("Book not found.")
        conn.close()
        return
    cur.execute("UPDATE leases SET book_id = ? WHERE customer_id = ?", (book_id[0], customer_id[0]))
    conn.commit()
    print("Book assigned to customer successfully.")

def get_customer_books(customer_name):
    conn = sqlite3.connect('leasing.db')
    cur = conn.cursor()
    cur.execute("SELECT books.title FROM leases JOIN customers ON leases.customer_id = customers.id JOIN books ON leases.book_id = books.id WHERE customers.name = ?", (customer_name,))
    books = cur.fetchall()
    for book in books:
        print(book[0])
    conn.commit() 
    conn.close()
def delete_customer(customer_name):
    conn = sqlite3.connect('leasing.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM customers WHERE name = ?", (customer_name,))
    conn.commit()
    print("Customer deleted successfully.")
    conn.close()

def delete_book(book_title):
    conn = sqlite3.connect('leasing.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE title = ?", (book_title,))
    conn.commit()
    print("Book deleted successfully.")
    conn.close()

   
   ## Creating the CLI prompt options

def main():
    options = '''
0 - Exit Program
1 - List All Customers
2 - List All Books
3 - List All Book Genres
4 - Create New Customers
5 - Create New Book
6 - Get Customer's Books 
7 - Assign Book to Customer
8 - Delete Customer
9 - Delete Book

'''
    print(options)
    selectOption = input('Option >>')
    if selectOption == '0':
        exit()
    elif selectOption == '1':
        list_all_customers()
    elif selectOption == '2':
        list_all_books()
    elif selectOption == '3':
        list_all_genres()
    elif selectOption == '4':
        name = input("Enter customer's name: ")
        email = input("Enter customer's email: ")
        create_new_customer(name, email)
    elif selectOption == '5':
        title = input("Enter book's title: ")
        author = input("Enter book's author: ")
        genre = input("Enter book's genre: ")
        create_new_book(title, author, genre)
    elif selectOption == '6':
        customer_name = input("Enter customer's name: ")
        get_customer_books(customer_name)
    elif selectOption == '7':
        customer_name = input("Enter customer's name: ")
        customer_email = input("Enter customer's email: ")  
        book_title = input("Enter book's title: ")
        assign_book_to_customer(customer_name, customer_email, book_title)
    elif selectOption == '8':
        customer_name = input("Enter customer's name to delete: ")
        delete_customer(customer_name)
    elif selectOption == '9':
        book_title = input("Enter book's title to delete: ")
        delete_book(book_title)
    else: 
        print ('Invalid Option')
    main()

if __name__ == '__main__':
    main()

conn.close()


   
