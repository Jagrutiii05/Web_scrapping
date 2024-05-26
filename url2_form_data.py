import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['scraping_db']
collection = db['forms_data']

base_url = 'https://www.scrapethissite.com/pages/forms/?page_num={}' # URL of the first page

page_number = 1
all_data = []

while True and page_number < 25:
    url = base_url.format(page_number) 
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser') # Parse the HTML content using BeautifulSoup

    # Extracting the table which has the data that could be useful from the given site
    table = soup.find('table', {'class': 'table'})
    # covering edge cases
    if not table:
        break 

    rows = table.find_all('tr')
    
    headers = []
    for th in rows[0].find_all('th'):
        headers.append(th.text.strip())
    
    for row in rows[1:]: 
        cells = row.find_all('td')
        cell_data = {headers[i]: cells[i].text.strip() for i in range(len(cells))}
        all_data.append(cell_data)
    # to ensure that each page is scraped we print this statement
    print(f"Scraped page {page_number}")

    page_number += 1

    time.sleep(2) # Sleep to avoid making too many requests in a short time

# Insert all the data into MongoDB
if all_data:
    collection.insert_many(all_data)
    print("Data successfully inserted into MongoDB!")
else:
    print("No data to insert into MongoDB.")