# Import flask and its components
from flask import *
import os

# Import the pymysql - it helps us create connection between python flask and mysql database.
import pymysql

# Create a flask application and give it a name,
app = Flask(__name__)

# Configure the location to where your product images willl be saved
app.config["UPLOAD_FOLDER"] = "static/images"


# Below is the sign up route
@app.route("/api/signup", methods = ["POST"])
def signup():
    if request.method == "POST":
        # Extract the different details entered on the form
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]

        # By use of the print function let's print all those details sent withthe upcoming request.
        # print(username,email,password,phone)

        # establish a connection btwn flask/python and mysql
        connection = pymysql.connect(host="localhost", user="root", password="", database="sokogardenonline")

        # Create a cursor to execute the sql queries
        cursor = connection.cursor()

        # Structure an sql to insert the details received from the form.
        sql = "INSERT INTO users(username,email,phone,password) VALUES(%s, %s, %s, %s)"

        # Create a tuple that will hold all the data gotten from the form
        data = (username, email, phone, password)

        # By use of the cursor,execute the sql as you replace the placholder with the actual value.
        cursor.execute(sql,data)

        # Commit the changes to the database
        connection.commit()

        return jsonify({"message" : "User registered successfully."})


# Below is the login/sign in route.
@app.route("/api/signin", methods = ["POST"])
def signin():
    if request.method == "POST":
        # Extract the two details entered on the form
        email = request.form["email"]
        password = request.form["password"]

        # Print out the details on the form
        # print(email,password)
        # Create/establish a connection.
        connection = pymysql.connect(host="localhost",user="root",password="",database="sokogardenonline")

        # Create a cursor
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        # Structure the sql query that will whether the email and password entered are correct.
        sql = "SELECT * FROM users WHERE  email = %s AND password = %s"

        # Put the data received from the form into a tuple.
        data = (email,password)

        # By use of the cursor execute the sql
        cursor.execute(sql,data)


        # Check whether there are rows returned and store the on a variable
        count = cursor.rowcount
        #  print(count)

        # If there are records returned,the password and the email are correct,otherwise,they are wrong
        if count == 0:
            return jsonify({"message" : "Login Failed"})
        else:
            # There must be  a user so we create a variable that will hold the details of the user fetched from the database.
            user=cursor.fetchone()
            # Return the details to the front end as well as a message
            return jsonify({"message" : "User Logged In Successfully", "user":user})





# Below is the roure for adding products
@app.route("/api/add_product", methods = ["POST"])
def Addproducts():
    if request.method == "POST":
        # Extract the data entered on the form
        product_name = request.form["product_name"]
        product_description= request.form["product_description"]
        product_cost = request.form["product_cost"]
        # For the product photo, we fetch it from files as shown below.
        product_photo = request.files["product_photo"]

        # Extract the filename of the product photo
        filename = product_photo.filename
        # By use of the OS module,we can extract the file path where the image is currentlysaved.
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Save the product photo image into the new location
        product_photo.save(photo_path)

        # Print them out to test whether you are receiving the details sent with the request.
        # print(product_name,product_description,product_cost,product_photo)

        # Establish a connection to theDB
        connection = pymysql.connect(host="localhost",user="root",password="",database="sokogardenonline")

        # Create a cursor
        cursor = connection.cursor()

        # Structure the 
        sql = "INSERT INTO product_details(product_name, product_description, product_cost, product_photo) VALUES (%s, %s, %s, %s)"

         # Create a tuple that will hold the data which are currently held onto the different varible declared.
        data = (product_name, product_description, product_cost, filename)

        # Use the cursor execute the sql as you replace the placeholder with the actual data.
        cursor.execute(sql,data)

        # Commit the changes to the database
        connection.commit()




        return jsonify({"message" : "Product Added Successfully."})





# Run the application.
app.run(debug=True)