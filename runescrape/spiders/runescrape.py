import scrapy
from pydantic import BaseModel


class RunscapeItem(BaseModel):
    title: str
    icon_source_url: str


class RunscrapeSpider(scrapy.Spider):
    name = 'runescrape'
    allowed_domains = ['oldschool.runescape.wiki']
    start_urls = ['https://oldschool.runescape.wiki/w/Head_slot_table']

    def parse(self, response):
        article_links = response.css(".wikitable tr td a")
        yield from response.follow_all(article_links, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css("#firstHeading::text").get()
        icon_source_url = response.css(".infobox-image img")[-1].attrib["src"]

        yield RunscapeItem(
            title=title,
            icon_source_url=icon_source_url,
        )
