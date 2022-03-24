from facebook_scraper import get_posts


class FbPostLinkScraper:

    def __init__(self):
        self.posts = []

    def scrape_post_links(self, fbName):
        for post in get_posts(fbName, pages=13):
            # print(post['post_url'])
            self.posts.append(post['post_url'])

        return self.posts, len(self.posts)

        # reidandtaylor
        # ZOAenergy
        # MiraGasAS
        # RaisinEnt




