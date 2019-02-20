
import pymysql
cnx = pymysql.connect(port=7777,
                                host='127.0.0.1',
                                database='dictionary_data')
cursor= cnx.cursor()
result = cursor.fetchall()
print(result)

cnx.close()
