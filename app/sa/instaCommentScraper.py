# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


class InstaCommentScraper:

    def __init__(self):
        self.comments = []
        self.driver = webdriver.Chrome()

    def scrape_comments(self, posts):
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

        for post in posts:
            self.driver.get(post)
            time.sleep(5)
            # elementList = self.driver.find_elements_by_css_selector("span[class='g47SY ']")
            # amended code (load more button being weird and NUiEW class - no more dCJp8 afkep)
            # NUiEW appears twice for posts that have 2 accounts linked (like espn and sportscenter), one for logo, one for loadMore
            elementList = self.driver.find_elements_by_class_name('NUiEW')
            time.sleep(3)
            while len(elementList) > 0:
                before = self.driver.find_element_by_class_name("XQXOT").find_elements_by_class_name("Mr508")
                time.sleep(3)
                for element in elementList:
                    loadMoreButton = element.find_elements_by_class_name('wpO6b')
                    if len(loadMoreButton) > 0:
                        loadMoreButton[0].click()
                        time.sleep(5)
                time.sleep(3)
                after = self.driver.find_element_by_class_name("XQXOT").find_elements_by_class_name("Mr508")
                time.sleep(3)
                if len(before) == len(after):
                    break
                elementList = self.driver.find_elements_by_class_name('NUiEW')
                time.sleep(3)
            time.sleep(3)
            # postComments = self.driver.find_elements_by_class_name('_97aPb')
            postComments = self.driver.find_element_by_class_name("XQXOT").find_elements_by_class_name("Mr508")
            for postComment in postComments:
                d = postComment.find_element_by_class_name("ZyFrc").find_element_by_tag_name(
                    "li").find_element_by_class_name("P9YgZ").find_element_by_class_name(
                    "C7I1f").find_element_by_class_name("C4VMK")
                post = d.find_elements_by_tag_name("span")
                if len(post) == 2:
                    self.comments.append(post[1].text)
                else:
                    self.comments.append(post[2].text)
        time.sleep(2)
        self.driver.close()
        return self.comments
