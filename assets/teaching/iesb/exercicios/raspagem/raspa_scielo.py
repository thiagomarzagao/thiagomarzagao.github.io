import requests
from bs4 import BeautifulSoup

html = requests.get("http://scielo.br/")
html_text = html.text.encode("utf-8")
soup = BeautifulSoup(html_text)
print(soup)
soup.find_all("p")
soup.find_all("a")