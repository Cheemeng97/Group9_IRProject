import scrapy
import datetime
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup

class EncyclopediaSpider(CrawlSpider):
    handle_httpstatus_list = [400, 403, 404, 500, 502, 503, 504]
    name = 'encyclopediaspider'
    allowed_domains = ['encyclopedia.com']
    start_urls = ['https://www.encyclopedia.com/']
    # custom_settings = {
    #     'LOG_FILE': 'logs/encyclopediaSpider.log',
    #     'LOG_LEVEL': 'DEBUG'
    # }

    rules = (
        Rule(LinkExtractor(unique=True), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        title = soup.title.string.strip()
        # print("Title:", title)

        content = soup.get_text().strip()
        # print("Content:", content)

        # Store data in a dictionary
        data = {
            'url': response.url,
            'title': title,
            'content': content
            # Add more data fields as needed
        }

        # Check if the URL exists in data.json
        if self.url_exists_in_json(response.url):
            print("URL already exists in data.json. Skipping crawl.")
        else:
            # Save data as JSON
            with open('data.json', 'a', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
                f.write('\n')

    def url_exists_in_json(self, url):
        with open('data.json', 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                if data['url'] == url:
                    return True
        return False