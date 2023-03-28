import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv


# fetch data for each new URL
def soup_link(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


# fetch the next button to determine if there are multiple pages
def next_button(url):
    next_button_link = soup_link(url).find("li", class_="next")
    return next_button_link


# retrieval of link from next page
def next_page(url):
    next_page_link = next_button(url).a["href"]
    return next_page_link


# url analysis to extract scheme, netloc and path then cut the path to have a clean url
def parsed_url_path(url, splitter, string_to_put, iterable_1, iterable_2):
    parsed_url = urlparse(url)
    path = parsed_url.path
    path_turned_into_a_list = path.split(splitter)
    path_list_turned_into_string = string_to_put.join(path_turned_into_a_list[int(iterable_1):int(iterable_2)])
    return parsed_url, path_list_turned_into_string


url_list = []


# definition of the new URL if there are several pages
def page_change(url):
    url_list.append(url)
    while next_button(url):
        parsed_page_url, path_string_page_url = parsed_url_path(url, "/", "/", "1", "-1")
        url = parsed_page_url.scheme + "://" + parsed_page_url.netloc + "/" + path_string_page_url + "/" \
                                                                            + next_page(url)
        url_list.append(url)
        if next_button(url) is None:
            break
    return url_list


# recovery of "td" tags for universal_product_code, price_including_tax, price_excluding_tax, availability_section which
# all depend on the same table
def table_tag_data(url, string_th_tag, data_to_extract):
    th_tag = soup_link(url).find_all("th", string=string_th_tag)
    for data_to_extract in th_tag:
        data_to_extract = data_to_extract.find_next("td").string
    return data_to_extract


product_page_url_list = []
universal_product_code_list = []
title_list = []
price_including_tax_list = []
price_excluding_tax_list = []
product_descriptions_list = []
categories_list = []
image_url_list = []
number_available_list = []
review_rating_list = []


# recovery of data from each book
def data_recovery(url):
    for url in page_change(url):
        product_page_url_tag = soup_link(url).find_all("div", class_="image_container")
        for page_url in product_page_url_tag:
            product_page_url_link = page_url.a["href"]
            parsed_url, path_url = parsed_url_path(url, "/", "", "1", "2")
            new_url = parsed_url.scheme + "://" + parsed_url.netloc + "/" + path_url + "/"
            parsed_product_page_url, path_product_page_url = parsed_url_path(product_page_url_link, "../", "", "3", "4")
            product_page_url = new_url + path_product_page_url
            product_page_url_list.append(product_page_url)
            universal_product_code_list.append(table_tag_data(product_page_url, "UPC", "universal_product_code"))
            price_including_tax_list.append(table_tag_data(product_page_url, "Price (incl. tax)",
                                                           "price_including_tax"))
            price_excluding_tax_list.append(table_tag_data(product_page_url, "Price (excl. tax)",
                                                           "price_excluding_tax"))
            title_tag = soup_link(product_page_url).find_all("h1")
            for title in title_tag:
                title_list.append(title.string)
            product_description_tag = soup_link(product_page_url).find_all("div", id="product_description")
            for product_description in product_description_tag:
                product_descriptions_list.append(product_description.find_next("p").string)
            category_tag = soup_link(product_page_url).find_all("li", class_="active")
            for category in category_tag:
                categories_list.append(category.find_previous("a").string)
            image_url_previous_tag = soup_link(product_page_url).find_all("div", class_="item active")
            for image_url_tag in image_url_previous_tag:
                image_url_link = image_url_tag.img["src"]
                parsed_img_url, path_img_url = parsed_url_path(image_url_link, "../", "", "2", "6")
                image_url = parsed_url.scheme + "://" + parsed_url.netloc + "/" + path_img_url
                image_url_list.append(image_url)

            # extraction of the number of available books
            # transform the digits of the string into int to extract them then reconvert them to transform the list into
            # string
            def extract_number():
                availability_section_tag = table_tag_data(product_page_url, "Availability", "availability_section")
                list_of_numbers_to_extract = []
                for number_in_availability_section in availability_section_tag:
                    if number_in_availability_section.isnumeric():
                        number_in_availability_section = str(number_in_availability_section)
                        list_of_numbers_to_extract.append(number_in_availability_section)
                return list_of_numbers_to_extract
            # convert list to string
            number_available = "".join(extract_number())
            number_available_list.append(number_available)

            # retrieving the name of the class that determines the review rating of the books
            def review_rating_class(class_name):
                review_rating_class_name_tag = soup_link(product_page_url).find("div", class_="product_main")\
                    .find("p", class_=class_name)
                return review_rating_class_name_tag
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
            review_rating_list.append(review_rating)
    return product_page_url_list, universal_product_code_list, title_list, price_including_tax_list, \
        price_excluding_tax_list, number_available_list, product_descriptions_list, categories_list, \
        review_rating_list, image_url_list


data_recovery("https://books.toscrape.com/catalogue/category/books/fiction_10/index.html")

# creation of csv file
header = ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
          "number_available", "product_description", "category", "review_rating", "image_url"]
with open("one_category_data_extraction.csv", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(header)
    for product_page_url_for_each_book, universal_product_code_for_each_book, title_for_each_book, \
            price_including_tax_for_each_book, price_excluding_tax_for_each_book, number_available_for_each_book, \
            product_description_for_each_book, category_for_each_book, review_rating_for_each_book, \
            image_url_for_each_book in \
            zip(product_page_url_list, universal_product_code_list, title_list, price_including_tax_list,
                price_excluding_tax_list, number_available_list, product_descriptions_list, categories_list,
                review_rating_list, image_url_list):
        lines = [product_page_url_for_each_book, universal_product_code_for_each_book, title_for_each_book,
                 price_including_tax_for_each_book, price_excluding_tax_for_each_book, number_available_for_each_book,
                 product_description_for_each_book, category_for_each_book, review_rating_for_each_book,
                 image_url_for_each_book]
        writer.writerow(lines)
