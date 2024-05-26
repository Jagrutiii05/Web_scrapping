import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['scraping_db']
collection = db['Advanced_topics']

url = 'https://www.scrapethissite.com/pages/advanced/'
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser') # Parse the HTML content using BeautifulSoup

# finding sections to scrape
section = soup.find('div', {'class': 'col-md-6 col-md-offset-3'})

if section:
    heading = section.find('h3').text.strip()
    paragraph_under_heading = section.find('p', {'class': 'lead'}).text.strip()
    
    # Extracting all subsections
    subsections = []
    for h4 in section.find_all('h4'):
        title = h4.text.strip()
        link = h4.find('a')['href']
        description = h4.find_next_sibling('p').text.strip()
        subsections.append({'title': title, 'link': link, 'description': description})
    
    # Preparing the data
    data = {
        'heading': heading,
        'paragraph_under_heading': paragraph_under_heading,
        'subsections': subsections
    }
    
    collection.insert_one(data)
    print("Data successfully inserted into MongoDB!")
else:
    print("Could not find the specified section.")
