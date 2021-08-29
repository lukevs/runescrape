import scrapy

from runescrape.items import RunescrapeItem


WIKI_DOMAIN = "oldschool.runescape.wiki"


class RunscrapeSpider(scrapy.Spider):
    name = "runescrape"
    allowed_domains = [WIKI_DOMAIN]
    start_urls = [f"https://oldschool.runescape.wiki/w/Head_slot_table"]

    def parse(self, response):
        article_links = response.css(".wikitable tr td a")
        yield from response.follow_all(article_links, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css("#firstHeading::text").get()
        icon_source_path = response.css(".infobox-image img")[-1].attrib["src"]
        icon_source_url = f"https://{WIKI_DOMAIN}{icon_source_path}"

        yield RunescrapeItem(
            title=title,
            icon_source_url=icon_source_url,
        )
