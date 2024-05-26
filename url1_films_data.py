import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['scraping_db']
collection = db['films_data']

url = 'https://www.scrapethissite.com/pages/ajax-javascript/#2015'
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser') # Parse the HTML content using BeautifulSoup

# Extract the year links and Iterate over each year link
years = soup.find_all('a', {'class': 'year-link'})
for year in years:
    year_id = year['id']
    print(f"Scraping data for year: {year_id}")

    year_url = f"https://www.scrapethissite.com/pages/forms/?year={year_id}" # Modify the URL to fetch data for the specific year
    year_response = requests.get(year_url)
    year_html_content = year_response.text
    
    year_soup = BeautifulSoup(year_html_content, 'html.parser') # Parse the HTML content for the specific year
    
    # Extracting the table which has useful information from the given site
    table = year_soup.find('table', {'class': 'table'})
    # covering edge cases
    if not table:
        continue 
    
    rows = table.find_all('tr')
    
    headers = []
    for th in rows[0].find_all('th'):
        headers.append(th.text.strip())
    
    data = []
    for row in rows[1:]:  # Skip the header row
        cells = row.find_all('td')
        cell_data = {headers[i]: cells[i].text.strip() for i in range(len(cells))}
        cell_data['Year'] = year_id  # Add year information to each record
        data.append(cell_data)
    
    # Insert data into MongoDB for each year
    if data:
        collection.insert_many(data)
        print(f"Data for year {year_id} successfully inserted into MongoDB!")
    else:
        print(f"No data found for year {year_id}.")

print("All data successfully scraped and inserted into MongoDB!")