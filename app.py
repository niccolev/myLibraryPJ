from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, url_for
from sqlalchemy import ForeignKey
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_library.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ CREATES CUSTOMER TABLE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""Creates Customers Table"""
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customerName = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(30), nullable = False)
    age = db.Column(db.Integer, nullable=False)
    customer_loans = db.relationship('Loans', backref='customers', lazy=True)

    def __init__(self, customerName, city, age):
        self.customerName = customerName
        self.city = city
        self.age = age

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ CREATES BOOKS TABLE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""Creates Books Table"""
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookName = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    yearPublished = db.Column(db.Integer, nullable=False)
    Type = db.Column(db.Integer, nullable=False)
    book_loans = db.relationship('Loans', backref='books', lazy=True)

    def __init__(self, bookName, author, yearPublished, Type):
        self.bookName = bookName
        self.author = author
        self.yearPublished = yearPublished
        self.Type = Type

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ CREATES LOANS TABLE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""Creates Loans Table -- with foreign keys from Books table and Customers table"""
class Loans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),
        nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'),
        nullable=False)
    loan_date = db.Column(db.Integer, nullable=False)
    return_date = db.Column(db.Integer, nullable = False)

    def __init__(self,customer_id,book_id,loan_date,return_date):
        self.customer_id=customer_id
        self.book_id=book_id
        self.return_date=return_date
        self.loan_date=loan_date

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ MAIN DEFAULT HOME PAGE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""URLS and FUNCTIONS (ADD, DELETE, DISPLAY ALL, FIND BY NAME, """

@app.route("/home")
@app.route("/")
def home():
    return render_template('layout.html')

#                                     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                                     @@@@@@@@@@@@ BOOKS FUNCTIONS @@@@@@@@@@@@@@
#                                     @@@@@@@@@@@@@@@@@ BELOW @@@@@@@@@@@@@@@@@@@
#                                     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ FUNCTION THAT DISPLAYS ALL BOOKS AVAIALABLE  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""Returns whole dict of Books"""
@app.route("/books/")
def all_books():
    return render_template('allBooks.html', book_list = Books.query.all()) 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ SEARCH A BOOK BY ITS NAME @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""Find book by name"""
@app.route("/findbook/", methods = ['GET', 'POST'])
def find_book(bookName=""):
    bookNames=[]
    if request.method == "POST":
        bookName = request.form
        for book in db.session.query(Books).filter_by(bookName=bookName['bkname']):
            bookNames.append(book)
    return render_template('findbook.html', bookNames=bookNames)

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ADDS A NEW BOOK TO BOOK TABLE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""function that adds a new book to the Books table"""
@app.route("/addbook/", methods = ['GET', 'POST'])
def add_book():
    if request.method=='POST':
            new_book=request.form
            newBook=Books(new_book['bkname'], new_book['author'], new_book['yrpublished'], new_book['type'])
            db.session.add(newBook)
            db.session.commit()
    return render_template('addbook.html')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ FUNCTION THAT DELETES A BOOK FROM BOOK TABLE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@app.route("/deletebook/<ind>", methods = ['DELETE', 'GET', 'POST'])
def delete_book(ind=-1):
    book = Books.query.get(int(ind))
    if book:
        db.session.delete(book)
        db.session.commit()
    return render_template('deletebook.html')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


#                                     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                                     @@@@@@@@@@@ CUSTOMER FUNCTIONS @@@@@@@@@@@@
#                                     @@@@@@@@@@@@@@@@@ BELOW @@@@@@@@@@@@@@@@@@@
#                                     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ FUNCTION THAT DISPLAYS ALL REGISTERED CUSTOMERS  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""Returns all dict of Customers"""
@app.route("/customers/", methods = ['GET', 'POST'])
def customers():
    return render_template('allCustomers.html', customers_list = Customers.query.all())

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ SEARCH A CUSTOMER BY HIS NAME @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""Find customer by name"""
@app.route("/findcustomer/", methods = ['GET', 'POST'])
def find_customer():
    custNames=[]
    if request.method == "POST":
        custName = request.form
        for cust in db.session.query(Customers).filter_by(customerName=custName['thename']):
            custNames.append(cust)
    return render_template('findcustomer.html', custNames=custNames)

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ADDS A NEW CUSTOMER TO CUSTOMER TABLE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""function that adds a new customer to the Customers table"""
@app.route("/addcustomer/", methods = ['GET', 'POST'])
def add_customer():
    if request.method=='POST':
        new_customer=request.form
        newCustomer=Customers(new_customer['custname'],new_customer['city'],new_customer['age'])
        db.session.add(newCustomer)
        db.session.commit()
    return render_template('addcustomer.html')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ FUNCTION THAT DELETES A CUSTOMER FROM CUSTOMER TABLE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@app.route("/deletecustomer/<ind>", methods = ['DELETE', 'GET', 'POST'])
def delete_customer(ind=-1):
    cust = Customers.query.get(int(ind))
    if cust:
        db.session.delete(cust)
        db.session.commit()
    return render_template('deletecustomer.html')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


#                                     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#                                     @@@@@@@@@@@ LOANS FUNCTIONS @@@@@@@@@@@@
#                                     @@@@@@@@@@@@@@@@@ BELOW @@@@@@@@@@@@@@@@@@@
#                                     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ FUNCTION THAT DISPLAYS ALL LOANS  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""Returns whole dict of Loans"""
@app.route("/loans")
def all_loans():
    return render_template('allLoans.html', loan_list = Loans.query.all())

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ FUNCTION THAT DISPLAYS ALL LATE LOANS  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@app.route("/lateloans/", methods=['GET'])
def late_loans():
    lateloans=[]
    database= db.session.query(Loans, Books, Customers). \
        select_from(Loans).join(Books).join(Customers).all()
    for loan, book, customer in database:
        if datetime.datetime.strptime(loan.return_date, '%Y-%m-%d').date() < datetime.date.today():
            lateloan={"loanid":loan.id,"bookname":book.bookName,"customername":customer.customerName,"returndate":loan.return_date,"loandate":loan.loan_date}
            lateloans.append(lateloan)
    return render_template('lateloans.html', lateloans=lateloans)

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ADDS A NEW LOAN TO LOANS TABLE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

"""Adds a new loan"""
@app.route("/addloan/", methods=['POST','GET'])
def add_loan():
    if request.method=='POST':
        todays_date=datetime.date.today()
        new_loan=request.form
        for book in db.session.query(Books).filter_by(id=new_loan['book_id']):
            book2loan = book
        if book2loan.Type == 1:
            return_date = todays_date + datetime.timedelta(days = 3)
        elif book2loan.Type == 2:
            return_date = todays_date + datetime.timedelta(days = 7)
        else:
            return_date = todays_date + datetime.timedelta(days = 10)
        newLoan=Loans(new_loan['customer_id'], new_loan['book_id'],todays_date,return_date )
        db.session.add(newLoan)
        db.session.commit()
    return render_template('addloan.html')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ RETURNS/DELETES A LOAN FROM LOANS TABLE @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@app.route("/returnloan/", methods=['POST','GET'])
@app.route("/returnloan/<ind>/", methods=['DELETE','GET'])
def return_loan(ind=-1):
# if int(ind)>0:
    book2return=Loans.query.get(int(ind))
    if book2return:
        db.session.delete(book2return)
        db.session.commit()
        return render_template('returnloan.html',id=id)

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ END OF FUNCTIONS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)