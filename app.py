import requests
from bs4 import BeautifulSoup


# Make a simple GET request (just fetching a page)

r = requests.get("http://example.com/page")


# Make a POST requests (usually used when sending information to the server like submitting a form)

r = requests.post("http://example.com/page", data=dict(
    email="me@domain.com",
    password="secret_value"
))

# Pass query arguments aka URL parameters (usually used when making a search query or paging through results)

r = requests.get("http://example.com/page", params=dict(
    query="web scraping",
    page=2
))

# See what response code the server sent back (useful for detecting 4XX or 5XX errors)
print(r.status_code)

# Access the full response as text (get the HTML of the page in a big string)
# print(r.text)

# Look for a specific substring of text within the response
if "blocked" in r.text:
    print("we've been blocked")

# Check the response’s Content Type (see if you got back HTML, JSON, XML, etc)
print(r.headers.get("content-type", "unknown"))
