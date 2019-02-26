import requests
from bs4 import BeautifulSoup
import time
import threading
import csv

missing_link=list()
missing_page_link = list()
def get_meaning(letter_link):
    while 1:
        try:
            # print(letter_link)
            next_page_req = requests.get(letter_link)
            next_page_soup = BeautifulSoup(next_page_req.content, "lxml")
            word = next_page_soup.find("div", id="cat_page").find("ul").find_all('a')
            for i in word:
                # print(i.text)
                to_write = list()
                to_write.append(i.text)
                word_meaning_link = i.get('href')
                meaning = get_particular_meaning(word_meaning_link)
                if meaning!=None:
                    to_write.append(meaning)
                    my_file = open('word_meaning.csv', 'a', encoding="utf-8")
                    with my_file:
                        writer = csv.writer(my_file,delimiter=',', lineterminator='\n')
                        writer.writerow(to_write)
                        to_write=list()
            try:
                pagination_links = next_page_soup.find("div", class_="pagination").find_all('a')
                for i in pagination_links:
                    if i.text == "Next &gt":
                        letter_link = i
                        break
                    else:
                        letter_link = None
            except:
                pass

            if letter_link == None:
                break
        except Exception as ex:
            print(ex)
            missing_page_link.append(letter_link)
            print(letter_link)
            my_file = open('missing_link.csv', 'a')
            with my_file:
                writer = csv.writer(my_file, delimiter=',', lineterminator='\n')
                writer.writerow(letter_link)
            print('pages: ',len(missing_page_link))

def get_particular_meaning(word_meaning_link):
    try:
        word_meaning_link_req = requests.get(word_meaning_link)
        word_meaning_soup = BeautifulSoup(word_meaning_link_req.content, "lxml")
        word_meaning = word_meaning_soup.find("div", id="w_info").find("span", class_="format1").text
        print(word_meaning)
    except:
        try:
            word_meaning_link_req = requests.get(word_meaning_link)
            word_meaning_soup = BeautifulSoup(word_meaning_link_req.content, "lxml")
            word_meaning = word_meaning_soup.find("div", id="w_info").find("span", class_="meaning").text
            print(word_meaning)
        except Exception as ex:
            try:
                word_meaning_link_req = requests.get(word_meaning_link)
                word_meaning_soup = BeautifulSoup(word_meaning_link_req.content, "lxml")
                word_meaning = word_meaning_soup.find("div", class_="word_info").find("div", class_="mgs").text
                print(word_meaning)
            except:
                word_meaning=None
                missing_link.append(word_meaning_link)
                print(missing_link)
                print(len(missing_link))

    return word_meaning
if __name__ == "__main__":
    threads = []

    r = requests.get("http://www.english-bangla.com/browse")
    print(r.status_code)
    soup = BeautifulSoup(r.content, "lxml")

    alphabt_link = soup.find("div", id="cat_page").find("div", class_="a-z").find_all('a')

    for letter in alphabt_link:
        # print(letter)
        # for value in values:
        letter_link = letter.get('href')
        print(letter_link)
        t = threading.Thread(target=get_meaning, args=(letter_link,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  # Wait until thread terminates its task

    # for word_link in missing_link:

