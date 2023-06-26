import shutil
import logging
from typing import Iterable, Literal

import requests

from settings import DOWNLOADS_ENDPNT_URL

from enums import ImagesetTypes, ImagesetSizes

logger = logging.getLogger()


class DataPage:
    def __init__(self, resp_data):
        self.root = self.get_page_ref(resp_data["root"]["$ref"])
        self.data = resp_data["page"]
        self.pagination = self.get_pagination()

    def get_page_ref(self, ref_path: str) -> str:
        return ref_path.split("/")[-1]  # type: ignore

    def get_dict_by_ref(self, full_ref: dict) -> dict:
        ref = self.get_page_ref(full_ref["$ref"])
        return self.data[ref]

    def get_pagination(self) -> dict:
        page_root = self.data[self.root]
        second_root = self.get_dict_by_ref(page_root["children"][0])
        return self.get_dict_by_ref(second_root["models"]["pagination"])

    def get_documents(self) -> Iterable[dict]:
        return [self.get_dict_by_ref(item) for item in self.pagination["items"]]

    def get_imagesets(
        self, documents: Iterable[dict], imageset_type: Literal[ImagesetTypes.DESKTOP] = ImagesetTypes.DESKTOP
    ) -> Iterable[dict]:
        return [self.get_dict_by_ref(document[imageset_type]) for document in documents]


class APIClient:
    downloads_endpoint_url = DOWNLOADS_ENDPNT_URL
    image_links = {}

    def __init__(self, teams: Iterable[str]):
        self.teams = teams

    def get_available_imagesets(self) -> Iterable[dict]:
        resp = requests.get(self.downloads_endpoint_url)
        data_page = DataPage(resp.json())
        documents = data_page.get_documents()
        if self.teams:
            documents = self.filter_documents(documents)
        return data_page.get_imagesets(documents)

    def filter_documents(self, documents: Iterable[dict]) -> Iterable[dict]:
        return filter(
            lambda item: item["data"]["dlTeam"]["selectionValues"]["key"] in self.teams,
            documents,
        )

    def grab_image(self, imageset: dict, storage_path: str, sizes: Iterable[ImagesetSizes]):
        for size in sizes:
            resp = requests.get(imageset[size]["links"]["site"]["href"], stream=True)
            with open(f"{storage_path}{imageset['data']['name']}", "wb") as f:
                resp.raw.decode_content = True
                shutil.copyfileobj(resp.raw, f)  # type: ignore
            logger.info(f"{imageset['data']['name']} of size {size} downloaded")


__all__ = ["APIClient"]
