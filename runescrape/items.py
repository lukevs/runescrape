from enum import Enum
from typing import List

from pydantic import BaseModel, validator


class RunscrapeItemType(Enum):
    HEAD = "head"
    NECK = "neck"
    WEAPON = "weapon"
    BODY = "body"
    FEET = "feet"
    RING = "ring"
    HANDS = "hands"


class RunescrapeItem(BaseModel):
    title: str
    item_type: RunscrapeItemType
    icon_source_url: str
    full_image_source_url: str

    # for scrapy - image_urls are fetched and loaded into images field
    image_urls: List[str] = []
    images: List[dict] = []

    @validator("image_urls", pre=True, always=True)
    def populate_image_urls(cls, v, values):
        return [
            values["icon_source_url"],
            values["full_image_source_url"],
        ]

    def get_icon_path(self):
        if len(self.images) < 2:
            raise RuntimeError("Images is not yet populated")

        return self.images[0]["path"]

    def get_full_image_path(self):
        if len(self.images) < 2:
            raise RuntimeError("Images is not yet populated")

        return self.images[1]["path"]
