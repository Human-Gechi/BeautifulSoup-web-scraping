import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
file_path = r"C:\Users\HP\web scrapping.csv"#file path
column_names = ["TITLE", "COST", "AVAILABILITY"]
data = []
url = "https://books.toscrape.com/catalogue/page-"
entries = 1
while True:
    url1 = f"{url}{entries}.html" 
    try:
        response = requests.get(url1, timeout=10)  # Setting  timeout to 10 seconds
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        break
    soup = BeautifulSoup(response.content, "html.parser")    
    books = soup.find_all("article", class_="product_pod")  # Finding all article elements with class "product_pod"   
    if not books:
        print(f"No more books found at page {entries}. Stopping...")
        break
    for book in books:
        title = book.h3.a["title"]
        cost = book.find("p", class_="price_color").text.strip()  # Extract text
        availability = book.find("p", class_="instock availability").text.strip()  # Extract text0
        data.append({"TITLE": title, "COST": cost, "AVAILABILITY": availability})        
    entries += 1
    time.sleep(1)
df = pd.DataFrame(data, columns=column_names)
sorted_values = df.sort_values(by=["TITLE"])
sorted_values.to_csv(file_path, index=False)
print(f"Scraped data has been saved to {file_path}")
