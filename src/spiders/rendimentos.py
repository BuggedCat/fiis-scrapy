from datetime import datetime

import boto3
import scrapy
from scrapy.http import TextResponse

from src.database.database import fetch_documentos_ids, start_mongo_client
from src.utils import start_s3_client, write_to_s3

BASE_URL = "https://fnet.bmfbovespa.com.br/fnet/publico/downloadDocumento?id={}"


class FnetDocumentsSpider(scrapy.Spider):
    name = "fnet_rendimentos"
    allowed_domains = ["fnet.bmfbovespa.com.br"]
    today = datetime.today().strftime("%Y-%m-%d")

    custom_settings = {
        "LOG_LEVEL": "INFO",
    }

    def __init__(self, *args, **kwargs):
        super(FnetDocumentsSpider, self).__init__(*args, **kwargs)
        self.s3_client = start_s3_client()
        self.mongo_client = start_mongo_client()

    def start_requests(self):
        try:
            for mongo_document in fetch_documentos_ids(self.mongo_client):
                fnet_document_id = mongo_document["id"]
                url = BASE_URL.format(fnet_document_id)
                yield scrapy.Request(
                    url, meta={"documento_id": fnet_document_id}, callback=self.parse_pages
                )
        except Exception as e:
            self.logger.error(f"Error fetching document IDs: {e}")
        finally:
            self.mongo_client.close()

    def parse_pages(self, response: TextResponse):
        try:
            xml_data = response.text.encode("utf-8")
            document_id = response.meta["documento_id"]
            with open(f"data/{self.name}/{document_id}.xml", "wb") as f:
                f.write(xml_data)
            # s3_object_key = f"{self.name}/{document_id}.xml"
            # s3_bronze_bucket = "rendafiis-bronze"
            # write_to_s3(
            #     self.s3_client,
            #     xml_data,
            #     s3_bronze_bucket,
            #     s3_object_key,
            # )
        except Exception as e:
            self.logger.error(f"Error in parse_pages: {e}")
