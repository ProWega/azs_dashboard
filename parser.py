from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import time
import pandas as pd
import chromedriver_py
from selenium import webdriver
import os
os.environ['MOZ_HEADLESS'] = '0'
#commit
class Parser:
    driver=None
    def __init__(self):
        self.driver = webdriver.Firefox()
    def Azs(self, link):
        name = None
        adress = None
        oil = {}
        link = link
        sourse_of_information = None
        x= None
        y=None
        driver = self.driver
        driver.get(link)
        time.sleep(1)
        if len(driver.find_elements(By.CLASS_NAME, 'something-wrong-view')) == 0:
            try:
                name = driver.find_element(By.TAG_NAME, 'h1').text
                adress = driver.find_element(By.CLASS_NAME, 'business-contacts-view__address-link').text
                price_objects = driver.find_elements(By.CLASS_NAME, 'search-fuel-info-view__rate._has-value')
                for el in price_objects:
                    arr = el.text.split('\n')
                    oil_name = arr[0]
                    oil_price = float(arr[1].replace(',', '.'))
                    oil[oil_name] = oil_price
                link = link
                try:
                    sourse_of_information = driver.find_element(By.CLASS_NAME, 'search-fuel-info-view__info').text
                except Exception as e:
                    sourse_of_information = "Нет источника"
                driver.find_element(By.CLASS_NAME, 'business-contacts-view__address-link').click()
                time.sleep(2)
                try:
                    coord = driver.find_element(By.CLASS_NAME, 'toponym-card-title-view__coords-badge').text
                    x, y = [float(el) for el in coord.split(', ')]
                except Exception as e:
                    print(e)
            except Exception as e:
                print(f"Не получилось спарсить {link}: {e}")


        return {
            "name": name,
            "adress": adress,
            "oil": oil,
            "link": link,
            "sourse_of_information": sourse_of_information,
            "x": x,
            "y": y
        }
if __name__ == '__main__':
    parser = Parser()
    azs = parser.Azs('https://yandex.ru/maps/org/terminal/161407822222/')
    print(azs)
    parser.driver.quit()