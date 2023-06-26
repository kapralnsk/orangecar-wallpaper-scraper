import logging
import logging.config
from time import sleep

from api_client import APIClient
from the_box_to_drop import TheBoxToDrop
import settings

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger()


def run():
    logger.info("starting a run")
    box_to_drop = TheBoxToDrop()
    client = APIClient(teams=settings.TEAMS)

    existing_images = box_to_drop.get_existing_images()
    available_imagesets = client.get_available_imagesets()
    available_imagesets_map = dict(zip([item["data"]["name"] for item in available_imagesets], available_imagesets))
    new_images = set(available_imagesets_map.keys()).difference(existing_images)
    logger.info(f"got {len(new_images)} new images")

    for image_name in new_images:
        client.grab_image(image_name, storage_path=settings.STORAGE_PATH, sizes=settings.IMAGESET_SIZES)
        box_to_drop.upload_image(image_name)
        # behaving ourselves
        logging.debug(f"waiting for {settings.TIMEOUT}")
        sleep(settings.TIMEOUT)
    logger.info("successfully uploaded all new images")


run()
