import requests
from bs4 import BeautifulSoup

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


def table_tag_data(string_th_tag):
    string_td_tag = soup.find("th", string=string_th_tag).find_next("td").string
    return string_td_tag


universal_product_code = table_tag_data("UPC")
price_including_tax = table_tag_data("Price (incl. tax)")
price_excluding_tax = table_tag_data("Price (excl. tax)")
title = soup.find("h1").string
product_description = soup.find("div", id="product_description").find_next("p").string
category = soup.find("li", class_="active").find_previous("a").string
image_url = soup.find("img")["src"]


def extract_number():
    availability_section = soup.find("th", string="Availability").find_next("td").string
    list_of_numbers_to_extract = []
    for number_in_availability_section in availability_section:
        if number_in_availability_section.isnumeric():
            number_in_availability_section = str(number_in_availability_section)
            list_of_numbers_to_extract.append(number_in_availability_section)
    return list_of_numbers_to_extract


# convert list to string
number_available = "".join(extract_number())
