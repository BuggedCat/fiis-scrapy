from datetime import datetime

import scrapy

from src.database.database import fetch_documentos_ids, start_mongo_client
from src.utils import write_to_s3

BASE_URL = "https://fnet.bmfbovespa.com.br/fnet/publico/downloadDocumento?id={}"


class FnetDocumentsSpider(scrapy.Spider):
    name = "fnet_rendimentos"
    allowed_domains = ["fnet.bmfbovespa.com.br"]
    today = datetime.today().strftime("%Y-%m-%d")

    custom_settings = {
        "LOG_FILE": f"logs/{name}/log.txt",
        "LOG_LEVEL": "INFO",
        "ITEM_PIPELINES": {
            "src.pipelines.S3UploadPipeline": 300,
        },
    }

    def __init__(self, *args, **kwargs):
        super(FnetDocumentsSpider, self).__init__(*args, **kwargs)
        self.mongo_client = None

    def start_requests(self):
        try:
            self.mongo_client = start_mongo_client()

            for mongo_document in fetch_documentos_ids(self.mongo_client):
                fnet_document_id = mongo_document["id"]
                url = BASE_URL.format(fnet_document_id)
                yield scrapy.Request(
                    url, meta={"document_id": fnet_document_id}, callback=self.parse_pages
                )
        except Exception as e:
            self.logger.error(f"Error fetching document IDs: {e}")
        finally:
            if self.mongo_client:
                self.mongo_client.close()

    def parse_pages(self, response):
        try:
            yield {
                "xml_data": response.text,
                "document_id": response.meta["document_id"],
            }
        except Exception as e:
            self.logger.error(f"Error in parse_pages: {e}")
