from pathlib import Path

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

encyclopediaDefaultUrl = "https://www.encyclopedia.com"

class DiscoverySpider(scrapy.Spider):
    name = "epCategories"
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

            if "references" not in link and "articles" not in link and "daily" not in link: 
                yield response.follow(link, callback=self.parse_subCategory)

            # if "references" in link:
            #     print(link)
                # yield response.follow(link, callback=self.parse_subReference)

    def parse_subCategory(self, response):
        subCategories_div = response.css('ul.no-bullet-list')

        subCategories_links = subCategories_div.css('a::attr(href)').getall()

        for subLink in subCategories_links:
            subLink = encyclopediaDefaultUrl + subLink + "/"
            yield response.follow(subLink, callback=self.parse_subSubCategory)

    # def parse_subReference(self, response):
    #     subReferences_div = response.css('ul.no-bullet-list')

    #     subReferences_links = subReferences_div.css('a::attr(href)').getall()

    #     for subReferenceLink in subReferences_links:
    #         subReferenceLink = encyclopediaDefaultUrl + subReferenceLink + "/"
    #         yield response.follow(subReferenceLink, callback=self.parse_subSubReference)

    def parse_subSubCategory(self,response):
        subSubCategories_div = response.css('ul.no-bullet-list')

        subSubCategories_links = subSubCategories_div.css('a::attr(href)').getall()

        for subSubLink in subSubCategories_links:
            subSubLink = encyclopediaDefaultUrl + subSubLink + "/"
            # print(subSubLink)
            yield response.follow(subSubLink, callback=self.parse_subCategory_pages, cb_kwargs={'subSubLink': subSubLink})

    def parse_subCategory_pages(self,response, subSubLink):
        # Extract page numbers from the HTML snippet
        hasPagination = response.css('ul.pager__items.js-pager__items').getall() is not None

        if hasPagination:
            pagination_ul = response.css('ul.pager__items.js-pager__items')
            page_numbers = pagination_ul.css('li.pager__item a::attr(href)').getall()
            for page_number in page_numbers:
                modified_url = subSubLink + page_number
                # print(modified_url)
                yield response.follow(modified_url, callback=self.parse_contentUrl)

    def parse_contentUrl(self,response):
        contentUrl_div = response.css('ul.no-bullet-list')

        contentUrl_links = contentUrl_div.css('a::attr(href)').getall()

        for contentUrl in contentUrl_links:
            contentUrl = encyclopediaDefaultUrl + contentUrl + "/"

            #store content url into txt file
            with open('discoveredUrl.txt', 'a') as f:
                f.write(contentUrl + "\n")

    
