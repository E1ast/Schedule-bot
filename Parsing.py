import requests
from bs4 import BeautifulSoup

url = 'http://simfpolyteh.ru/raspisanie/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

links = soup.find_all('img')


def Pars():
  i = 0
  for link in links:
      links_all = link.get('src')
      i += 1
      if i == 4:
          print(link.get('src'))

Pars()