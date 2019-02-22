import requests
from bs4 import BeautifulSoup
import time
import pymysql
try:
    db = pymysql.connect(user="root", passwd="", host="localhost", database="dictionary_data")
    print("connection success....")
    mycursor = db.cursor()
    sql = "INSERT INTO english_bangle_word_meaning (word, meaning) VALUES (%s, %s)"

except:
    print("opsss....")

r = requests.get("http://www.english-bangla.com/browse")
# print(r.status_code)
soup = BeautifulSoup(r.content, "lxml")

alphabt_link = soup.find("div", id="cat_page").find("div", class_="a-z").find_all('a')
for letter in alphabt_link:
    letter_link =letter.get('href')
    # print(letter_link)
    letter_link_req = requests.get(letter_link)
    letter_link_soup = BeautifulSoup(letter_link_req.content, "lxml")
    letter = letter_link_soup.find("div", id="cat_page").find("ul").find_all('a')
    for i in letter:
        print(i.text)
        word = i.text
        letter_meaning_link = i.get('href')
        letter_meaning_link_req = requests.get(letter_meaning_link)
        letter_meaning_soup = BeautifulSoup(letter_meaning_link_req.content, "lxml")
        try:
            letter_meaning = letter_meaning_soup.find("div", id="w_info").find("span", class_="format1").text
            print(letter_meaning)
            val = (word, letter_meaning)
            mycursor.execute(sql, val)
            db.commit()
        except:
            try:
                letter_meaning = letter_meaning_soup.find("div", id="w_info").find("span", class_="meaning").text
                print(letter_meaning)
                val = (word, letter_meaning)
                mycursor.execute(sql, val)
                db.commit()

            except:
                print("Not a valid word")
                val = (word, "Not a valid word")
                mycursor.execute(sql, val)
                db.commit()
    try:
        next_page_link = letter_link_soup.find("div", class_="pagination").find('a')
    except:
        next_page_link = None

    while 1:
        if next_page_link == None:
            break
        else:
            # print(next_page_link)
            next_page_req = requests.get(next_page_link.get('href'))
            next_page_soup = BeautifulSoup(next_page_req.content, "lxml")
            letter = next_page_soup.find("div", id="cat_page").find("ul").find_all('a')
            for i in letter:
                print(i.text)
                word = i.text
                letter_meaning_link = i.get('href')
                try:
                    letter_meaning_link_req = requests.get(letter_meaning_link)
                    letter_meaning_soup = BeautifulSoup(letter_meaning_link_req.content, "lxml")


                except:
                    time.sleep(3)
                    letter_meaning_link_req = requests.get(letter_meaning_link)
                    letter_meaning_soup = BeautifulSoup(letter_meaning_link_req.content, "lxml")

                try:
                    letter_meaning = letter_meaning_soup.find("div", id="w_info").find("span", class_="format1").text
                    print(letter_meaning)
                    val = (word, letter_meaning)
                    mycursor.execute(sql, val)
                    db.commit()
                except:
                    try:
                        letter_meaning = letter_meaning_soup.find("div", id="w_info").find("span",
                                                                                           class_="meaning").text
                        print(letter_meaning)
                        val = (word, letter_meaning)
                        mycursor.execute(sql, val)
                        db.commit()
                    except:
                        print("Not a valid word")
                        val = (word, "Not a valid word")
                        mycursor.execute(sql, val)
                        db.commit()


            try:
                pagination_links = next_page_soup.find("div", class_="pagination").find_all('a')
                for i in pagination_links:
                    if i.text == "Next >":
                        next_page_link = i
                        break
                    else:
                        next_page_link = None

            except:
                pass