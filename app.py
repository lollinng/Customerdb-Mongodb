from flask import Flask, render_template, request, redirect, url_for, flash
from db_helper import DBHELPER

app = Flask(__name__)
app.secret_key = "Secret Key"
helper = DBHELPER()

#This is the index route where we are going to
#query on all our customer data
@app.route('/')
def Index():
    all_data = helper.fetch_all()
    return render_template("index.html", customer = all_data)

#this route is for inserting data to mongodb database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        no_products = request.form['no_products']
        
        product1 = request.form['product1']
        productname1 = request.form['productname1']
        productprice1 = request.form['productprice1']
        category1 = request.form['category1']

        product2 = request.form['product2']
        productname2 = request.form['productname2']
        productprice2 = request.form['productprice2']
        category2 = request.form['category2']

        product3 = request.form['product3']
        productname3 = request.form['productname3']
        productprice3 = request.form['productprice3']
        category3 = request.form['category3']

        helper.insert_user(            
            name, email, phone,no_products,
            product1,productname1,productprice1,category1,
            product2,productname2,productprice2,category2,
            product3,productname3,productprice3,category3,
        )
        
        flash("Customer Data Inserted Successfully")
        return redirect(url_for('Index'))

#this is our update route where we are going to update our customer
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        no_products = request.form['no_products']
        
        product1 = request.form['product1']
        productname1 = request.form['productname1']
        productprice1 = request.form['productprice1']
        category1 = request.form['category1']

        product2 = request.form['product2']
        productname2 = request.form['productname2']
        productprice2 = request.form['productprice2']
        category2 = request.form['category2']

        product3 = request.form['product3']
        productname3 = request.form['productname3']
        productprice3 = request.form['productprice3']
        category3 = request.form['category3']
        

        helper.update_user(
            name, email, phone,no_products,
            product1,productname1,productprice1,category1,
            product2,productname2,productprice2,category2,
            product3,productname3,productprice3,category3,
        )
        flash("Customer Data Updated Successfully")

        return redirect(url_for('Index'))

#This route is for deleting our customer
@app.route('/delete/<email>/', methods = ['GET', 'POST'])
def delete(email):
    helper.delete_user(email)
    flash("Customer Data Deleted Successfully")
    return redirect(url_for('Index'))

# This route is for getting the details of the customer
@app.route('/details/<email>/', methods = ['GET', 'POST'])
def details(email):
    all_data = helper.fetch_user(email)
    return render_template("details.html", customer = all_data)

if __name__ == "__main__":
    app.run(debug=True)
