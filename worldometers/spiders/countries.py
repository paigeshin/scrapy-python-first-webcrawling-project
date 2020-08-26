# -*- coding: utf-8 -*-
import scrapy


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info/']
    start_urls = [
        'https://worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        title = response.xpath("//h1/text").get()
        countries = response.xpath("//td/a/text()").getall()

        yield {
            'title': title,
            'countries': countries
        }