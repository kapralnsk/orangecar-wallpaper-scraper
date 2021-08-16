
import logging
import logging.config
from time import sleep

from scraper import Scraper
from the_box_to_drop import TheBoxToDrop
from settings import TIMEOUT, LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger()


def run():
    logger.info('starting a run')
    box_to_drop = TheBoxToDrop()
    scraper = Scraper()

    existing_images = box_to_drop.get_existing_images()
    available_images = scraper.scrape_available_images()
    new_images = available_images - existing_images
    # at the moment, they have two '1920x1200.jpg' images, which we rename during upload
    # (see TheBoxToDrop.upload_image for details),
    # because of that, this file will always be marked as new, so in turn we manually discard it
    new_images.discard('1920x1200.jpg')
    logger.info(f'got {len(new_images)} new images')

    for image_name in new_images:
        scraper.grab_image(image_name)
        box_to_drop.upload_image(image_name)
        # behaving ourselves
        logging.debug(f'waiting for {TIMEOUT}')
        sleep(TIMEOUT)
    logger.info('successfully uploaded all new images')

run()
