from bs4 import BeautifulSoup
import requests

NUM_YEARS = 5

response = requests.get("https://gvwilson.github.io/sd4ds/table.html")
doc = BeautifulSoup(response.text, "html.parser")

results = {}
for (i, row) in enumerate(doc.find_all("tr")):
    if i == 0:
        continue
    items = list(row.find_all("td"))
    if "%GDP" not in items[1].text:
        continue
    country = items[0].text.strip()
    average = sum([float(x.text) for x in items[2:(2+NUM_YEARS)]]) / NUM_YEARS
    results[country] = average

print(f"Country,Average Health Care Spending (%GDP)")
for (key, average) in sorted(results.items()):
    print(f"{key},{average}")
