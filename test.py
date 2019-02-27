import requests
from bs4 import BeautifulSoup
import time
import threading
import csv

missing_link=list()
missing_page_link = list()
def get_meaning(letter_link):
    has_next_page = True
    while has_next_page:
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
                        print(to_write)
                        to_write=list()
            try:
                print("here")
                pagination_links = next_page_soup.find("div", class_="pagination").find_all('a')
                print(bool(pagination_links))
                letter_link = pagination(pagination_links)
                print(letter_link)
            except:
                letter_link = None

            if letter_link == None:
                has_next_page = False
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
        # print(word_meaning)
    except:
        try:
            word_meaning_link_req = requests.get(word_meaning_link)
            word_meaning_soup = BeautifulSoup(word_meaning_link_req.content, "lxml")
            word_meaning = word_meaning_soup.find("div", id="w_info").find("span", class_="meaning").text
            # print(word_meaning)
        except Exception as ex:
            try:
                word_meaning_link_req = requests.get(word_meaning_link)
                word_meaning_soup = BeautifulSoup(word_meaning_link_req.content, "lxml")
                word_meaning = word_meaning_soup.find("div", class_="word_info").find("div", class_="mgs").text
                # print(word_meaning)
            except:
                word_meaning=None
                missing_link.append(word_meaning_link)
                print(missing_link)
                print(len(missing_link))

    return word_meaning

def pagination(pagination_links):
    letter_link = None
    if bool(pagination_links):
        next = list()
        for i in pagination_links:
            element = {i.text: i.get('href')}
            next.append(element)
            element = dict()
        print(next)
        for j in next:
            print(j)
            if "Next &gt;" in j or "Next >" in j or "Last" in j:
                if "Next &gt;" in j:
                    letter_link = j["Next &gt;"]
                    print(letter_link)
                    return letter_link
                elif "Next >" in j:
                    letter_link = j["Next >"]
                    print(letter_link)
                    return letter_link
                elif "Last" in j:
                    letter_link = j["Last"]
                    print(letter_link)
                    return letter_link
            else:
                letter_link = None
    else:
        letter_link = None
    return letter_link

if __name__ == "__main__":
    threads_list = []

    r = requests.get("http://www.english-bangla.com/browse")
    print(r.status_code)
    soup = BeautifulSoup(r.content, "lxml")

    alphabt_link = soup.find("div", id="cat_page").find("div", class_="a-z").find_all('a')

    for letter in alphabt_link:
        letter_link = letter.get('href')
        # print(letter_link)
        t = threading.Thread(target=get_meaning, args=(letter_link,))
        threads_list.append(t)
        t.start()
    # get_meaning('http://www.english-bangla.com/browse/index/i/2')
    # for word_link in missing_link:

