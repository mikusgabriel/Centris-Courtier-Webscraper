
## This project involves scraping broker information from a website that requires login. There are two versions of the scraper:

1. **Anonymous Broker Version**: This version scrapes broker information without emails.
2. **Emails Broker Version**: This version scrapes broker information including emails, requiring user authentication.



## Anonymous Broker Version
  This version scrapes broker information excluding emails. It runs relatively fast, taking approximately 6 minutes to complete.
    
  ### Run the script using Python:
    python brokersAsAnon.py


## Emails Broker Version
  This version scrapes broker information including emails. It requires user authentication and takes about 2 hours to complete.

  ### Obtaining Cookies and Headers
  Follow the [guide](https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup) on StackOverflow to obtain your cookies and headers.
  Use the "Search" request that appears when you click the 'Répertoire' button, instead of the first network request mentioned in the guide.
  Copy your cookies and headers information into the predefined variables in the script.
    
  ### Preparing the Script
    python brokersWithEmails.py
