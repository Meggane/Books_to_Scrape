import requests
from bs4 import BeautifulSoup

url_array = []
all_categories_links_array = []
category_url_array = []
category_names_array = []
universal_product_code_array = []
title_array = []
price_including_tax_array = []
price_excluding_tax_array = []
product_descriptions_array = []
categories_array = []
image_url_array = []
product_page_url_array = []
number_available_array = []
review_rating_array = []


# URL definition so as not to create shadows name
def url_link(url):
    return url


# fetch data for each new URL
def soup_link(url):
    page = requests.get(url_link(url))
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


# definition of the new URL if there are several pages
def page_change(url):
    url_array.append(url)
    while next_button(url):
        url = url_link(url) + "/../" + next_page(url)
        url_array.append(url)
        if next_button(url) is None:
            break
    return url_array


# recovery of links for each category
def links_tag_of_each_category(url):
    all_categories_tag = soup_link(url).find("ul", class_="nav-list").find_next("a").find_next_siblings("ul")
    for all_categories in all_categories_tag:
        # noinspection PyUnresolvedReferences
        test = all_categories.find_all("a")
        for category_link in test:
            all_categories_links_array.append(category_link["href"])
    return all_categories_links_array


# creation of links for each category
def links_of_each_category(url):
    for link_category in links_tag_of_each_category(url):
        category_url = url + link_category
        category_url_array.append(category_url)
    return category_url_array


# recovery of the title of each category
def category_names(url):
    for category_name in links_of_each_category(url):
        category_titles = soup_link(category_name).find_all("h1")
        for one_category_title in category_titles:
            category_names_array.append(one_category_title.string)
    return category_names_array


# recovery of "td" tags for universal_product_code, price_including_tax, price_excluding_tax, availability_section which
# all depend on the same table
def table_tag_data(url, string_th_tag, data_to_extract):
    th_tag = soup_link(url).find_all("th", string=string_th_tag)
    for data_to_extract in th_tag:
        data_to_extract = data_to_extract.find_next("td").string
    return data_to_extract


# recovery of data from each book
def data_recovery(url):
    for url in page_change(url):
        product_page_url_tag = soup_link(url).find_all("div", class_="image_container")
        for page_url in product_page_url_tag:
            product_page_url = url_link(url + "/../" + page_url.a["href"])
            product_page_url_array.append(product_page_url)

            universal_product_code_array.append(table_tag_data(product_page_url, "UPC", "universal_product_code"))
            price_including_tax_array.append(table_tag_data(product_page_url, "Price (incl. tax)",
                                                            "price_including_tax"))
            price_excluding_tax_array.append(table_tag_data(product_page_url, "Price (excl. tax)",
                                                            "price_excluding_tax"))

            title_tag = soup_link(product_page_url).find_all("h1")
            for title in title_tag:
                title_array.append(title.string)

            product_description_tag = soup_link(product_page_url).find_all("div", id="product_description")
            for product_description in product_description_tag:
                product_descriptions_array.append(product_description.find_next("p").string)

            category_tag = soup_link(product_page_url).find_all("li", class_="active")
            for category in category_tag:
                categories_array.append(category.find_previous("a").string)

            image_url_tag = soup_link(product_page_url).find_all("img")
            for image_url in image_url_tag:
                image_url_array.append(image_url["src"])

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
            number_available_array.append(number_available)

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

            review_rating_array.append(review_rating)

    return product_page_url_array, universal_product_code_array, title_array, price_including_tax_array, \
        price_excluding_tax_array, number_available_array, product_descriptions_array, categories_array, \
        review_rating_array, image_url_array
