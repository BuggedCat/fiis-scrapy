import json
import math
from datetime import datetime
from urllib.parse import urlencode

import scrapy
from dateutil.relativedelta import relativedelta
from scrapy.http import TextResponse

BASE_URL = "https://fnet.bmfbovespa.com.br/fnet/publico/pesquisarGerenciadorDocumentosDados"
ITENS_POR_PAGINA = 200
TIPO_FUNDO = 1
ID_CATEGORIA_DOCUMENTO = 14


class FnetDocumentsSpider(scrapy.Spider):
    name = "fnet_documentos"
    allowed_domains = ["fnet.bmfbovespa.com.br"]

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    today = datetime.today().strftime("%Y-%m-%d")

    custom_settings = {
        "LOG_LEVEL": "INFO",
        "FEEDS": {
            "s3://scrapy-fiis-bronze/%(name)s/reference_date=%(today)s/data.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 0,
            },
        },
    }

    def build_url(self, inicio: int = 0) -> str:
        """Constrói a URL com os parâmetros de requisição.

        Args:
            inicio (int): O índice de início para a paginação de resultados.

        Returns:
            str: A URL construída com os parâmetros de requisição.
        """
        request_params = self.get_request_params(inicio)
        encoded_params = urlencode(request_params)
        url = f"{BASE_URL}?{encoded_params}"
        self.logger.debug(f"Construindo URL: {url}")
        return url

    def get_request_params(self, inicio: int) -> dict:
        """Retorna os parâmetros de requisição para a URL.

        Args:
            inicio (int): O índice de início para a paginação de resultados.

        Returns:
            dict: Um dicionário com os parâmetros de requisição.
        """
        request_params: dict[str, str | int] = {
            "d": 0,
            "s": inicio,
            "l": ITENS_POR_PAGINA,
            "tipoFundo": TIPO_FUNDO,
            "idCategoriaDocumento": ID_CATEGORIA_DOCUMENTO,
        }

        full = bool(getattr(self, "full", False))
        if not full:
            start_date = datetime.today() - relativedelta(months=1)
            request_params["dataInicial"] = start_date.strftime("%d/%m/%Y")

        return request_params

    def start_requests(self):
        """Inicia as requisições pelo Scrapy."""
        url = self.build_url()
        self.logger.info(f"Iniciando requisições com a URL: {url}")
        yield scrapy.Request(url, callback=self.parse_initial)

    def parse_initial(self, response: TextResponse):
        """Processa a resposta inicial e programa as requisições das páginas seguintes.

        Args:
            response (TextResponse): A resposta recebida do Scrapy.
        """
        json_response = json.loads(response.text)
        total_records = json_response.get("recordsTotal", 0)
        total_pages = math.ceil(total_records / ITENS_POR_PAGINA)
        self.logger.info(f"Total de registros: {total_records}, Total de páginas: {total_pages}")

        for page in range(total_pages):
            start = page * ITENS_POR_PAGINA
            url = self.build_url(start)
            self.logger.debug(f"Solicitando página {page} na URL: {url}")
            yield scrapy.Request(
                url,
                callback=self.parse_pages,
                dont_filter=True,
            )

    def parse_pages(self, response: TextResponse):
        """Processa os dados de cada página.

        Args:
            response (TextResponse): A resposta recebida do Scrapy.
        """
        data = json.loads(response.text)["data"]
        self.logger.debug(f"Recebendo dados de {response.url}, Número de itens: {len(data)}")
        yield from data
