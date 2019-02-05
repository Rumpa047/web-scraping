import requests
from bs4 import BeautifulSoup
import re


# Make a simple GET request (just fetching a page)
# here i connect with the url using request.
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

# Using Regular Expressions
# Run a regular expression on the response text to look for specific string patterns:
re.findall(r'\$[0-9,.]+', r.text)

# Using BeautifulSoup
soup = BeautifulSoup(r.text, "html.parser")
print(soup)

# Look for all anchor tags on the page (useful if you’re building a crawler and need to find the next pages to visit)
links = soup.find_all("a")
print(links)

# Look for all tags with a specific class attribute (eg <li class="search-result">...</li>)
tags = soup.find_all("li", "search-result")
print(tags)

# Look for the tag with a specific ID attribute (eg: <div id="bar">...</div>)
tag = soup.find("div", id="bar")
print(tag)

# Look for nested patterns of tags (useful for finding generic elements, but only within a specific section of the page)
# tags = soup.find("div", id="search-results").find_all("a", "external-links")
# print(tags)

# Look for all tags matching CSS selectors (similar query to the last one, but might be easier to write for someone who knows CSS)
# tags = soup.select("#search-results .external-links")
# print(tags)

# Get a list of strings representing the inner contents of a tag (this includes both the text nodes as well as the text representation of any other nested HTML tags within)
# inner_contents = soup.find("div", id="price").contents
# print(inner_contents)

# Return only the text contents within this tag, but ignore the text representation of other HTML tags (useful for stripping our pesky <span>, <strong>, <i>, or other inline tags that might show up sometimes)
# inner_text = soup.find("div", id="price").text.strip()
# print(inner_text)

# Convert the text that are extracting from unicode to ascii if you’re having issues printing it to the console or writing it to files
# inner_text = soup.find("div", id="price").text.strip().encode("utf-8")
# print(inner_text)

# Get the attribute of a tag (useful for grabbing the src attribute of an <img> tag or the href attribute of an <a> tag)
anchor_href = soup.find("a")["href"]  # here i get the link
print(anchor_href)


# Putting several of these concepts together, here’s a common idiom: iterating over a bunch of container tags and pull out content from each of them
# for product in soup.find_all("div", "products"):
#     product_title = product.find("h1").text
#     product_price = product.find("span", "price").text
#     product_url = product.find("a")["href"]
#     print("{} is selling for {} at {}".format(
#         product_title, product_price, product_url))

# modifing
for product in soup.find_all("div"):
    title = product.find("h1").text
    detail = product.find("p").text
    url = product.find("a")["href"]
    print("Title: {}. detail: {}. link: {}".format(
        title, detail, url))
