import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import openpyxl
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import math
import re

loginUrl='https://steamcommunity.com/login/home/?goto='
username= "bregva2001"
password= "gvanca2003"
authcode= "8w89q"
TIMEOUT = 0.5
LOGINTIME= 5

class SteamScraper():
    def __init__(self):
        self.loginUrl = "https://steamcommunity.com/login/home/?goto="
    def headlessDriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--window-size=1920, 900")
        chrome_options.add_argument("--hide-scrollbars")
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    def headDriver(self):
        options = Options()
        options.headless = False
        unpacked_extension_path = 'C:/Users/bikks/AppData/Local/Google/Chrome/User Data/Default/Extensions/kaibcgikagnkfgjnibflebpldakfhfih/2.9_0'
        options.add_argument("--window-size=1920,1200")
        options.add_argument('--load-extension={}'.format(unpacked_extension_path))
        try:
            driver = webdriver.Chrome(options=options, executable_path="chromedriver86.exe")
            return driver
        except:
            print("You must install chrome 86!")
            return 0
    def load(self, filename):
        f = open(filename, "r")
        itemUrls= []
        for x in f:
            itemUrls.append(x)
        f.close()
        return itemUrls
    def scrape(self):
        # write csv headers
        if os.path.exists('result.csv'):
            os.remove('result.csv')
        columns=['Item Name', 'Activity']
        df = pd.DataFrame(columns = columns)
        df.to_csv('result.csv', mode='x', index=False, encoding='utf-8')

        # get item urls
        itemUrls= self.load('itemUrls.txt')
        driver= self.headDriver()
        driver.get(self.loginUrl)
        time.sleep(5)
        driver.find_element_by_id("input_username").send_keys(username) # set username
        driver.find_element_by_id("input_password").send_keys(password) # set password
        try:
            driver.find_element_by_id("remember_login").click()
        except:
            print("You don't need to remember!")
        driver.find_element_by_xpath("//button[@class='btn_blue_steamui btn_medium login_btn']").click()
        time.sleep(LOGINTIME)

        # this is authcode part
        # driver.find_element_by_id("authcode").send_keys(authcode)
        # time.sleep(5)
        # driver.find_element_by_class_name('auth_button leftbtn').click()
        # time.sleep(1)
        total= []
        while True:
            activitys= []
            cnt= 0
            for itemUrl in itemUrls:
                cnt+=1
                driver.get(itemUrl)
                time.sleep(TIMEOUT)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                itemNameDom= soup.find('div', attrs={'class':'market_listing_nav'})
                if itemNameDom!= None:
                    itemName= itemNameDom.text
                    activityDoms= soup.find_all('div', attrs={'class':'market_activity_line_item ellipsis'})
                    for activityDom in activityDoms: 
                        if activityDom!= None:
                            activity= activityDom.text
                            new= {'Item Name': itemName, 'Activity': activity}
                            if new not in total:
                                activitys.append(new)
                    print("item "+ str(cnt)+ " is saved in array!")
                else:
                    driver.refresh()
                    print("You accessed too many times! So I have refreshed! :D")
                    time.sleep(2)
            df = pd.DataFrame(activitys, columns = columns)
            print("Now items writed in csv file!")
            df.to_csv('result.csv', mode='a', header=False, index=False, encoding='utf-8')
            total+= activitys
           
if __name__ == '__main__':
    scraper = SteamScraper()
    scraper.scrape()