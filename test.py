
import pymysql

try:
    db = pymysql.connect(user="root", passwd="", host="localhost", database="dictionary_data")
    print("connection success....")
    mycursor = db.cursor()

    sql = "INSERT INTO english_bangle_word_meaning (word, meaning) VALUES (%s, %s)"
    val = ("John", "Highway 21")
    mycursor.execute(sql, val)

    db.commit()
    print("1 record inserted, ID:", mycursor.lastrowid)
    db.close()


except:
    print("opsss....")