from bs4 import BeautifulSoup
import re
import requests
url = "https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=children+supplements"
# add header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")
# a = re.compile((?<=data-asin))
print(soup.h1)
