import json
import pandas as pd

with open("product_hunt1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

df.to_csv("product_hunt1.csv", index=False, encoding="utf-8")

print("CSV file created successfully")