clean_pycache:
	@find . -type f -name "*.pyc" -exec rm -f {} +
	@find . -type d -name "__pycache__" -exec rm -rf {} +

requirements:
	@poetry lock --no-update
	@poetry export -f requirements.txt --output requirements.txt --without-hashes

fnet_documentos:
	scrapy crawl fnet_documentos

fnet_documentos_full:
	scrapy crawl fnet_documentos -a full="True"

fnet_rendimentos:
	scrapy crawl fnet_rendimentos
