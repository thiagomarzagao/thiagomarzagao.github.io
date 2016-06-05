import requests

url1 = "http://api.vagalume.com.br/search.php?art=Lady%20Gaga&mus=Alejandro"
url2 = "http://api.vagalume.com.br/search.php?art=Lady%20Gaga&mus=Telephone"
url3 = "http://api.vagalume.com.br/search.php?art=Foo%20Fighters&mus=Learn%20to%20Fly"
urls = [url1, url2, url3]

for url in urls:
    response = requests.get(url)
    print(response)
    print(response.text)