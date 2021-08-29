from enum import Enum
from typing import List

from pydantic import BaseModel, validator


class RunscrapeItemType(Enum):
    HEAD = "head"
    NECK = "neck"
    WEAPON = "weapon"
    BODY = "body"
    LEGS = "legs"
    FEET = "feet"
    RING = "ring"


class RunescrapeItem(BaseModel):
    title: str
    item_type: RunscrapeItemType
    icon_source_url: str

    # for scrapy - image_urls are fetched and loaded into images field
    image_urls: List[str] = []
    images: List[dict] = []

    @validator("image_urls", pre=True, always=True)
    def populate_image_urls(cls, v, values):
        return [values["icon_source_url"]]

    def get_icon_path(self):
        if len(self.images) == 0:
            raise RuntimeError("Images is not yet populated")

        return self.images[0]["path"]
