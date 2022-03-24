# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import time


class FbCommentScraper:

    def __init__(self):
        self.comments = []
        self.option = Options()
        self.option.add_argument("--disable-infobars")
        self.option.add_argument("start-maximized")
        self.option.add_argument("--disable-extensions")
        # Pass the argument 1 to allow and 2 to block
        self.option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 1
        })
        self.driver = webdriver.Chrome(options=self.option)

    def scrape_comments(self, posts):
        # go to insta first
        self.driver.maximize_window()
        self.driver.get("https://www.facebook.com/")
        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
        # enter username and password
        username.clear()
        username.send_keys("")
        password.clear()
        password.send_keys("")
        # target the login button and click it
        WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        time.sleep(2)

        # posts = ['https://www.facebook.com/ChinaPressCP/posts/4614926295266446']
        # posts = ['https://www.facebook.com/ChinaPressCP/posts/4652732488152493']
        # posts = ['https://www.facebook.com/TGVCinemas/posts/5089709007724129']
        # posts = ['https://www.facebook.com/RaisinEnt/posts/4497360503660207']
        # posts = ['https://www.facebook.com/TGVCinemas/posts/5103172099711153']
        # posts = ['https://facebook.com/TGVCinemas/posts/5103040283057668']
        # posts = ['https://facebook.com/TGVCinemas/posts/5107168059311557']
        # posts = ['https://facebook.com/TGVCinemas/posts/5093106507384379']
        # posts = ['https://www.facebook.com/TGVCinemas/posts/5106219426073087']
        for post in posts:
            self.driver.get(post)
            time.sleep(5)
            # testButton = self.driver.find_element_by_css_selector("div[class='j83agx80 bkfpd7mw jb3vyjys hv4rvrfc qt6c0cv9 dati1w0a l9j0dhe7']").find_element_by_css_selector("div[class='j83agx80 buofh1pr jklb3kyz l9j0dhe7']")
            # testClick = self.driver.find_element_by_css_selector("div[class='cwj9ozl2 tvmbv18p']").click()

            postComments = self.driver.find_elements_by_css_selector("div[class='cwj9ozl2 tvmbv18p']")
            # STANDARD POSTS
            if len(postComments) > 0:
                print('standard post!')
                postComments = self.driver.find_element_by_css_selector("div[class='cwj9ozl2 tvmbv18p']")
                time.sleep(3)
                print(postComments)
                # load more comments (if ada)
                # has two div[class='j83agx80 bkfpd7mw jb3vyjys hv4rvrfc qt6c0cv9 dati1w0a l9j0dhe7'] in one post
                # (optional) here can add loadMoreComments = postComments.find_elements_by_css_selector("div[class='j83agx80 bkfpd7mw jb3vyjys hv4rvrfc qt6c0cv9 dati1w0a l9j0dhe7']") and if/else statement first to check
                # whether this element exist even though cwj9 (element above) exists (just in case for special facebook post)
                # use only if no need else (no need set postComments yet)
                loadMoreComments = postComments.find_elements_by_css_selector("div[class='j83agx80 bkfpd7mw jb3vyjys hv4rvrfc qt6c0cv9 dati1w0a l9j0dhe7']")[0].find_elements_by_css_selector("div[class='j83agx80 buofh1pr jklb3kyz l9j0dhe7']")
                if len(loadMoreComments) == 0:
                    loadMoreComments = postComments.find_elements_by_css_selector("div[class='j83agx80 bkfpd7mw jb3vyjys hv4rvrfc qt6c0cv9 dati1w0a l9j0dhe7']")[1].find_elements_by_css_selector("div[class='j83agx80 buofh1pr jklb3kyz l9j0dhe7']")
                print(loadMoreComments)
                while len(loadMoreComments) > 0:
                    try:
                        loadMoreComments[0].click()
                    except ElementClickInterceptedException:
                        pass
                    time.sleep(5)
                    print(loadMoreComments)
                    # using postComments.find here solves staleElementException problem
                    loadMoreComments = postComments.find_elements_by_css_selector("div[class='j83agx80 bkfpd7mw jb3vyjys hv4rvrfc qt6c0cv9 dati1w0a l9j0dhe7']")[1].find_elements_by_css_selector("div[class='j83agx80 buofh1pr jklb3kyz l9j0dhe7']")
                time.sleep(3)
                # end here
                # can use for loop for check whether rj exists in ul if exist then use that ul
                # can use postComments.find_elements_by_css_selector('ul') and if/else statement to check
                # use both if and else (else: postComments = []) - for posts with no comments
                checkUL = postComments.find_elements_by_css_selector('ul')
                if len(checkUL) > 0:
                    print("checkUL")
                    print(len(checkUL))
                    print('next')
                    for ul in checkUL:
                        elem = ul.find_elements_by_css_selector("div[class='rj1gh0hx buofh1pr ni8dbmo4 stjgntxs hv4rvrfc']")
                        time.sleep(2)
                        if len(elem) > 0:
                            postComments = ul.find_elements_by_css_selector("div[class='rj1gh0hx buofh1pr ni8dbmo4 stjgntxs hv4rvrfc']")
                            break
                        else:
                            postComments = []
                    # postComments = postComments.find_element_by_css_selector('ul').find_elements_by_css_selector("div[class='rj1gh0hx buofh1pr ni8dbmo4 stjgntxs hv4rvrfc']")
                else:
                    postComments = []
                print(len(postComments))
                for postComment in postComments:
                    # to avoid stickers etc
                    try:
                        postComment = postComment.find_element_by_css_selector("div[class='tw6a2znq sj5x9vvc d1544ag0 cxgpxx05']").find_element_by_css_selector("div[class='ecm0bbzt e5nlhep0 a8c37x1j']")
                        # .find_element_by_css_selector("div[class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']")
                        time.sleep(3)
                        # load See More
                        hasSeeMore = postComment.find_elements_by_css_selector("div[class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p']")
                        time.sleep(3)
                        while len(hasSeeMore) > 0:
                            try:
                                hasSeeMore[0].click()
                            except ElementClickInterceptedException:
                                pass
                            time.sleep(5)
                            print('OHYEAH!')
                            hasSeeMore = postComment.find_elements_by_css_selector("div[role='button']")
                        time.sleep(3)
                        finalComment = ''
                        finalComment = finalComment + postComment.text
                        time.sleep(3)
                        emojis = postComment.find_elements_by_tag_name('img')
                        for emoji in emojis:
                            finalComment = finalComment + emoji.get_attribute('alt')
                        print(finalComment)
                        self.comments.append(finalComment)
                    except NoSuchElementException:
                        pass
            # FACEBOOK WATCH
            else:
                print('facebook watch!')
                postComments = self.driver.find_elements_by_css_selector("div[class='cwj9ozl2 j83agx80 cbu4d94t buofh1pr ni8dbmo4 stjgntxs du4w35lb']")
                if len(postComments) > 0:
                    postComments = self.driver.find_element_by_css_selector("div[class='cwj9ozl2 j83agx80 cbu4d94t buofh1pr ni8dbmo4 stjgntxs du4w35lb']")
                    time.sleep(3)
                    print(postComments)
                    # view more comments (if ada)
                    # only has one div[class='l6v480f0 pfnyh3mw kvgmc6g5 wkznzc2l oygrvhab dhix69tm j83agx80 bkfpd7mw'] in one post
                    loadMoreComments = postComments.find_elements_by_css_selector("div[class='l6v480f0 pfnyh3mw kvgmc6g5 wkznzc2l oygrvhab dhix69tm j83agx80 bkfpd7mw']")[0].find_elements_by_css_selector("div[class='j83agx80 buofh1pr jklb3kyz l9j0dhe7']")
                    print(loadMoreComments)
                    while len(loadMoreComments) > 0:
                        try:
                            loadMoreComments[0].click()
                        except ElementClickInterceptedException:
                            pass
                        time.sleep(5)
                        print(loadMoreComments)
                        # using postComments.find here solves staleElementException problem
                        loadMoreComments = postComments.find_elements_by_css_selector("div[class='l6v480f0 pfnyh3mw kvgmc6g5 wkznzc2l oygrvhab dhix69tm j83agx80 bkfpd7mw']")[0].find_elements_by_css_selector("div[class='j83agx80 buofh1pr jklb3kyz l9j0dhe7']")
                    time.sleep(3)
                    # end here
                    checkUL = postComments.find_elements_by_css_selector('ul')
                    # for watch with no comments
                    if len(checkUL) > 0:
                        print("checkUL")
                        print(len(checkUL))
                        print('next')
                        for ul in checkUL:
                            elem = ul.find_elements_by_css_selector("div[class='rj1gh0hx buofh1pr ni8dbmo4 stjgntxs hv4rvrfc']")
                            time.sleep(2)
                            if len(elem) > 0:
                                postComments = ul.find_elements_by_css_selector("div[class='rj1gh0hx buofh1pr ni8dbmo4 stjgntxs hv4rvrfc']")
                                break
                            else:
                                postComments = []
                    else:
                        postComments = []
                    print(len(postComments))
                    for postComment in postComments:
                        # to avoid stickers etc
                        try:
                            postComment = postComment.find_element_by_css_selector("div[class='tw6a2znq sj5x9vvc d1544ag0 cxgpxx05']").find_element_by_css_selector("div[class='ecm0bbzt e5nlhep0 a8c37x1j']")
                            # .find_element_by_css_selector("div[class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']")
                            time.sleep(3)
                            # load See More
                            hasSeeMore = postComment.find_elements_by_css_selector("div[class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p']")
                            time.sleep(3)
                            while len(hasSeeMore) > 0:
                                try:
                                    hasSeeMore[0].click()
                                except ElementClickInterceptedException:
                                    pass
                                time.sleep(5)
                                print('OHYEAH!')
                                hasSeeMore = postComment.find_elements_by_css_selector("div[role='button']")
                            time.sleep(3)
                            finalComment = ''
                            finalComment = finalComment + postComment.text
                            time.sleep(3)
                            emojis = postComment.find_elements_by_tag_name('img')
                            for emoji in emojis:
                                finalComment = finalComment + emoji.get_attribute('alt')
                            print(finalComment)
                            self.comments.append(finalComment)
                        except NoSuchElementException:
                            pass
        time.sleep(2)
        self.driver.close()
        return self.comments


# x = CommentScraper()
# comments = x.scrape_comments()
# print(comments)
# print(len(comments))
