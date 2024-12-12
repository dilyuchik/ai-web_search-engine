import requests
from bs4 import BeautifulSoup

prefix = 'https://www.ikw.uni-osnabrueck.de/en/'

start_url = prefix+'home.html'

agenda = [start_url]

while agenda:
    url = agenda.pop()
    print("Get ",url)
    r = requests.get(url) # get content of a URL
    print(r, r.encoding)
    if r.status_code == 200:
        print(r.headers)
        soup = BeautifulSoup(r.content, 'html.parser') # parse html content, giving all headers or anchors e.g.
        print(soup.find_all('a'))
        