import scrapy

from runescrape.items import RunescrapeItem, RunscrapeItemType


WIKI_DOMAIN = "oldschool.runescape.wiki"

ITEM_TYPE_META = "item_type"
TABLE_URLS_BY_ITEM_TYPE = {
    RunscrapeItemType.HEAD: "https://oldschool.runescape.wiki/w/Head_slot_table",
    RunscrapeItemType.NECK: "https://oldschool.runescape.wiki/w/Neck_slot_table",
    RunscrapeItemType.WEAPON: "https://oldschool.runescape.wiki/w/Weapon_slot_table",
    RunscrapeItemType.BODY: "https://oldschool.runescape.wiki/w/Body_slot_table",
    RunscrapeItemType.LEGS: "https://oldschool.runescape.wiki/w/Legs_slot_table",
    RunscrapeItemType.FEET: "https://oldschool.runescape.wiki/w/Feet_slot_table",
    RunscrapeItemType.RING: "https://oldschool.runescape.wiki/w/Ring_slot_table",
    "https://oldschool.runescape.wiki/w/Worn_Equipment#Hands_slot "
}


class RunscrapeSpider(scrapy.Spider):
    name = "runescrape"
    allowed_domains = [WIKI_DOMAIN]
    start_urls = [f"https://oldschool.runescape.wiki/w/Head_slot_table"]

    def start_requests(self):
        return [
            scrapy.Request(url=table_url, meta={ITEM_TYPE_META: item_type})
            for item_type, table_url in TABLE_URLS_BY_ITEM_TYPE.items()
        ]

    def parse(self, response):
        article_links = response.css(".wikitable tr td a")
        yield from response.follow_all(
            article_links,
            callback=self.parse_article,
            meta={ITEM_TYPE_META: response.meta.get(ITEM_TYPE_META)}
        )

    def parse_article(self, response):
        title = response.css("#firstHeading::text").get()
        item_type = response.meta.get(ITEM_TYPE_META)
        icon_source_path = response.css(".infobox-image img")[-1].attrib["src"]
        icon_source_url = f"https://{WIKI_DOMAIN}{icon_source_path}"

        yield RunescrapeItem(
            title=title,
            item_type=item_type,
            icon_source_url=icon_source_url,
        )
