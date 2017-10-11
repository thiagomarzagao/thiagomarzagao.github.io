import time
from selenium import webdriver

path = '/Users/thiagomarzagao/Dropbox/dataScience/UnB-ADM/aula_raspagem/chromedriver'
browser = webdriver.Chrome(executable_path = path)
url = "http://www.scielo.br/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=title&fmt=iso.pft&lang=i"
url = "http://scielo.br/"
browser.get(url)
time.sleep(3)
browser.find_element_by_link_text("search form").click()
time.sleep(3)
browser.find_element_by_name("exprSearch").send_keys("macarena")
time.sleep(3)
browser.find_element_by_name("config").click()