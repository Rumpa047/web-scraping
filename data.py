import requests
from bs4 import BeautifulSoup

r = requests.get("http://www.english-bangla.com/browse/index/a")
print(r.status_code)
print(r.headers.get("content-type", "unknown"))
soup = BeautifulSoup(r.content, "lxml")
print(type(soup))
print(soup.title)

# tags = soup.find("div", id="cat_page").find("ul").find_all('a')
# for i in tags:
#     print(i)

for i in soup.select('ul'):
    print(i.text)
# print(soup.find_all('a')['href'])
# tags = soup.find_all("li")
# print(tags)
