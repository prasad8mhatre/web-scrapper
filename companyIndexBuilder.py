from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import util
import json

#fetches all the company name and url for page link
def execute(driver, pageUrl):
    companiesNameUrl = dict()

    driver.get(pageUrl)

    try:
        companies = driver.find_elements(By.CSS_SELECTOR, '#seo-dir > div > div:nth-child(3) > div > ul > li > a')
        for company in companies:
            try:
                companyName = company.text
                companyUrl = company.get_attribute('href')
                row = {
                    'n': companyName,
                    'u':companyUrl
                }

                util.writeFile("resources/companyIndex.json", json.dumps(row))
                print(companyName)
            except Exception:
                print("Failed to get company detail for " + company.text)
    except TimeoutException:
        print("Loading took too much time!")

    return companiesNameUrl


# Enable to test on local
if __name__ == "__main__":
    print("Started company index builder")
    driver = util.openChromeBrowser()
    for i in range(97+25,97+26,1):
        url = 'https://www.linkedin.com/directory/companies/' + str(chr(i))
        print("performing for page " + url)
        execute(driver, url)
