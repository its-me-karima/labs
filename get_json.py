from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time

driver = webdriver.Chrome()

url = "https://www.producthunt.com/search?q=mental+health+ai"
driver.get(url)

time.sleep(5)

data = []
seen = set()

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")

    products = soup.find_all(
        "button",
        {"data-test": lambda x: x and "spotlight-result-product" in x}
    )

    new_items = 0

    for p in products:
        app_id = p.get("data-test")

        if app_id in seen:
            continue

        seen.add(app_id)
        new_items += 1

        # title
        title_tag = p.find("span", class_="text-base font-semibold text-dark-gray")
        title = title_tag.text.strip() if title_tag else None

        # description
        descr_tag = p.find("span", class_="text-sm font-normal text-light-gray")
        description = descr_tag.text.strip() if descr_tag else None

        # rating
        stars = p.find_all("svg")
        rating = len(stars)

        # reviews
        review = None
        review_tag = p.find(string=lambda x: x and "review" in x.lower())
        if review_tag:
            review = review_tag.strip()

        data.append({
            "id": app_id,
            "name": title,
            "tagline": description,
            "rating": rating,
            "reviews": review
        })

    # stop if no new products
    if new_items == 0:
        break

    # scroll
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

driver.quit()

with open("product_hunt1.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("JSON file created successfully")