import requests
from bs4 import BeautifulSoup

r = requests.get("http://www.english-bangla.com/browse/index/a")
print(r.status_code)
print(r.headers.get("content-type", "unknown"))
soup = BeautifulSoup(r.content, "lxml")
print(soup)
print(soup.title)

# print(soup.find_all('a')['href'])
# tags = soup.find_all("li")
# print(tags)
