import requests
from bs4 import BeautifulSoup


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
    while next_button(url):
        url = url_link(url) + "/../" + next_page(url)
        if next_button(url) is None:
            break
