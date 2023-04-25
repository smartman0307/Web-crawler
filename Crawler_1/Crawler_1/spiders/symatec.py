import scrapy
import requests
import json
from bs4 import BeautifulSoup


class SymatecSpider(scrapy.Spider):
    name = "symatec"
    allowed_domains = ["symantec-enterprise-blogs.security.com"]
    start_urls = ["https://symantec-enterprise-blogs.security.com/blogs/ransomware"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.date = ""

    def parse(self, response):
        div_selector = response.xpath(
            "//app-root/div[@class='page-wrapper']/app-blog-home/div[@class='blog-id--16990 page-search sidebar-first']/div[@class='page-container']/main[@class='main']/div[@class='result-items']"
        )

        for article_selector in div_selector.xpath(".//app-blog-teaser"):
            yield {
                "title": article_selector.xpath(
                    ".//div[@class='blog-teaser']/div[@class='blog-teaser__inner']/article[@class='blog-teaser__feature']/div[@class='blog-teaser__content']/div[@class='blog-teaser__content-inner']/header/h1/text()"
                ).get(),
                "url": response.urljoin(
                    article_selector.xpath(
                        ".//div[@class='blog-teaser']/div[@class='blog-teaser__inner']/article[@class='blog-teaser__feature']/div[@class='blog-teaser__content']/div[@class='blog-teaser__content-inner']/a/@href"
                    ).get()
                ),
                "date": article_selector.xpath(
                    ".//div[@class='blog-teaser']/div[@class='blog-teaser__inner']/article[@class='blog-teaser__feature']/div[@class='blog-teaser__content']/div[@class='blog-teaser__content-inner']/header/div[@class='meta']/span/time/text()"
                ).get(),
                "summary": article_selector.xpath(
                    ".//div[@class='blog-teaser']/div[@class='blog-teaser__inner']/article[@class='blog-teaser__feature']/div[@class='blog-teaser__content']/div[@class='blog-teaser__content-inner']/header/h2/text()"
                ).get(),
            }

        api_res = requests.get(
            f"https://symantec-enterprise-blogs.security.com/blogs/api/v1/blogs/search?aid=IOTVy1&blog=16990&sort=&sortDirection=&rows=5&page=5&sid=0ea78691-3b54-45e2-bd5f-b45ee9a86226"
        )

        parsed_data = json.loads(api_res.text)

        date_include_str = parsed_data["results"][0]["paragraphs"][0]["content"]

        soup = BeautifulSoup(date_include_str, "html.parser")
        strong_tag = soup.find("strong")

        if strong_tag:
            self.date = strong_tag.text.replace("UPDATE ", "").replace(" ", " ")
        else:
            print("error!")

        yield {
            "title": parsed_data["results"][0]["title"],
            "url": parsed_data["results"][0]["postUrl"],
            "date": self.date,
            "summary": parsed_data["results"][0]["subtitle"],
        }

        yield {
            "title": parsed_data["results"][1]["title"],
            "url": parsed_data["results"][1]["postUrl"],
            "date": parsed_data["facets"][0]["items"][6]["label"],
            "summary": parsed_data["results"][1]["subtitle"],
        }
