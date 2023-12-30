## My Scrapy Project

### Overview
This project is built using Scrapy, a powerful web crawling and scraping framework for Python. The aim is to extract specific data from target websites.

### Requirements
- Python 3.6+
- Scrapy 2.0+
- Poetry 1.7.1+

### Installation
Install Scrapy, and the required libraries:

```bash
poetry install
```

### Usage
To run a spider, navigate to the project's root directory and use:

```bash
scrapy crawl spider_name
```

### Project Structure
- `src/` - Root code directory.
    - `spiders/` - Directory containing all the spiders.
    - `items.py` - Defines the data structure for scraped data.
    - `middlewares.py` - Custom middlewares.
    - `pipelines.py` - Pipelines to process the scraped data.
    - `settings.py` - Settings for the Scrapy project.

### Deploy
Generate the requirements.txt needed to deploy on ScrapeOps Cloud

```bash
poetry lock --no-update
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

Add the project to a github repository

Spin up a AWS EC2 Server and configure SSH key

Follow the instructions on [ScrapeOps docs](https://scrapeops.io/docs/servers-scheduling/aws-integration/) to deploy on AWS EC2 Server

