from flask import Flask, jsonify, request,render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
import yaml

db=yaml.load(open('database_details.yaml'))

#initializing 
app=Flask(__name__)
#config Mysql
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']
#cursor class not neccessary exactly but it helps to get the data in dictionay
#format, normally it just return tuples, but dict is more easy to read.
# app.config['MYSQL_CURSORCLASS']='DictCursor'

#instantiating mysqldb
mysql = MySQL(app)

@app.route('/home',methods=['GET'])
def data():
    if request.method =='GET':
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM example")
        userDetails = cur.fetchall()

        return render_template('users.html', userDetails=userDetails)



@app.route('/post',methods=['GET','POST'])
def post():
    if request.method =='POST':
        userdetail = request.form
        name = userdetail['username']
        age = userdetail['age']
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''CREATE TABLE example(name VARCHAR(20), age INTEGER)''')
        except Exception as e:
            pass
        finally:
            cursor.execute('''INSERT INTO example VALUES(%s, %s)''',(name,age))
            mysql.connection.commit()
            cursor.close()
        
        return redirect('/home')
    return render_template('index.html')

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method=='POST':
        userdetail = request.form
        name = userdetail['username']
        age = userdetail['age']
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE example SET age=%s WHERE name=%s''',(age,name))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('data'))
    return render_template('update.html')


@app.route('/delete',methods=['POST','GET'])
def delete():
    if request.method=='POST':
        userdetail = request.form
        name = userdetail['user']
        cursor = mysql.connection.cursor()
        #In the below (name,) means to unpack the values
        cursor.execute("DELETE FROM example WHERE name=%s",(name))
        '''You need to add a trailing comma to your query to pass a tuple,
         rather than a string as an argument.'''
        # flash("deleted successfully")
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('data'))
    return render_template('del.html')
if __name__ == '__main__':
    app.run(debug=True)