import scrapy


class RunscrapeSpider(scrapy.Spider):
    name = 'runescrape'
    allowed_domains = ['oldschool.runescape.wiki/w/Head_slot_table']
    start_urls = ['https://oldschool.runescape.wiki/w/Head_slot_table']

    def parse(self, response):
        pass
