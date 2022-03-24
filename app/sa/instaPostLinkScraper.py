# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


class InstaPostLinkScraper:

    def __init__(self):
        self.posts = set()
        self.driver = webdriver.Chrome()

    def scrape_post_links(self, instaLink):
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # self.driver = webdriver.Chrome()

        # go to insta first
        self.driver.maximize_window()
        self.driver.get("https://www.instagram.com/")
        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

        # enter username and password
        username.clear()
        username.send_keys("")
        password.clear()
        password.send_keys("")

        # target the login button and click it
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        # Not now alert
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

        # go to client link
        self.driver.get(instaLink)

        time.sleep(5)
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        links = self.driver.find_elements_by_tag_name('a')
        time.sleep(5)
        for link in links:
            post = link.get_attribute('href')
            if '/p/' in post:
                self.posts.add(post)

        # scroll to the bottom of the page and find all links on the page and if they match '/p' append to set named posts
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        lenOfPage = self.driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(5)
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        links = self.driver.find_elements_by_tag_name('a')
        time.sleep(5)
        for link in links:
            post = link.get_attribute('href')
            if '/p/' in post:
                self.posts.add(post)

        match = False
        while not match:
            lastCount = lenOfPage
            time.sleep(5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            lenOfPage = self.driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            time.sleep(5)
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
            links = self.driver.find_elements_by_tag_name('a')
            time.sleep(5)
            for link in links:
                post = link.get_attribute('href')
                if '/p/' in post:
                    self.posts.add(post)
            if lastCount == lenOfPage:
                match = True

        time.sleep(5)
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        links = self.driver.find_elements_by_tag_name('a')
        time.sleep(5)
        for link in links:
            post = link.get_attribute('href')
            if '/p/' in post:
                self.posts.add(post)

        print(self.posts)
        print(len(self.posts))
        self.posts = list(self.posts)
        self.driver.close()
        return self.posts, len(self.posts)
