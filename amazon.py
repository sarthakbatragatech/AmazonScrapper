from bs4 import BeautifulSoup
import re
import requests
a = []
url = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=children+supplements"
# add header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content, "html.parser")

#Csv writing setup
filename = "products.csv"
f = open(filename, "w", encoding='utf-8')
headers ="Asin, Name, Price, Number of Reviews\n"
f.write(headers)

#Regex if needed
# a = re.compile((?<=data-asin))
containers = soup.findAll("li", {"class":"s-result-item s-result-card-for-container a-declarative celwidget "})
for container in containers:
	asin = (container["data-asin"])

	# Product Name
	title_container = container.findAll("a", {"class":"a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"})
	name = title_container[0]["title"]

	# Product Price
	# span class="a-offscreen">$14.67
	price_container = container.findAll("span", {"class":"a-offscreen"})
	if (len(price_container) == 1):
		price = price_container[0].text
	else:
		price = "N/A"

	#Number of reviews
	num_review_container = container.findAll("a", {"class":"a-size-small a-link-normal a-text-normal"})
	if (len(num_review_container) > 1):
		num_reviews = num_review_container[1].text.strip()
	else: 
		num_reviews = num_review_container[0].text.strip()

	#
	#try:
	#	num_review2 = num_review_container[1].text.strip()
	#	print(num_review2)
	# except list index out of range:
	#	num_review2 = 0;
	#

	f.write(asin + ',' + name.replace(",", "|") + ',' + price.replace("$", "") + "," + num_reviews.replace(",", "") + "\n") # + ',' + name.replace(",", "|") + ',' + price + "," + num_reviews + "\n")

f.close()
