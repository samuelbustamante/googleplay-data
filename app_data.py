from BeautifulSoup import BeautifulSoup
import urllib
import re

class AppData(object):

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
            self.set_appId()
            self.set_appName()
            self.set_appIcon()
            self.set_appAuthorName()
            self.set_appAuthorUrl()
            self.set_appDescription()
            self.set_appVersion()
            self.set_appPrice()
            self.set_appCategory()
            self.set_appPublished()
            self.set_appDownloads()
            self.set_appSize()
            self.set_appContentRating()
            self.set_appBanner()
            self.set_appScreenshots()
            self.set_appVideo()
        else:
            self.data['error'] = 'App not found'

    def set_appId(self):
        self.data['appId'] = self.appId

    def set_appName(self):
        appName = self.soup('span', {'itemprop': 'name'})[0]
        self.data['appName'] = appName['content']

    def set_appIcon(self):
        appIcon = self.soup('span', {'itemprop': 'image'})[0]
        self.data['appIcon'] = appIcon['content']

    def set_appAuthorName(self):
        appAuthorName = self.soup('span', {'itemprop': 'author'})[0]
        self.data['appAuthorName'] = appAuthorName('span', {'itemprop': 'name'})[0]['content']

    def set_appAuthorUrl(self):
        appAuthorUrl = self.soup('span', {'itemprop': 'author'})[0]
        self.data['appAuthorUrl'] = appAuthorUrl('span', {'itemprop': 'url'})[0]['content']

    def set_appDescription(self):
        appDescription = self.soup('div', {'itemprop': 'description'})[0]
        self.data['appDescription'] = ' '.join(appDescription.findAll(text=True))

    def set_appRating(self):
        appRating = self.soup('span', {'itemprop': 'ratingCount'})[0]
        self.data['appRating'] = appRating.contents[0]

    def set_appVersion(self):
        appVersion = self.soup('dd', {'itemprop': 'softwareVersion'})[0]
        self.data['appVersion'] = appVersion.contents[0]

    def set_appPrice(self):
        appPrice = self.soup('span', {'itemprop': 'price'})[0]
        self.data['appPrice'] = appPrice['content']

    def set_appCategory(self):
        appCategory = self.soup('a', {'href': re.compile('^/store/apps/category/')})[0]
        self.data['appCategory'] = appCategory.contents[0]

    def set_appPublished(self):
        appPublished = self.soup('time', {'itemprop': 'datePublished'})[0]
        self.data['appPublished'] = appPublished.contents[0]

    def set_appDownloads(self):
        appDownloads = self.soup('dd', {'itemprop': 'numDownloads'})[0]
        self.data['appDownloads'] = appDownloads.contents[0]

    def set_appSize(self):
        appSize = self.soup('dd', {'itemprop': 'fileSize'})[0]
        self.data['appSize'] = appSize.contents[0]

    def set_appContentRating(self):
        appContentRating = self.soup('dd', {'itemprop': 'contentRating'})[0]
        self.data['appContentRating'] = appContentRating.contents[0]

    def set_appBanner(self):
        appBanner = self.soup('div', {'class': 'doc-banner-image-container'})[0]
        self.data['appBanner'] = appBanner.contents[0]['src']

    def set_appScreenshots(self):
        appScreenshots = self.soup('img', {'itemprop': 'screenshot'})
        self.data['appScreenshots'] = [screenshot['src'] for screenshot in appScreenshots]

    def set_appVideo(self):
        appVideo = self.soup('div', {'class': 'doc-video-section'})
        if len(appVideo):
            self.data['appVideo'] = appVideo[0]('param', {'name': 'movie'})[0]['value']
