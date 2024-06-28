
import requests
import gzip
from io import BytesIO
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.centris.ca/fr/courtiers-immobiliers?view=Thumbnail&pback=true&uc=1'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Start a session to handle cookies
session = requests.Session()

# Make the request with session handling
response = session.get(url, headers=headers)

# Check the status code and decode content
if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    brokers_container = soup.find('section', id='broker-result')
    
    brokers = brokers_container.find('div', class_='wrapper even wrapper-results')
    
    print(brokers)
    
    data = []
    for courtier in soup.find_all('div', class_='broker-thumbnail-item col-12 col-lg-6 legacy-reset'):
        name = courtier.find(itemprop='name').text
        jobTitle = courtier.find(itemprop='jobTitle').text
        data.append({'Name': name, 'Titre': jobTitle})

    # Create a DataFrame
    df = pd.DataFrame(data)


    df.to_excel('scraped_data.xlsx', index=False)
else:
    print("Failed to retrieve content, status code:", response.status_code)





def find_nested_div(soup, class_list):
    if not class_list:
        return soup
    
    current_class = class_list.pop(0)
    next_div = soup.find('div', class_=current_class)
    
    if next_div:
        return find_nested_div(next_div, class_list)
    else:
        return None

# class_list = [
#     'wrapper even wrapper-results', 'level-1', 'level-2', 'level-3', 'level-4',
#     'level-5', 'level-6', 'level-7', 'level-8', 'level-9', 'target-div'
# ]

# result_div = find_nested_div(soup, class_list.copy())

# if result_div:
#     print(result_div.text)
# else:
#     print("Target div not found")
