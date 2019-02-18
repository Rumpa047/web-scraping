import requests
from bs4 import BeautifulSoup

r = requests.get("http://www.english-bangla.com/browse")
print(r.status_code)
soup = BeautifulSoup(r.content, "lxml")
# print(type(soup))
# print(soup.title)
alphabt_link = soup.find("div", id="cat_page").find("div", class_="a-z").find_all('a')
# print(alphabt_link)
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

# for i in soup.select('ul'):
#     print(i.text)
# print(soup.find_all('a')['href'])
# tags = soup.find_all("li")
# print(tags)
