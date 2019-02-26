from flask import Flask, render_template
import pymysql
import json

db = pymysql.connect(user="root", passwd="", host="localhost", database="dictionary_data")
print("connection success....")
mycursor = db.cursor()
sql = "SELECT * FROM english_bangle_word_meaning"
mycursor.execute(sql)
data = mycursor.fetchall()

app = Flask(__name__)


@app.route('/')
def index():

    return render_template('home.html', data = data)


@app.route('/About')
def about():
    return render_template('about.html', data = data)

if __name__ == '__main__':

     app.run(debug=True)