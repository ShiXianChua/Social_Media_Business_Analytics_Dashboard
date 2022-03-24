from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import time
import pandas as pd


class InfluencerDataScraper:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def scrape_data(self, inf_links):
        # go to insta first
        self.driver.maximize_window()
        self.driver.get("https://www.instagram.com/")
        username = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
        # enter username and password
        username.clear()
        username.send_keys("")
        password.clear()
        password.send_keys("")
        # target the login button and click it
        WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        # Not now alert
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

        inf_df = pd.DataFrame(columns=['name', 'img', 'posts', 'followers', 'following'])
        for url in inf_links:
            data = []
            self.driver.get(url)
            time.sleep(3)
            name = self.driver.find_element_by_class_name('XBGH5').find_element_by_class_name('_7UhW9').text
            data.append(name)
            time.sleep(5)
            images = self.driver.find_elements_by_class_name('_6q-tv')
            infImage = images[0]
            infImage = infImage.get_attribute('src')
            data.append(infImage)
            time.sleep(5)
            basics = self.driver.find_elements_by_class_name("g47SY")
            for basic in basics:
                text = basic.text
                data.append(text)
            data_series = pd.Series(data, index=['name', 'img', 'posts', 'followers', 'following'])
            inf_df = inf_df.append(data_series, ignore_index=True)
        print(inf_df)
        self.driver.close()
        return inf_df
