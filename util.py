import csv
import os
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def arrayToCSV(fileName, data):
    with open(fileName, mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for item in data:
            writer.writerow([item])



def dictToCSV(fileName, data):
    with open(fileName, mode='a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for key in data:
            writer.writerow([key, data[key]])



def writeFile(fileName, data):
    with open(fileName, mode='a') as csv_file:
        csv_file.write(data +',\n')


def readPagesFromFile(fileName):
    f = open(fileName, "r")
    return f.read()

def openChromeBrowser(proxies):

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--incognito')
    #options.add_argument('--headless')
    currentIp = proxies[random.randint(0,len(proxies))]
    print("Current Ip being used: " +  currentIp)
    options.add_argument('--proxy-server={}'.format(currentIp))
    driver = webdriver.Chrome(os.environ.get('CHROME_DRIVER_BASE'), options=options)
    driver.maximize_window()
    username = None
    try:
        driver.get("https://www.linkedin.com/login")
        username = driver.find_element_by_id("username")
    except Exception as ex:
        print(ex)
        print("Ip not working")
        while(username == None):
            try:
                options = webdriver.ChromeOptions()
                options.add_argument('--ignore-certificate-errors')
                currentIp = proxies[random.randint(0, len(proxies))]
                print("Current Ip being used: " + currentIp)
                options.add_argument('--proxy-server={}'.format(currentIp))
                driver = webdriver.Chrome(os.environ.get('CHROME_DRIVER_BASE'), options=options)
                driver.maximize_window()
                driver.get("https://www.linkedin.com/login")
                username = driver.find_element_by_id("username")
            except Exception as exce:
                print(ex)
                print("Ip not working")

    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")

    username.send_keys(os.environ.get('LINKEDIN_USERNAME'))
    password.send_keys(os.environ.get('LINKEDIN_PASSWORD'))

    login_button = driver.find_element_by_xpath("//*[@id='organic-div']/form/div[3]/button")

    login_button.click()
    print("login success")
    return driver

def getProxies():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(chrome_options=options, executable_path=os.environ.get('CHROME_DRIVER_BASE'))
    driver.get("https://sslproxies.org/")
    driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH,
                                          "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))))
    ips = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(
        EC.visibility_of_all_elements_located((By.XPATH,
                                               "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
    ports = [my_elem.get_attribute("innerHTML") for my_elem in WebDriverWait(driver, 5).until(
        EC.visibility_of_all_elements_located((By.XPATH,
                                               "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]
    driver.quit()
    proxies = []
    for i in range(0, len(ips)):
        proxies.append(ips[i] + ':' + ports[i])
    print(proxies)
    return proxies