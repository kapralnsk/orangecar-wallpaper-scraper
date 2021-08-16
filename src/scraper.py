import shutil
import logging

import requests
from bs4 import BeautifulSoup

from settings import URL, STORAGE_PATH

logger = logging.getLogger()


class Scraper:
    def __init__(self, width: str = "1920", height: str = "1200", delay_secs: int = 5):
        self.url = URL
        self.width = width
        self.height = height
        self.storage_path = STORAGE_PATH
        self.delay_secs = delay_secs
        self.image_links = {}

    def scrape_available_images(self) -> set[str]:
        resp = requests.get(self.url)
        soup = BeautifulSoup(resp.content)
        image_elements = soup(
            'a',
            title='Download',
            attrs={'data-resolution-width': self.width, 'data-resolution-height': self.height},
        )
        self.image_links = dict(map(
            lambda el: (el['href'].split('/')[-1], el['href']),
            image_elements,
        ))
        return set(self.image_links)

    def grab_image(self, filename: str) -> None:
        resp = requests.get(self.image_links[filename], stream=True)
        with open(f'{self.storage_path}{filename}', 'wb') as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)
        logger.info(f'{filename} downloaded')