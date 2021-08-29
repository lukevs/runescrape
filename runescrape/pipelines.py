from pathlib import Path

from pydantic import BaseModel

from runescrape.settings import IMAGES_STORE
from runescrape.items import RunescrapeItem


EXPORT_PATH = "items.jsonl"


class RunscrapeExportItem(BaseModel):
    title: str
    icon_filepath: str


class RunescrapeExportPipeline:
    def open_spider(self, spider):
        self.output_file = open(EXPORT_PATH, "w+")

    def close_spider(self, spider):
        self.output_file.close()

    def process_item(self, item: RunescrapeItem, spider):
        icon_filepath = Path(IMAGES_STORE) / item.get_icon_path()
        export_item = RunscrapeExportItem(title=item.title, icon_filepath=str(icon_filepath))

        self.output_file.write(export_item.json() + "\n")
