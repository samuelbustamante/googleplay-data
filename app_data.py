from BeautifulSoup import BeautifulSoup
import urllib

class AppData(object):

    def __init__(self, appId):
        self.data = dict()
        self.url  = 'http://play.google.com/store/apps/details?id='
        self.html = urllib.urlopen(self.url + appId).read()
        self.soup = BeautifulSoup(self.html)
        self.set_appId(appId)

    def get_data(self):
        return self.data

    def set_data(self):
        self.set_appDev()
        self.set_appDesc()
        self.set_appName()
        self.set_appRating()

    def set_appId(self, appId):
        self.data['appId'] = appId

    def set_appDev(self):
        appDev = self.soup('a', {'class': 'doc-header-link'})[0]
        self.data['appDev'] = appDev.contents[0]

    def set_appDesc(self):
        appDesc = self.soup('div', {'itemprop': 'description'})[0]
        self.data['appDesc'] = ' '.join(appDesc.findAll(text=True))

    def set_appName(self):
        appName = self.soup('h1', {'class': 'doc-banner-title'})[0]
        self.data['appName'] = appName.contents[0]

    def set_appRating(self):
        appRating = self.soup('span', {'itemprop': 'ratingCount'})[0]
        self.data['appRating'] = appRating.contents[0]
