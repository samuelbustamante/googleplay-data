from BeautifulSoup import BeautifulSoup
import urllib
import re

class GooglePlayError404(Exception):
    def __str__(self):
        return 'App not found.'

class GooglePlayData(object):

    def __init__(self, app_id):
        self.data = dict(id=app_id)
        url = 'https://play.google.com/store/apps/details?id='
        request = urllib.urlopen(url + app_id)
        if request.getcode() == 200:
            self.soup = BeautifulSoup(request.read())

            # Set data
            self.set_name()
            self.set_description()
            self.set_average_rating()
            self.set_votes()
            self.set_version()
            self.set_price()
            self.set_published()
            self.set_downloads()
            self.set_size()
            self.set_icon()
            self.set_banner()
            self.set_video()
            self.set_developer_name()
            self.set_developer_url()
            self.set_category_name()
            self.set_category_url()
            self.set_content_rating()
            self.set_screenshots()

        else:
            raise GooglePlayError404()

    def get_data(self):
        return self.data

    def set_name(self):
        data = self.soup('span', {'itemprop': 'name'})[0]
        self.data['name'] = data['content']

    def set_icon(self):
        data = self.soup('span', {'itemprop': 'image'})[0]
        self.data['icon'] = data['content']

    def set_developer_name(self):
        data = self.soup('span', {'itemprop': 'author'})[0]
        self.data['developer_name'] = data('span', {'itemprop': 'name'})[0]['content']

    def set_developer_url(self):
        data = self.soup('span', {'itemprop': 'author'})[0]
        self.data['developer_url'] = data('span', {'itemprop': 'url'})[0]['content']

    def set_description(self):
        data = self.soup('div', {'itemprop': 'description'})[0]
        self.data['description'] = ' '.join(data.findAll(text=True))

    def set_votes(self):
        data = self.soup('div', {'class' : 'votes'})
        if len(data) > 0:
            self.data['votes'] = int(data[0].contents[0].replace(',', ''))
        else:
            self.data['votes'] = 0

    def set_average_rating(self):
        data = self.soup('div', {'class': 'average-rating-value'})
        if len(data) > 0:
            self.data['average_rating'] = float(data[0].contents[0])
        else:
            self.data['average_rating'] = 0.0

    def set_version(self):
        data = self.soup('dd', {'itemprop': 'softwareVersion'})[0]
        self.data['version'] = data.contents[0]

    def set_price(self):
        data = self.soup('span', {'itemprop': 'price'})[0]
        self.data['price'] = float(data['content'].replace('$', ''))

    def set_category_name(self):
        data = self.soup('a', {'href': re.compile('^/store/apps/category/')})[0]
        self.data['category_name'] = data.contents[0]

    def set_category_url(self):
        data = self.soup('a', {'href': re.compile('^/store/apps/category/')})[0]
        self.data['category_url'] = data['href']

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
        data = self.soup('div', {'class': 'doc-banner-image-container'})
        if len(data) > 0:
            self.data['banner'] = data[0].contents[0]['src']
        else:
            self.data['banner'] = ''

    def set_screenshots(self):
        data = self.soup('img', {'itemprop': 'screenshot'})
        self.data['screenshots'] = [screenshot['src'] for screenshot in data]

    def set_video(self):
        data = self.soup('div', {'class': 'doc-video-section'})
        if len(data) > 0:
            self.data['video'] = data[0]('param', {'name': 'movie'})[0]['value']
        else:
            self.data['video'] = ''
