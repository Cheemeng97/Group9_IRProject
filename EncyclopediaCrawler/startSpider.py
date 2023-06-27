from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from EncyclopediaCrawler.spiders.encyclopediaSpider import EncyclopediaSpider
from collections.abc import MutableMapping

# Run the spider
process = CrawlerProcess(get_project_settings())
process.crawl(EncyclopediaSpider)
process.start()

# Run multiple spiders
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings

# from EncyclopediaCrawler.spiders.spider1 import Spider1
# from EncyclopediaCrawler.spiders.spider2 import Spider2
# from EncyclopediaCrawler.spiders.spider3 import Spider3

# # Create a list of spiders to run
# spiders = [Spider1, Spider2, Spider3]

# # Run the spiders
# process = CrawlerProcess(get_project_settings())
# for spider_cls in spiders:
#     process.crawl(spider_cls)
# process.start()