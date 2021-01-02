from flask import Flask, render_template, request, jsonify
from flaskext.mysql import MySQL
import envirunment as env


app = Flask(__name__)

# configuration for MySQL 
app.config['MYSQL_DATABASE_USER'] = env.MYSQL_DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = env.MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = env.MYSQL_DATABASE_DB
app.config['MYSQL_DATABASE_HOST'] = env.MYSQL_DATABASE_HOST

mysql = MySQL()
mysql.init_app(app)


@app.route('/insert', methods=['POST'])

def insert():
    """ data insert in to database """

    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        phoneNumber = details['phnumber']

        conn = mysql.connect() # Start to connecting into database 
        cur = conn.cursor()

        repeat_query = "SELECT firstName FROM MyUsers"
        cur.execute(repeat_query)
        repeat_var = str(cur.fetchall())

        if firstName not in repeat_var: # Check for duplicate data
            query = "INSERT INTO MyUsers(firstName, lastName, phoneNumber) VALUES (%s, %s, %s)"
            value = (firstName, lastName, phoneNumber)
            cur.execute(query, value)
            cur.connection.commit()
        else:
            return jsonify({"message " : "data is repeated" })

        cur.close()

    return jsonify({"message" : "data successfully inserted "})    


@app.route('/update', methods=['POST'])

def update():
    details = request.form
    firstName = details['fname']
    lastName = details['lname']
    rname = details['rname']
    rfamily = details['rfamily']
    rphone = details['rphone']

    if firstName and rname and rfamily and rphone:
        conn = mysql.connect()
        cur = conn.cursor()
        repeat_query = "SELECT firstName FROM MyUsers"
        cur.execute(repeat_query)
        repeat_var = str(cur.fetchall())
    else:
        return jsonify({"message" : "all filed is required !"})

    if firstName in repeat_var and rname not in repeat_var:
        query = "UPDATE `MyUsers` SET `firstName`=%s,`lastName`=%s `phoneNumber`=%s WHERE `firstName`=%s "
        value = (rname, rfamily, rphone, firstName)
        cur.execute(query, value)
        cur.connection.commit()
        return jsonify({"message" : "data updated "})
    else:
        return jsonify({"message " : "User not found !, or replace parameter is repeated" })

    cur.close()


@app.route('/list', methods=['GET','POST'])

def list():
    conn = mysql.connect()
    cur = conn.cursor()
    query = "SELECT * FROM MyUsers"
    cur.execute(query)
    data = sorted(cur.fetchall())
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True)
