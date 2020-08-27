# -*- coding: utf-8 -*-
import scrapy
import logging

#  Practice
# 'https://worldometers.info/world-population/population-by-country/'
# a tag => 'https://www.worldometers.info/world-population/mozambique-population/'
# get `name` of the country and `year`, `population`


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['worldometers.info']  # 필요없는 extra slash를 지워줘야 한다.
    start_urls = [
        'https://worldometers.info/world-population/population-by-country/']

    # 첫 번째 웹사이트에서 crawling
    def parse(self, response):

        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()

            # absolute_url = f*https://www.worldometers.info{link}
            # absolute_url = response.urljoin(link)

            # give meta information
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})

    # 각각의 a tag의 값을 긁어와서 crawling
    # Example URL https://www.worldometers.info/world-population/mozambique-population/
    def parse_country(self, response):
        # retreive meta information
        name = response.request.meta['country_name']
        # table이 2개 이상일 때 잡는 방법.   (//table)[index]
        rows = response.xpath(
            '(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()  # table row는 1부터 시작함.
            population = row.xpath('.//td[2]/strong/text()').get()
            yield {
                'name': name,
                'year': year,
                'population': population
            }
