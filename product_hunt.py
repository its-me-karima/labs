from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome()

data = []

# -------- scraping ----------
url = "https://www.producthunt.com/search?q=mental+health+ai"

driver.get(url)
time.sleep(3)

soup = BeautifulSoup(driver.page_source, "html.parser")
time.sleep(5)
products = soup.find_all("button", {"data-test": lambda x: x and "spotlight-result-product" in x})

for p in products:
    #title
    title_tag = p.find("span", class_="text-base font-semibold text-dark-gray")
    title = title_tag.text.strip() if title_tag else None
    #descr
    descr_tag = p.find("span", class_="text-sm font-normal text-light-gray")
    description = descr_tag.text.strip() if descr_tag else None
    #rating
        # rating (count stars svg)
    stars = p.find_all("svg")
    rating = len(stars) if stars else None

    # reviews
    review = None
    review_tag = p.find(string=lambda x: x and "review" in x.lower())
    if review_tag:
        review = review_tag.strip()
        
    data.append([title, description, review, rating])


driver.quit()

# dataframe
df = pd.DataFrame(
    data,
    columns=["title", "description", "review", "rating"]
)

# save
df.to_csv("product_hunt.csv", index=False, encoding="utf-8")

print("CSV file created successfully")