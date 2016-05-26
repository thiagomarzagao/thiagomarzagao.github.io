import requests

html = requests.get("http://scielo.br/")
print html
print html.text