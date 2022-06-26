import requests

response = requests.get("https://gvwilson.github.io/sd4ds/table.html")
print(f"status code: {response.status_code}")
print(f"len(text): {len(response.text)}")
