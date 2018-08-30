from bs4 import BeautifulSoup
import re # import Regular expression operations module
import requests
a = []
url_str = input("Enter the product category you want to search for: ")
try:
	str1, str2 = url_str.split()
except ValueError:
	str2 = "empty"

if (str2 == "empty"):
	url = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=" + url_str
else:
	url = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=" + str1 + "+" + str2

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

# Used this to beautify and inspect the html/xml data ----> http://jsbeautifier.org/


containers = soup.findAll("li", {"class":"s-result-item s-result-card-for-container a-declarative celwidget "})
# if empty, page is styled different, invoke second style query s-result-item s-result-card-for-container s-carded-grid celwidget  
if (len(containers) == 0):
	containers = soup.findAll("li", {"class":"s-result-item s-result-card-for-container s-carded-grid celwidget "})
	print("Style 2")

if (len(containers) == 0):
	sponsored_containers = soup.findAll("li", {"class":"s-result-item  celwidget  AdHolder"}) 
	print("Style 3")
	containers2 = soup.findAll("li", {"class":"s-result-item  celwidget  "})  
	container3 = soup.findAll("li", {"class":"s-result-item s-col-span-12  celwidget  "})

#Sponsored
for container in sponsored_containers:
	asin = (container["data-asin"])
	print(asin)

	# Product Name
	try:
		title_container = container.findAll("h2")
		name = title_container[0]["data-attribute"]
	except:
		name = "N/A"

	# Product Price
	# span class="a-offscreen">$14.67
	price_container = container.findAll("span", {"class":"a-offscreen"})
	if (len(price_container) == 1):
		price = price_container[0].text
	else:
		price = "N/A"

	#Number of reviews
	num_review_container = container.findAll("a", {"class":"a-size-small a-link-normal a-text-normal"})
	try:
		if (len(num_review_container) > 1):
			num_reviews = num_review_container[1].text
		else: 
			num_reviews = num_review_container[0].text
	except:
		num_reviews = "0"
	#
	#try:
	#	num_review2 = num_review_container[1].text.strip()
	#	print(num_review2)
	# except list index out of range:
	#	num_review2 = 0;
	#

	f.write(asin + ',' + name.replace(",", "|") + ',' + price.replace("$", "") + "," + num_reviews.replace(",", "") + "\n") # + ',' + name.replace(",", "|") + ',' + price + "," + num_reviews + "\n")	

for container in containers2:
	asin = (container["data-asin"])

	# Product Name
	try:
		title_container = container.findAll("a", {"class":"a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"})
		name = title_container[0]["title"]
	except:
		name = "N/A"

	# Product Price
	# span class="a-offscreen">$14.67
	price_container = container.findAll("span", {"class":"a-offscreen"})
	if (len(price_container) == 1):
		price = price_container[0].text
	else:
		price = "N/A"

	#Number of reviews
	num_review_container = container.findAll("a", {"class":"a-size-small a-link-normal a-text-normal"})
	try:
		if (len(num_review_container) > 1):
			num_reviews = num_review_container[1].text
		else: 
			num_reviews = num_review_container[0].text
	except:
		num_reviews = "0"
	#
	#try:
	#	num_review2 = num_review_container[1].text.strip()
	#	print(num_review2)
	# except list index out of range:
	#	num_review2 = 0;
	#

	f.write(asin + ',' + name.replace(",", "|") + ',' + price.replace("$", "") + "," + num_reviews.replace(",", "") + "\n") # + ',' + name.replace(",", "|") + ',' + price + "," + num_reviews + "\n")

f.close()