from pathlib import Path

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

encyclopediaDefaultUrl = "https://www.encyclopedia.com"
categories = []

class DiscoverySpider(scrapy.Spider):
    name = "encyclopedia"
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
            
            # print(link)
            if "references" not in link and "articles" not in link and "daily" not in link: 
                yield response.follow(link, callback=self.parse_subCategory)

    def parse_subCategory(self, response):
        subCategories_div = response.css('ul.no-bullet-list')

        subCategories_links = subCategories_div.css('a::attr(href)').getall()

        for subLink in subCategories_links:
            subLink = encyclopediaDefaultUrl + subLink + "/"
            yield response.follow(subLink, callback=self.parse_subSubCategory)

    def parse_subSubCategory(self,response):
        subCategories_div = response.css('ul.no-bullet-list')

        subCategories_links = subCategories_div.css('a::attr(href)').getall()

        for subLink in subCategories_links:
            subLink = encyclopediaDefaultUrl + subLink + "/"
            yield response.follow(subLink, callback=self.parse_contentUrl)

    def parse_contentUrl(self,response):
        contentUrl_div = response.css('ul.no-bullet-list')

        contentUrl_links = contentUrl_div.css('a::attr(href)').getall()

        for contentUrl in contentUrl_links:
            contentUrl = encyclopediaDefaultUrl + contentUrl + "/"

            # if "earth-and-environment" in subLink:
            print(contentUrl)

            #store content url into txt file
            with open('discoveredUrl.txt', 'a') as f:
                f.write(contentUrl + "\n")

    
