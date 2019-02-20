import requests
from bs4 import BeautifulSoup

r = requests.get("http://www.english-bangla.com/browse")
print(r.status_code)
soup = BeautifulSoup(r.content, "lxml")

alphabt_link = soup.find("div", id="cat_page").find("div", class_="a-z").find_all('a')
for letter in alphabt_link:
    letter_link =letter.get('href')
    print(letter_link)
    letter_link_req = requests.get(letter_link)
    letter_link_soup = BeautifulSoup(letter_link_req.content, "lxml")
    letter = letter_link_soup.find("div", id="cat_page").find("ul").find_all('a')
    for i in letter:
        print(i.text)
        letter_meaning_link = i.get('href')
        letter_meaning_link_req = requests.get(letter_meaning_link)
        letter_meaning_soup = BeautifulSoup(letter_meaning_link_req.content, "lxml")
        try:
            letter_meaning = letter_meaning_soup.find("div", id="w_info").find("span", class_="format1").text
            print(letter_meaning)
        except:
            print("Not a valid word")
    try:
        next_page_link = letter_link_soup.find("div", class_="pagination").find('a')
    except:
        next_page_link = None

    while 1:
        if next_page_link == None:
            break
        else:
            next_page_req = requests.get(next_page_link.get('href'))
            next_page_soup = BeautifulSoup(next_page_req.content, "lxml")
            letter = next_page_soup.find("div", id="cat_page").find("ul").find_all('a')
            for i in letter:
                print(i.text)
                letter_meaning_link = i.get('href')
                letter_meaning_link_req = requests.get(letter_meaning_link)
                letter_meaning_soup = BeautifulSoup(letter_meaning_link_req.content, "lxml")
                try:
                    letter_meaning = letter_meaning_soup.find("div", id="w_info").find("span", class_="format1").text
                    print(letter_meaning)
                except:
                    print("Not a valid word")

            try:
                pagination_links = next_page_soup.find("div", class_="pagination").find_all('a')
                for i in pagination_links:
                    if i.text == "Next >":
                        next_page_link = i
                        break
            except:
                next_page_link = None
