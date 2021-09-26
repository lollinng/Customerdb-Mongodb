import mysql.connector as sql
import pymongo
# connection = sql.connect(
#                 host = 'localhost',
#                 port = '3306',
#                 user = 'user1',
#                 password = 'password',
#                 database = 'learn_website'
#             )

class DBHELPER:
    def __init__(self):

        client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        mydb = client['Employee']
        global information 
        information = mydb.employeeinformation       # table name

    def insert_user(self,username,email,phone,products,shopping_value):
        record = {
            'name':username,
            'email':email,
            'phone':phone,
            'products':products,
            'shopping_value':shopping_value
        }
        information.insert_one(record)
        print('user saved to db')

    def fetch_all(self):
        dataset = information.find({})
        return dataset

    def delete_user(self,email):
        print(email)
        information.delete_one(
            { "email": email} 
        )


    def update_user(self,new_name, new_email, new_phone,new_products,new_shopping_value):
        information.update_one(
            {"name":new_name},
                {"$set":{
                    "name":new_name,
                    "email":new_email,
                    "phone":new_phone,
                    'products':new_products,
                    'shopping_value':new_shopping_value
                }}
        )
        print("Userid {} updated !".format(new_name))
