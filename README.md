How to Run:
==============================
 1. Edit **set_env.sh** file with appropriate values and export those variables.
 
 2. Run each file to extract the data.
       1. **CompanyIndexBuilder.py** : It extracts the list of all company names and its url.
       2. **CompanyInfoExtractor.py** : It takes input as list of company name and url and fetches company details for each company.
       3. **EmployeeInfoExtractor.py** : It takes input as list of company details and extracts all employees of that company.
 
 3. Enjoy!

Output:
============================

* **CompanyIndex**:

        [{"n": "Apple", "u": "https://www.linkedin.com/company/apple?trk=companies_directory"}]

* **CompanyInfo**:

       [{
        "url": "https://www.linkedin.com/company/apple?trk=companies_directory",
        "name": "Apple",
        "companyId": "162479",
        "about": "We\u2019re a diverse collective of thinkers and doers, continually reimagining what\u2019s possible to help us all do what we love in new ways. And the same innovation that goes into our products also applies to our practices \u2014 strengthening our commitment to leave the world better than we found it. This is where your work can make a difference in people\u2019s lives. Including your own.\n\nApple is an equal opportunity employer that is committed to inclusion and diversity. Visit jobs.apple.com to learn more.",
        "website": "http://www.apple.com/jobs/",
        "industry": "Consumer Electronics",
        "companysize": 10001,
        "headquarters": "Cupertino, California",
        "type": "Public Company",
        "founded": "1976",
        "specialties": "Innovative Product Development, World-Class Operations, Retail, and Telephone Support"
      }]


* **EmployeeInfo**:

        [{
          "designation": "Senior Director, Commercial Sales EMEA",
          "name": "John Doe",
          "link": "",
          "company": {
            "url": "https://www.linkedin.com/company/apple?trk=companies_directory",
            "name": "Apple",
            "companyId": "162479",
            "website": "http://www.apple.com/jobs/",
            "industry": "Consumer Electronics",
            "companysize": 10001,
            "headquarters": "Cupertino, California",
            "type": "Public Company",
            "founded": "1976",
            "specialties": "Innovative Product Development, World-Class Operations, Retail, and Telephone Support"
          },
          "location": "Brussels Metropolitan Area",
          "lastname": "Doe",
          "firstname": "John"
        }]
 
Disclaimer:
============================
This project is a research project and an enquiry into how distributed scraping systems can work in practice. The project demonstrates cutting edge technology to try and scrape a website of your choice and takes into consideration the right architecture to be used in a distributed scraping system. While the example used in this particular project is that of Linkedin, this project is in no way associated, sponsored or represented by Linkedin, it is also to be noted that scraping any data from Linkedin is against the data policies of Linkedin and will be liable for legal action (according to Linkedin's policy). Furthermore, feel free to make changes to this project and use it for any other website that does not have strict data policies or if you already have a contract/agreement with such a website. All data scraped while testing this project was from our 1st degree connections and only publicly available information was scraped of not more than 10 records and the same records were scraped each time the test was run. This is a production ready system in the sense you can crawl and scrape specific website data but it is not production-ready in the sense that it's not supposed to be used on Linkedin to scrape any information but you can feel free to test this, learn from this and make changes as required to use it on other websites. If however, even after reading this disclaimer you plan to use this to scrape Linkedin then please keep in mind that Linkedin has advanced bot detection capabilities and will block you profile in the first few tries. 
**The use of this project for any application and purpose and the consequences of the same are the sole responsibility of the developer.**    
    
 
 
 
     