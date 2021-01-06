import scrapy
import os

# Links = //div[contains(@class,"rowItem")]/a/@href
# año = //li[@class="specs-item" and ./strong/text()="Año"]/span/text()
# kms = //li[@class="specs-item" and ./strong/text()="Kilómetros"]/span/text()
# Transmisión = //li[@class="specs-item" and ./strong/text()="Transmisión"]/span/text()
# precio = //fieldset[contains(@class,"item-price")]//span[@class="price-tag-fraction"]/text()
# Title = //h1[contains(@class,"item-title__primary")]/text()

# delete csv file
os.remove('carros.csv')


class SpiderTuCarro(scrapy.Spider):
    name = 'tucarro'
    start_urls = ['https://carros.tucarro.com.co/mazda/3/antioquia/desde-2015/',
                  'https://carros.tucarro.com.co/mazda/mazda-3/antioquia/desde-2015/']
    custom_settings = {
        'FEED_URI': 'carros.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'USER_AGENT': 'Cudeiro'
    }

    def parse(self, response):
        links_carros = response.xpath(
            '//div[contains(@class,"rowItem")]/a/@href').getall()
        for link in links_carros:
            yield response.follow(link, callback=self.parse_link)

    def parse_link(self, response):
        title = response.xpath(
            '//h1[contains(@class,"item-title__primary")]/text()').get().strip()
        price = response.xpath(
            '//fieldset[contains(@class,"item-price")]//span[@class="price-tag-fraction"]/text()').get()
        year = response.xpath(
            '//li[@class="specs-item" and ./strong/text()="Año"]/span/text()').get()
        kms = response.xpath(
            '//li[@class="specs-item" and ./strong/text()="Kilómetros"]/span/text()').get()
        transmission = response.xpath(
            '//li[@class="specs-item" and ./strong/text()="Transmisión"]/span/text()').get()

        yield {
            'nombre': title,
            'precio': price,
            'año': year,
            'kms': kms,
            'transmision': transmission,
            'url': response.url
        }
