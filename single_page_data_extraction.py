import requests
from bs4 import BeautifulSoup
import csv

home_page_url = "http://books.toscrape.com/"
page = requests.get(home_page_url)
soup = BeautifulSoup(page.content, "html.parser")

# get the link of the first book
product_page_url_link = soup.find("div", class_="image_container").a["href"]
# link of the first book
product_page_url = home_page_url + product_page_url_link
# assignment of the new URL to retrieve the data
page = requests.get(product_page_url)
soup = BeautifulSoup(page.content, "html.parser")


# recovery of "td" tags for universal_product_code, price_including_tax, price_excluding_tax, availability_section which
# all depend on the same table
def table_tag_data(string_th_tag):
    string_td_tag = soup.find("th", string=string_th_tag).find_next("td").string
    return string_td_tag


universal_product_code = table_tag_data("UPC")
price_including_tax = table_tag_data("Price (incl. tax)")
price_excluding_tax = table_tag_data("Price (excl. tax)")
title = soup.find("h1").string
product_description = soup.find("div", id="product_description").find_next("p").string
category = soup.find("li", class_="active").find_previous("a").string
image_url = home_page_url + soup.find("img")["src"]


# extraction of the number of available books
# transform the digits of the string into int to extract them then reconvert them to transform the list into string
def extract_number():
    availability_section = table_tag_data("Availability")
    list_of_numbers_to_extract = []
    for number_in_availability_section in availability_section:
        if number_in_availability_section.isnumeric():
            number_in_availability_section = str(number_in_availability_section)
            list_of_numbers_to_extract.append(number_in_availability_section)
    return list_of_numbers_to_extract


# convert list to string
number_available = "".join(extract_number())


# retrieving the name of the class that determines the review rating of the books
def review_rating_class(class_name):
    review_rating_class_name = soup.find("div", class_="product_main").find("p", class_=class_name)
    return review_rating_class_name


if review_rating_class("Five"):
    review_rating = "5"
elif review_rating_class("Four"):
    review_rating = "4"
elif review_rating_class("Three"):
    review_rating = "3"
elif review_rating_class("Two"):
    review_rating = "2"
elif review_rating_class("One"):
    review_rating = "1"
else:
    review_rating = "0"

# creation of csv file
header = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
          "number_available", "product_description", "category", "review_rating", "image_url"]
line = [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,
        product_description, category, review_rating, image_url]
with open("single_page_data_extraction.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(header)
    writer.writerow(line)
