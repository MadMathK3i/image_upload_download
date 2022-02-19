#app.py
from flask import Flask, render_template, redirect, request, flash
import flask
from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
from werkzeug.utils import secure_filename
import os
#import magic
#import urllib.request
from datetime import datetime
 
app = Flask(__name__)
       
app.secret_key = "caircocoders-ednalan"
       
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'testingdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
 
UPLOAD_FOLDER = 'static/uploads'
DOWNLOAD_FOLDER = 'static/downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
  
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
 
@app.route('/',methods=["POST","GET"])
def index():
    return render_template('index.html')
 
@app.route("/upload",methods=["POST"])
def upload():

    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    print("app...")

    #file = request.form.get('image')
    #file = flask.request.files.get('image')
    #file = request.form.get('image')
    file = request.files['image']

#    if file and allowed_file(file.filename):
    if file:
        #filename = secure_filename(file.filename)
        filename = file.filename 
        print(filename)
        s_filename = filename
        filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filename)

        empPicture = convertToBinaryData(filename)
        cur.execute("INSERT INTO Python_Employee (name, photo) VALUES (%s, %s)",[s_filename, empPicture])

        mysql.connection.commit()

        '''
        print(s_filename)

        cur.execute("select * from python_employee where name = %s", [s_filename])

        record = cur.fetchall()
        for row in record:
            image = row['photo']
            print("storing employee image and bio-data on disk \n")
            write_file(image, os.path.join(app.config['DOWNLOAD_FOLDER'], s_filename))
        '''

    cur.close()   

    flash('File(s) successfully uploaded')    

    return redirect('/')

# どうファイル名をとるか...
@app.route("/download",methods=["POST"])
def download():

    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    print("app...")

    s_filename = 'alla-san.png'

    cur.execute("select * from Python_Employee where name = %s", [s_filename])

    record = cur.fetchall()
    for row in record:
        image = row['photo']
        print("storing employee image and bio-data on disk \n")
        write_file(image, os.path.join(app.config['DOWNLOAD_FOLDER'], s_filename))

    flash('File(s) successfully download')    

    return s_filename 
    #return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)