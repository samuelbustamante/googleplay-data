from BeautifulSoup import BeautifulSoup
import urllib
import re

class GooglePlayData(object):

    def __init__(self, appId):
        self.appId = appId
        self.data = dict()
        self.url = 'https://play.google.com/store/apps/details?id='
        self.request = urllib.urlopen(self.url + self.appId)

    def get_data(self):
        return self.data

    def set_data(self):

        if self.request.getcode() == 200:
            self.soup = BeautifulSoup(self.request.read())

            # Set data
            self.set_id()
            self.set_name()
            self.set_icon()
            self.set_name_developer()
            self.set_url_developer()
            self.set_description()
            self.set_votes()
            self.set_average_rating()
            self.set_version()
            self.set_price()
            self.set_category()
            self.set_url_category()
            self.set_published()
            self.set_downloads()
            self.set_size()
            self.set_content_rating()
            self.set_banner()
            self.set_screenshots()
            self.set_video()

        else:
            self.data['error'] = 'App not found'

    def set_id(self):
        self.data['id'] = self.appId

    def set_name(self):
        data = self.soup('span', {'itemprop': 'name'})[0]
        self.data['name'] = data['content']

    def set_icon(self):
        data = self.soup('span', {'itemprop': 'image'})[0]
        self.data['icon'] = data['content']

    def set_name_developer(self):
        data = self.soup('span', {'itemprop': 'author'})[0]
        self.data['name_developer'] = data('span', {'itemprop': 'name'})[0]['content']

    def set_url_developer(self):
        data = self.soup('span', {'itemprop': 'author'})[0]
        self.data['url_developer'] = data('span', {'itemprop': 'url'})[0]['content']

    def set_description(self):
        data = self.soup('div', {'itemprop': 'description'})[0]
        self.data['description'] = ' '.join(data.findAll(text=True))

    def set_votes(self):
        data = self.soup('div', {'class' : 'votes'})[0]
        self.data['votes'] = data.contents[0]

    def set_average_rating(self):
        data = self.soup('div', {'class': 'average-rating-value'})[0]
        self.data['average_rating'] = data.contents[0]

    def set_version(self):
        data = self.soup('dd', {'itemprop': 'softwareVersion'})[0]
        self.data['version'] = data.contents[0]

    def set_price(self):
        data = self.soup('span', {'itemprop': 'price'})[0]
        self.data['price'] = data['content']

    def set_category(self):
        data = self.soup('a', {'href': re.compile('^/store/apps/category/')})[0]
        self.data['category'] = data.contents[0]

    def set_url_category(self):
        data = self.soup('a', {'href': re.compile('^/store/apps/category/')})[0]
        self.data['url_category'] = data['href']

    def set_published(self):
        data = self.soup('time', {'itemprop': 'datePublished'})[0]
        self.data['published'] = data.contents[0]

    def set_downloads(self):
        data = self.soup('dd', {'itemprop': 'numDownloads'})[0]
        self.data['downloads'] = data.contents[0]

    def set_size(self):
        data = self.soup('dd', {'itemprop': 'fileSize'})[0]
        self.data['size'] = data.contents[0]

    def set_content_rating(self):
        data = self.soup('dd', {'itemprop': 'contentRating'})[0]
        self.data['content_rating'] = data.contents[0]

    def set_banner(self):
        data = self.soup('div', {'class': 'doc-banner-image-container'})[0]
        self.data['banner'] = data.contents[0]['src']

    def set_screenshots(self):
        data = self.soup('img', {'itemprop': 'screenshot'})
        self.data['screenshots'] = [screenshot['src'] for screenshot in data]

    def set_video(self):
        data = self.soup('div', {'class': 'doc-video-section'})
        if len(data) > 0:
            self.data['video'] = data[0]('param', {'name': 'movie'})[0]['value']
