from typing import Any

import boto3
from scrapy.crawler import Crawler
from scrapy.spiders import Spider

from src.utils import start_s3_client, write_to_s3


class S3UploadPipeline:
    def __init__(
        self,
        environment: str,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_endpoint: str | None = None,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_endpoint = aws_endpoint
        self.environment = environment
        self.s3_client = None

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        return cls(
            environment=crawler.settings.get("ENVIRONMENT", "dev"),
            aws_access_key_id=crawler.settings.get("AWS_ACCESS_KEY_ID", None),
            aws_secret_access_key=crawler.settings.get("AWS_SECRET_ACCESS_KEY", None),
            aws_endpoint=crawler.settings.get("AWS_ENDPOINT_URL", None),
        )

    def open_spider(self, spider: Spider):
        spider.logger.debug("Creating S3 session")
        self.s3_client = start_s3_client(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            endpoint_url=self.aws_endpoint,
            environment=self.environment,
        )

    def close_spider(self, spider: Spider):
        if self.s3_client:
            spider.logger.debug("Closing S3 session")
            self.s3_client.close()

    def process_item(self, item: dict[str, Any], spider: Spider):
        if "xml_data" in item and "document_id" in item:
            s3_object_key = f"{spider.name}/{item['document_id']}.xml"
            bucket_name = "rendafiis-bronze"
            data = item["xml_data"].encode("utf-8")

            try:
                self.s3_client.put_object(
                    Body=data,
                    Bucket=bucket_name,
                    Key=s3_object_key,
                )
                spider.logger.debug(f"Uploaded to S3: {s3_object_key}")
            except Exception as e:
                spider.logger.error(f"Error uploading to S3: {e}")

        return item
