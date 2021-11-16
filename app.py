from flask import Flask, render_template, request, redirect, url_for, flash,session
import bcrypt
from db_helper import DBHELPER
import pymongo


app = Flask(__name__)
helper = DBHELPER()
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
mydb = client['Customer_Database']
user = mydb.user_login
admins = mydb.admin_login  

@app.route('/admin')
def admin():
    all_data = helper.fetch_all()
    return render_template("index.html", customer = all_data,type = 'admin')


@app.route('/', methods = ['GET','POST'])
def login():
    session.clear()
    if request.method == 'POST':

        admin_check = request.form.get('mycheckbox')
        if admin_check == 'admin':
            login_admin = admins.find_one({'email' : request.form['email']})
            if login_admin:
                if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_admin['password']) == login_admin['password']:
                    session['admin'] = True
                    session['email'] = request.form['email']
                    return redirect(url_for('admin'))
            else: flash('You are not admin please untick the box !')
            return render_template("auth.html")

        login_user = user.find_one({'email' : request.form['email']})
        if login_user: 
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['admin'] = False
                session['email'] = request.form['email']
                return redirect(url_for("details",email = session['email']))

        flash('Invalid username/password combination')
    return render_template("auth.html")

@app.route('/register/',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        print('sup')
        # if  session.get("USERNAME")
        if session.get('admin')  is not None:
            existing_user = admins.find_one({'email' : request.form['email']})
            print('admin he is')
        else:
            existing_user = user.find_one({'email' : request.form['email']})
            print('not admin')

        if existing_user is None:
            if request.form['pass1'] == request.form['pass2']:
                hashpass = bcrypt.hashpw(request.form['pass1'].encode('utf-8'), bcrypt.gensalt())
                if session.get('admin')  is not None:
                    admins.insert_one({
                    'name' : request.form['username'],
                    'email':request.form['email'], 
                    'phone' : request.form['phone'],  
                    'password' : hashpass
                    })
                    session['email'] = request.form['email']
                    return redirect(url_for('admin'))
                else:
                    user.insert_one({
                        'name' : request.form['username'],
                        'email':request.form['email'], 
                        'phone' : request.form['phone'],  
                        'password' : hashpass
                    })
                    session['email'] = request.form['email']
                    session['admin'] = False
                    return redirect(url_for('details',email=session['email']))
            else : flash("Please type the same password!")
        else: flash("That Email id already exists!")
    return render_template("register.html")


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
        if session['admin'] == True:
            return redirect(url_for('Index',type = 'admin'))
        else:
            print('hi')

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

        return redirect(url_for('admin'))

#This route is for deleting our customer
@app.route('/delete/<email>/', methods = ['GET', 'POST'])
def delete(email):
    helper.delete_user(email)
    flash("Customer Data Deleted Successfully")
    return redirect(url_for('admin'))

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        email = request.form['email']
        data = helper.fetch_user(email)
        return render_template("details.html", customer = data,type='admin')

# This route is for getting the details of the customer
@app.route('/details/<email>/', methods = ['GET', 'POST'])
def details(email):
    if session['admin'] == True:
        data = helper.fetch_user(email)
        return render_template("details.html", customer = data,type='admin')
    else:
        for record in user.find({'email':email}):
            data = record 
        return render_template("details.html", customer = data,type='0')





if __name__ == "__main__":
    app.secret_key = "Secret Key"
    app.run(debug=True)
