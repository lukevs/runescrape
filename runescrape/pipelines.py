import csv
from pathlib import Path

from runescrape.settings import IMAGES_STORE
from runescrape.items import RunescrapeItem


EXPORT_FILEPATH = "items.csv"
EXPORT_FIELDNAMES = ["title", "item_type", "icon_filepath", "full_image_filepath"]


class RunescrapeExportPipeline:
    def open_spider(self, spider):
        self.csv_file = open(EXPORT_FILEPATH, "w", newline="")
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=EXPORT_FIELDNAMES)
        self.csv_writer.writeheader()

    def close_spider(self, spider):
        self.csv_file.close()

    def process_item(self, item: RunescrapeItem, spider):
        icon_filepath = Path(IMAGES_STORE) / item.get_icon_path()
        full_image_filepath = Path(IMAGES_STORE) / item.get_full_image_path()

        self.csv_writer.writerow(dict(
            title=item.title,
            item_type=item.item_type.value,
            icon_filepath=icon_filepath,
            full_image_filepath=full_image_filepath,
        ))
