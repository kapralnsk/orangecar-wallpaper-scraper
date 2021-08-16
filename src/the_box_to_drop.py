import logging

from dropbox import Dropbox, exceptions
from dropbox.files import UploadError
from settings import DROPBOX_TOKEN, STORAGE_PATH


logger = logging.getLogger()


class TheBoxToDrop:
    def __init__(self):
        self.box_to_drop = Dropbox(DROPBOX_TOKEN)

    def get_existing_images(self) -> set[str]:
        return set(
            map(lambda file: file.name, self.box_to_drop.files_list_folder('').entries)
        )

    def upload_image(self, filename: str) -> None:
        with open(f'{STORAGE_PATH}{filename}', 'rb') as f:
            try:
                self.box_to_drop.files_upload(f.read(), f'/{filename}')
            except exceptions.ApiError as e:
                if not type(e.error) is UploadError:
                    raise e
                # They like to upload files w/ same name (essentially rewriting old ones)
                # also they treat "filename.jpg" and "filename.JPG" as different files,
                # however Dropbox does not. We add prefix to such file, so it uploads successfully
                logger.debug(f'got UploadError while uploading {filename}, trying to rename')
                self.box_to_drop.files_upload(f.read(), f'/extension-double_{filename}')
        logger.info(f'{filename} uploaded')
            
                
