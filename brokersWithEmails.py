import requests
import pandas as pd
import json




cookies = {
    #input your cookies here
}
headers = {
    #input your headers here
}




def getCourtiers():
    startpage = 1
    data = []
    while True:
        json_data = {
            'params': {
                'sort': '',
                'page': startpage,
                'per_page': 1000,
                'searchFor': None,
                'context': {
                    'agencyCode': None,
                    'randomSortSeed': 22477,
                    'userType': None,
                    'areaServed': None,
                    'language': None,
                    'searchFor': None,
                },
            },
        }

        # Request url
        url = "https://zone.centris.ca/Directory/Search"

       
    
        try:
            response = requests.post(url=url, cookies=cookies, headers=headers, json=json_data)
            
            content = json.loads(response.content)
            response.raise_for_status()
            content = response.json()
            
            if not content.get("data"):
                break  # Exit loop if no more data
            for courtier in content["data"]:
                # print(courtier)
                
                name = courtier["fullName"]
                jobTitle = courtier["certificateType"]
                
                
                # Primary number
                primary_desc = courtier["primaryTelephoneDesc"]
                primary_extension = str(courtier["primaryTelephoneExtension"]) if courtier.get("primaryTelephoneExtension") else ""
                primary_number = f"{primary_desc} #{primary_extension}" if primary_extension else courtier["primaryTelephoneDesc"]

                # Secondary number
                secondary_desc = courtier["secondaryTelephoneDesc"]
                secondary_extension = str(courtier["secondaryTelephoneExtension"]) if courtier.get("secondaryTelephoneExtension") else ""
                secondary_number = f"{secondary_desc} #{secondary_extension}" if secondary_extension else ""
                        
                company_name = courtier["agencyName"]
                courtier_id = courtier["userCode"]
                        
            

                responseUser = requests.get(f'https://zone.centris.ca/Directory/Users/{courtier_id}', cookies=cookies, headers=headers)   
                responseUser.raise_for_status()
                    
                try:
                    contentUser = responseUser.json()
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    print(f"Response content: {responseUser.content}")
                    continue  # Skip to the next iteration
            
            
                # print(contentUser)
                
                website = contentUser.get("website", "")
                company_website = contentUser["office"].get("website", "") if contentUser.get("office") else courtier["primaryTelephone"]
                company_type = contentUser["office"].get("agencyCertificateType", "") if contentUser.get("office") else ""
                email = contentUser.get("email", "")
                languages = ", ".join(contentUser.get("spokenLanguages", []))
                data.append({
                            'Nom': name, 
                            'Titre': jobTitle, 
                            'Langues':languages,
                            'Téléphone principal': primary_number,
                            'Téléphone secondaire': secondary_number,
                            "Email" : email, 
                            "Site Web" : website, 
                            "Compagnie": company_name, 
                            "Compagnie Type": company_type, 
                            "Compagnie Site Web" : company_website 
                            })
                
               
                
                responseUser.close()
            print(startpage)
            startpage+=1
            
        
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break  # Exit loop on any request error
        
    return data

# Create a DataFrame
   
data = getCourtiers()
df = pd.DataFrame(data)
df.to_excel('scraped_data.xlsx', index=False)
