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
        products = request.form['products']
        shopping_value = request.form['shopping_value']

        helper.insert_user(name, email, phone,products,shopping_value)
        flash("Customer Data Inserted Successfully")
        return redirect(url_for('Index'))

#this is our update route where we are going to update our customer
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        new_name = request.form['name']
        new_email = request.form['email']
        new_phone = request.form['phone']
        new_products = request.form['products']
        new_shopping_value = request.form['shopping_value']

        helper.update_user(new_name, new_email, new_phone,new_products,new_shopping_value)
        flash("Customer Data Updated Successfully")

        return redirect(url_for('Index'))

#This route is for deleting our customer
@app.route('/delete/<email>/', methods = ['GET', 'POST'])
def delete(email):
    helper.delete_user(email)
    flash("Customer Data Deleted Successfully")
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
