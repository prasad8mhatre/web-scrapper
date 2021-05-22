import json
import sys
import time
import urllib.parse as urlparse
from datetime import datetime
from urllib.parse import parse_qs

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import util


#fetches all the company name and url for page link
def execute(driver,companyUrl):
    print("Fetching company info for url:" +  companyUrl)


    company = dict()
    try:
        company['url'] = companyUrl
        #go to about page
        companyUrl = companyUrl.replace('?trk=companies_directory', '')
        if companyUrl[len(companyUrl)-1] != '/' :
            companyUrl  = companyUrl + '/'
        companyUrl = companyUrl + 'about'

        driver.get(companyUrl)


        name = driver.find_elements(By.XPATH, '//span[@dir="ltr"]')[0].text.strip()
        company['name'] = name

        salesNavigatorLink = ""
        try:
            salesNavigatorLink = driver.find_element_by_class_name('org-top-card-primary-actions__view-in-sales-navigator-action').get_attribute('href')
            print(salesNavigatorLink)
            parsed = urlparse.urlparse(salesNavigatorLink)
            print(parse_qs(parsed.query)['companyId'][0])
            company['companyId'] = parse_qs(parsed.query)['companyId'][0]
        except Exception as ex:
            try:
                dropDown = driver.find_element_by_class_name('org-overflow-menu')
                dropDown.click()
                dropDown.click()

                dropDownlist = driver.find_element_by_class_name(
                    'artdeco-dropdown__content-inner').find_elements_by_tag_name('li')
                salesNavigatorLink = dropDownlist[2].find_element_by_tag_name('a').get_attribute('href')
                print(salesNavigatorLink)
                parsed = urlparse.urlparse(salesNavigatorLink)
                print(parse_qs(parsed.query)['companyId'][0])
                company['companyId'] = parse_qs(parsed.query)['companyId'][0]
            except Exception as err:
                print("Ignore sales navigator link")




        grid = driver.find_elements_by_tag_name("section")[4]
        ptags = grid.find_elements_by_tag_name("p")
        if ptags.__len__() > 0:
            about = grid.find_elements_by_tag_name("p")[0].text.strip()
            company['about'] = about

        values = grid.find_elements_by_tag_name("dd")
        keys = grid.find_elements_by_tag_name("dt")
        i = 0
        for key in keys:
            keyText = key.text.replace(' ', '').lower().strip()
            if keyText == 'companysize':
                rawCmpSize = values[i].text.strip()
                if '+' in rawCmpSize:
                    cmpSizeStr = rawCmpSize.split("+")
                    cmpSize = cmpSizeStr[0].replace(",","")
                    value = int(cmpSize)
                elif '-' in rawCmpSize:
                    cmpSizeStrWithSpace = rawCmpSize.split("-")
                    cmpSizeStr = cmpSizeStrWithSpace[1].split(" ")
                    cmpSize = cmpSizeStr[0].replace(",","")
                    value = int(cmpSize)
                else:
                    cmpSizeStr = rawCmpSize.split(" ")
                    cmpSize = cmpSizeStr[0].replace(",","")
                    value = int(cmpSize)
                i =  i + 2
            else:
                value = values[i].text.strip()
                i = i + 1

            company[keyText] = value


        print(company)


    except TimeoutException:
        print("Loading took too much time!")
    except Exception as ex:
        print(ex)
        print("something went wrong, skip")

    #util.writeFile('resources/companyInfo.json', json.dumps(company))

    return company

def __get_text_under_subtitle(self, elem):
    return "\n".join(elem.text.split("\n")[1:])

def __get_text_under_subtitle_by_class(self, driver, class_name):
    return __get_text_under_subtitle(driver.find_element_by_class_name(class_name))


# Enable to test on local
if __name__ == "__main__":
    print("Started company info extractor")
    proxies = util.getProxies()
    driver = util.openChromeBrowser(proxies)

    input_file = sys.argv[1]
    with open(input_file) as f:
        data = json.load(f)
        i = 1
        records = []
        totalRecordsCompleted = 0
        for company in data:
            print("performing for company " + company['u'])
            companyDetails=execute(driver, company['u'])
            records.append(companyDetails)
            i = i + 1
            totalRecordsCompleted = totalRecordsCompleted + 1
            if(i == 50 or len(data) == totalRecordsCompleted):
                (dt, micro) = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.')
                dt = "%s%03d" % (dt, int(micro) / 1000)
                fileName = "companyPages-" + dt + ".json"
                filecontent = json.dumps(records)
                util.writeFile("output/"+ fileName,filecontent)
                time.sleep(10)
                driver = util.openChromeBrowser(proxies)
                i = 1
                records = []


    print("Ended company info builder")
