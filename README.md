![repo size](https://img.shields.io/github/repo-size/Meggane/Books_to_Scrape?style=plastic)
![last commit](https://img.shields.io/github/last-commit/Meggane/Books_to_Scrape?style=plastic)
![python](https://img.shields.io/pypi/pyversions/requests?color=yellow&style=plastic)

# Web scraping of the site Books to Scrape to create a price monitoring system

---

This project aims to recover data from the site [Books to Scrape](https://books.toscrape.com/), an online book dealer. It allows to recover the data of each 
book at the time of its execution. We can thus retrieve the link of the different books, the universal product code, the title, the price with and without tax, 
the number of books still available, the description of the book, the category, the grade obtained by the book as well as its image. The purpose of this ETL 
pipeline is to perform price monitoring of books automatically.
Through this project, we will extract, transform and load data into CSV files. We also retrieve the images from each book.

---

## Install and execute the code (on Linux) :
- clone the repository on your computer
`git clone https://github.com/Meggane/Books_to_Scrape.git`
- move to the cloned folder
`cd Books_to_Scrape/`
- create a virtual environment named "env" on your computer
`python -m venv env`
- activate it
`source env/bin/activate`
- install the virtual environment using the file **requirements.txt**
`pip install -r requirements.txt`
- execute the code in your terminal
`python all_categories_data_extraction.py`

---

Once the code is executed, you will find two new folders : *csv_files* and *images*. Inside there is a folder for each category of the site in which we find 
the csv file and the images of each book of this category.
