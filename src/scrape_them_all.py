
import requests
import re

# <li><div class="views-field views-field-title"><span class="field-content"><a href="/epstein/files/DataSet%202/EFTA00003159.pdf">EFTA00003159.pdf</a></span></div></li>

class EpsteinScraper:

    def __init__(self):
        self.start_urls = [
            'https://www.justice.gov/epstein/doj-disclosures/data-set-1-files',
        ]
        self.extractor = re.compile(r'^.*<a href="(/epstein/files/(DataSet[% \d]+)/(EFTA[\d]+.pdf))">\2</a>.*$')


    def start(self):
        for url in self.start_urls:
            response = requests.get(url)
            if response.status_code == 200:
                self.parse(url, response.text)
            else:
                print(f'Failed to retrieve {url}: {response.status_code}')

    def parse(self, url, html):
        # Extract links to individual files
        lines = html.splitlines()
        for line in lines:
            m = self.extractor.match(line)
            if m:
                link = url + '/' + m.group(1)
                group = m.group(2).replace(' ', '_')
                fname = m.group(3)
                self.download(group, fname, link)

    def download(self, group, fname, link):
        import os.path as path
        response = requests.get(url)
        data = response.content
        target_fname = path.join('data', group + '_' + fname)
        with open(target_fname, 'wb') as f:
            f.write(data)


if __name__ == '__main__':
    scraper = EpsteinScraper()
    scraper.start()
