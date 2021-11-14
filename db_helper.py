import pymongo

class DBHELPER:
    def __init__(self):
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        mydb = client['Customer_Database']
        global information 
        information = mydb.customerinformation       # table name

    def insert_user(
            self,username, email, phone,no_products,
            product1,productname1,productprice1,category1,
            product2,productname2,productprice2,category2,
            product3,productname3,productprice3,category3 
    ):  
        
        if productprice2 == '':
            productprice2 = 0
        if productprice3 == '':
            productprice3 = 0

        record = {
            'name':username,
            'email':email,
            'phone':phone,
            'no_products':no_products,
            'products':[
                {'product':product1,'productname':productname1,'productprice':productprice1,'category':category1},
                {'product':product2,'productname':productname2,'productprice':productprice2,'category':category2},
                {'product':product3,'productname':productname3,'productprice':productprice3,'category':category3},
                ],
            'shopping_value': int(productprice1) + int(productprice2) + int(productprice3)
        }
        information.insert_one(record)
        print('user saved to db')

    def fetch_user(self,email):
        for record in information.find({'email':email}):
            return record

    def fetch_all(self):
        dataset = information.find({})
        return dataset

    def delete_user(self,email):
        print(email)
        information.delete_one(
            { "email": email} 
        )

    def update_user(
        self,username, email, phone,no_products,
            product1,productname1,productprice1,category1,
            product2,productname2,productprice2,category2,
            product3,productname3,productprice3,category3,
    ):
    
        if productprice2 == '':
            productprice2 = 0
            if productprice3 == '':
                productprice3 = 0

        information.update_one(
            {"email":email},
            {
                "$set":{
                    "name":username,
                    "email":email,
                    "phone":phone,
                    'no_products':no_products,
                    'products':[
                        {'product':product1,'productname':productname1,'productprice':productprice1,'category':category1},
                        {'product':product2,'productname':productname2,'productprice':productprice2,'category':category2},
                        {'product':product3,'productname':productname3,'productprice':productprice3,'category':category3}
                    ],
                    'shopping_value' : int(productprice1) + int(productprice2) + int(productprice3)
                }
            }
        )
        print("Userid {} updated !".format(username))
