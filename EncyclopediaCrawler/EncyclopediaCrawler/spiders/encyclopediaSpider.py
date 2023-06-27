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
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'LOG_FILE': 'logs/encyclopediaSpider.log'
    }

    rules = (
        Rule(LinkExtractor(unique=True), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        title = soup.title.string.strip()
        print("Title:", title)

        content = soup.get_text().strip()
        print("Content:", content)

        # Store data in a dictionary
        data = {
            'url': response.url,
            'title': title,
            'content': content
            # Add more data fields as needed
        }

        # Save data as JSON
        with open('data.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            f.write('\n')