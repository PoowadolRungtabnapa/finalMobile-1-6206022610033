import pymysql
from werkzeug.wrappers import Request, Response
from flask import flash, render_template, request
from flask import jsonify
from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'appdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def hello():
    return """
    Flask API !<br>
    <a href='/new_user'>add</a>insert new<br>
    <a href='/appdb'>appdb</a>Show all<br>
    <b>/create</b> Insert new Record<br>
    <b>/appdb/<id></b> get by ID<br>
    <b>/update/<id></b> Edit info<br>
    <b>/delete/<id></b> Delete by  ID<br>
    """
@app.route('/new_user')
def add_user_view():
    return render_template('add.html')

@app.route('/create', methods=['POST'])
def create_appdb():
    try:        
        _json = request.json
        print(_json)
        _type = _json['type']
        _description = _json['description']
        _amount = _json['amount']
        if _type and _description and _amount and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO appdb(type, description, amount) VALUES(%s, %s, %s)"
            bindData = (_type, _description, _amount)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee added successfully!')
            respone.status_code = 200
            #flash('User added successfully!')
            #redirect('/')
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close() 
        if conn:
            conn.close()
        
@app.route('/appdb')
def appdb():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, type, description, amount, createdAt FROM appdb")
        appdbRows = cursor.fetchall()
        respone = jsonify(appdbRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close() 
        if conn:
            conn.close() 

@app.route('/appdb/<int:appdb_id>')
def appdb_details(appdb_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, type, description, amount, createAt FROM appdb WHERE id =%s", appdb_id)
        appdbRow = cursor.fetchone()
        respone = jsonify(appdbRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close() 
        if conn:
            conn.close()

@app.route('/update/<int:appdb_id>', methods=['PUT'])
def update_appdb(appdb_id):
    try:
        _json = request.json
        #_id = _json['id']
        _type = _json['type']
        _description = _json['description']
        _amount = _json['amount']
        if _type and _description and _amount  and appdb_id and request.method == 'PUT':
            sqlQuery = "UPDATE appdb SET name=%s, description=%s, amount=%s, WHERE id=%s"
            bindData = (_type, _description, _amount, appdb_id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close() 
        if conn:
            conn.close()

@app.route('/delete/<int:appdb_id>', methods=['DELETE'])
def delete_appdb(appdb_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appdb WHERE id =%s", (appdb_id,))
        conn.commit()
        respone = jsonify('Employee deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close() 
        if conn:
            conn.close()      

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app.debug = True
    run_simple('localhost',80, app)