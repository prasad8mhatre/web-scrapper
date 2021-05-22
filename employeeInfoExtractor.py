import datetime
import json
import os
import sys
import time
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import util


def execute(sessionId, companyDetail, driver):
    print("Fetching company info for : " + companyDetail['name'])

    try:
        company_base_urls = getCompanyBaseUrls(sessionId, companyDetail)

        company_urls_with_pages = getCompanyUrlsWithPages(company_base_urls, driver)

        fetchAndSaveEmployees(company_urls_with_pages, companyDetail, driver)
    except TimeoutException:
        print("Loading took too much time!")


def getCompanyBaseUrls(sessionId, companyDetail):
    base_sales_navigator_url = "https://www.linkedin.com/sales/search/people/list/employees-for-account/"
    company_url = base_sales_navigator_url + companyDetail['companyId'] + "?searchSessionId=" + sessionId
    company_base_urls = []
    ########################################
    # seniority levels : 10 Owner
    #                    9 Partner
    #                    8 CXO
    #                    7 VP
    #                    6 Director
    ########################################
    if companyDetail['companysize'] > 2500:
        for i in range(6, 11, 1):
            company_url_with_seniority = company_url + "&seniorityIncluded=" + str(i)
            company_base_urls.append(company_url_with_seniority)

    else:
        company_base_urls.append(company_url)
    return company_base_urls


def getCompanyUrlsWithPages(company_base_urls, driver):
    company_urls_with_pages = []
    for company_base_url in company_base_urls:
        driver.get(company_base_url)
        # get total no of pages
        pages = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "search-results__pagination-list")))[0].text.split("\n")

        last_page = pages[len(pages) - 1]
        lsize = last_page.split(" ")
        no_of_pages = 0;
        if (len(lsize) == 2):
            no_of_pages = lsize[1]
        else:
            no_of_pages = lsize[0]

        # fetch empl info per page
        for i in range(1, int(no_of_pages) + 1):
            company_url_with_page = company_base_url + "&page=" + str(i)
            company_urls_with_pages.append(company_url_with_page)
    return company_urls_with_pages


def fetchAndSaveEmployees(company_urls_with_pages, companyDetail, driver):
    employees = []
    for company_url_with_page in company_urls_with_pages:
        print("Opening new page...")
        driver.get(company_url_with_page)
        employee_list = driver.find_elements_by_class_name("search-results__result-item")


        (dt, micro) = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.')
        dt = "%s%03d" % (dt, int(micro) / 1000)
        fileName = "output/employees/employeePages-" + dt + ".json"
        for employee in employee_list:
            try:

                employee_element = extractEmployeeElement(driver, employee)
                if (employee_element == None):
                    employee_element = extractEmployeeElement(driver, employee)

                employee_name = employee_element.text
                employee_link = employee_element.find_element_by_tag_name("a").get_attribute(
                    "href")
                employee_designation = employee.find_elements_by_tag_name("dd")[1].text.split("at")[0].strip()
                employee_location = employee.find_elements_by_tag_name("dd")[3].text

                employee_info = {}
                employee_info['company'] = companyDetail
                employee_info['name'] = employee_name
                firstname = ""
                lastname = ""
                split_content = employee_name.split(" ", 1)
                len_of_name = len(split_content)
                if len_of_name == 1:
                    firstname = split_content[0]
                elif len_of_name == 2:
                    firstname = split_content[0]
                    lastname = split_content[1]

                employee_info['firstname'] = firstname
                employee_info['lastname'] = lastname

                employee_info['link'] = employee_link
                employee_info['designation'] = employee_designation
                employee_info['location'] = employee_location
                employees.append(employee_info)


                print(employee_info)
                util.writeFile(fileName, json.dumps(employee_info))
                if(len(employees) == 10):
                    break
            except Exception as e:
                print("Error occured while fetching info for " + str(e))

        if (len(employees) == 10):
            break

    return employees



def extractEmployeeElement(driver, employee):
    try:
        element = employee.find_element_by_tag_name("dt")
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(1)
        return element
    except Exception as e:
        print("Error for extractEmployeeElement " + str(e))
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
    return None


def __get_text_under_subtitle(self, elem):
    return "\n".join(elem.text.split("\n")[1:])


def __get_text_under_subtitle_by_class(self, driver, class_name):
    return __get_text_under_subtitle(driver.find_element_by_class_name(class_name))


# Enable to test on local
if __name__ == "__main__":
    sessionId = os.environ.get('LINKEDIN_SESSION_ID')
    proxies = util.getProxies()
    driver = util.openChromeBrowser(proxies)
    input_file = sys.argv[1]
    with open(input_file) as f:
        data = json.load(f)
        i = 1
        records = []
        for company in data:
            print("performing for company " + company['u'])
            del company['about']
            companyDetails = execute(sessionId, company, driver)
            records.append(companyDetails)
            i = i + 1
            totalRecordsCompleted = totalRecordsCompleted + 1
            if (i == 10 or len(data) == totalRecordsCompleted):
                (dt, micro) = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.')
                dt = "%s%03d" % (dt, int(micro) / 1000)
                fileName = "employees-" + dt + ".json"
                filecontent = json.dumps(records)
                util.writeFile("output/"+ fileName,filecontent)
                time.sleep(10)
                i = 1
                records = []
