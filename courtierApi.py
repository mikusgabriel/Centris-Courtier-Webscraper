import requests
from bs4 import BeautifulSoup
import pandas as pd
import json




# Transforme un liste de phonme number html, en string avec les numeros
def list_of_numbers(numbers: list):
    numbers_text=""
    numbers_text+=(numbers[0].text)
    
    
    for i in range (1,len(numbers)):
        
        numbers_text+=","
        numbers_text+=numbers[i].text
        
    
    return numbers_text




headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
base_url = "https://www.centris.ca"

startposition = 0
data = []
while True:
    # Needed param
    payload={"startPosition" : startposition}
   
    # Cookies
    session = requests.Session()

    # Request url
    url = 'https://www.centris.ca/Broker/GetBrokers'
    response = session.post(url, headers=headers,json=payload)

    
    if response.status_code == 200:
        
        # Load json content and get HTML content
        content = json.loads(response.content)
        content = content["d"]["Result"]["Html"]
        
        if not content:
            break
        
        
        # Parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
    
        for courtier in soup.find_all('div', class_='broker-thumbnail-item col-12 col-lg-6 legacy-reset'):
            
            
            name = courtier.find(itemprop='name').text
            jobTitle = courtier.find(itemprop='jobTitle').text
            
            
            numbers = courtier.find_all(itemprop='telephone')
            if isinstance(numbers,list):
                if len(numbers)!= 0 :
                    numbers = list_of_numbers(numbers)
                else:
                    numbers = ""
                    
        
            contact_link = courtier.find('a', class_="btn btn-outline-icon-only GTM-contact-broker")["href"]
            
            
            company_name = courtier.find(itemprop = 'legalName').text
            company_type = courtier.find(itemprop = 'legalName')["content"].split()[-2]+courtier.find(itemprop = 'legalName')["content"].split()[-1]
            
            website_tag = courtier.find('a', class_="btn btn-outline-icon-only")
            if website_tag and 'href' in website_tag.attrs:
                website = website_tag['href']
            else:
                website=""
                        
                        
            
            data.append({
                         'Nom': name, 
                         'Titre': jobTitle, 
                         'Téléphone': numbers,
                         "Contact" : base_url+contact_link, 
                         "Compagnie": company_name, 
                         "Compagnie_Type": company_type , 
                         "Site_Web" : website 
                         })
            
            
            startposition+=1

        
    
    else:
        print("Failed to retrieve content, status code:", response.status_code)
 # Create a DataFrame
 

df = pd.DataFrame(data)
df.to_excel('scraped_data.xlsx', index=False)
