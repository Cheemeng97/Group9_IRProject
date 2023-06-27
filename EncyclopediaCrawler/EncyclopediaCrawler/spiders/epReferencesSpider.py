import scrapy

encyclopediaDefaultUrl = "https://www.encyclopedia.com"

class DiscoveryRefSpider(scrapy.Spider):
    name = "epReferences"
    start_urls = [encyclopediaDefaultUrl + "/" ]

    def parse(self, response):
        # Extract categories from the "categories" div
        categories_div = response.css('div.categories')

        category_links = categories_div.css('a::attr(href)').getall()
        # Process or store the extracted category links as desired
        for link in category_links:
            if "article" not in link:
                link = encyclopediaDefaultUrl + link
                if "daily" not in link:
                    link = link + "/"

            if "references" in link:
                # print(link)
                yield response.follow(link, callback=self.parse_mainCategorypages, cb_kwargs={'link': link})

    def parse_mainCategorypages(self, response, link):
        pagination_ul = response.css('ul.pager__items.js-pager__items')
        page_numbers = pagination_ul.css('li.pager__item:not(.pager__item.pager__item--next):not(.pager__item.pager__item--last) a::attr(href)').getall()
        for pageNumber in page_numbers:
            pageNumber = link + pageNumber + "/"
            yield response.follow(pageNumber, callback=self.parse_mainCategory)

    def parse_mainCategory(self, response):
        mainCategories_div = response.css('div.main-section')

        mainCategories_links = mainCategories_div.css('div.a::attr(href)').getall()
        print(mainCategories_links)
        # for mainLink in mainCategories_links:
        #     mainLink = encyclopediaDefaultUrl + mainLink + "/"
        #     print(mainLink)
            # yield response.follow(mainLink, callback=self.parse_subCategory)

        # mainCategories_div = response.css('div.main-section')

        # mainCategories_links = mainCategories_div.css('div.a::attr(href)').getall()

        # for mainLink in mainCategories_links:
        #     mainLink = encyclopediaDefaultUrl + mainLink + "/"
        #     print(mainLink)
            # yield response.follow(mainLink, callback=self.parse_subCategory)