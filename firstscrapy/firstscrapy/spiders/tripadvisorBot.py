# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
#from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from firstscrapy.items import RestaurantItem, ReviewItem


class TripadvisorbotSpider(scrapy.Spider):
    name = 'tripadvisorBot'
    allowed_domains = ['tripadvisor.de']
    start_urls = [
        "https://www.tripadvisor.de/RestaurantSearch?Action=PAGE&geo=187323&ajax=1&itags=10591&sortOrder=popularity&o=a" + str(i * 30) + "&availSearchEnabled=false"
        for i in range(2)
    ]

    def parse(self, response):
        for href in response.xpath('//div[@class="title"]/a/@href'):
            url = response.urljoin(href.extract())
            yield response.follow(url, callback=self.parse_reviews)


    def parse_reviews(self, response):
        yield RestaurantItem(
            name=response.xpath('//*[@id="HEADING"]/text()').extract_first(),
            url=response.url
        )

        for sel in response.xpath('//div[@class="wrap"]'):
            yield ReviewItem(
                title=sel.xpath('.//span[@class="noQuotes"]/text()').extract_first(),
                date=sel.xpath('.//span[contains(@class, "ratingDate")]/@title').extract_first(),
                text=sel.xpath('.//p[@class="partial_entry"]/text()').extract_first()
            )

'''
    def parse(self,response):
        urls = response.xpath('//h3[@class="title"]/a/@href').extract()
        for url in urls:
            rest_url = response.urljoin(url)
            request = scrapy.Request(rest_url, callback = self.parse_restaurant)
            yield request

    rules = (Rule (LinkExtractor(allow=(response.xpath('//h3[@class="title"]/a/@href'))), callback ="parse_restaurant"))

    def parse_restaurant(self, response):
        name = response.xpath('//h1[@id="HEADING"]/text()').extract()
        rating = response.xpath('//span[@class="ui_bubble_rating"]/@alt').extract()
        review_title = response.xpath('//span[@class="noQuotes"]/text()').extract()
        review = response.xpath('//p[@class="partial_entry"]').extract().extract()

        rest_reviews = {
            'name' : name,
            'rating' : rating,
            'review_title' : review_title,
            'review' : review
            }
        yield rest_reviews





    def parse(self, response):
        for href in response.xpath('//div[@class="title"]/a/@href').extract():
            url = "https://www.tripadvisor.com{}".format(href)

            yield scrapy.Request(url, callback = self.parse_review)

    def parse_review(self, response):
        for sel in response.xpath('//div[@class="wrap"]'):
            item = FirstscrapyItem()
            item['title'] = sel.xpath('//span[@class="noQuotes"]/text()').extract()
            item['date'] = sel.xpath('//span[@class="ratingDate"]/text()').extract()
            item['text'] = sel.xpath('//p[@class="partial_entry"]').extract()
            yield item



    def parse(self, response):
        urls = []
        for href in response.xpath('//div[@class="title"]/a/@href').extract():
            url = "https://www.tripadvisor.com{}".format(href)
            if url not in urls:
                urls.append(url)

                yield scrapy.Request(url, callback = self.parse_reviews)



    def parse_reviews(self, response):
        item = FirstscrapyItem()

        title = response.xpath('//h1[@class="heading_title"]/text()').extract()
        review_title = response.xpath('//div[@class="quote"]/a/span[@class="noQuotes"]/text()').extract()
        review = response.xpath('//div[@class="entry"]/p/text()').extract()

        item['title'] = title
        item['review_title'] = review_title
        item['review'] = review
        yield item




        for items in zip(title,review_title,review):
            reviews_rest = {
            'name' : item[0],
            'title' : item[1],
            'text' : item[2]
            }

            yield reviews_rest

    def parse(self, response):
        #extracting the content unsing css selectors
        restName = response.css('.property_title::text').extract()
        rating = response.css('.ui_bubble_rating::attr(alt)').extract()
        links = response.xpath('//div[@class="title"]/a/@href').extract()
        #priceRange = response.css('.price::text').extract()
        #cuisine = response.css('.cuisine::text').extract()


        #create a table with extracted content
        for item in zip(restName,rating,links):
            #create a dictionary to store the scraped infos
            restaurantsBerlin = {
            'name' : item[0],
            'rating' : item[1],
            'link' : item[2],
            }

            #return infos to sracpy and store it
            yield restaurantsBerlin
'''
