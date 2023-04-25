import scrapy


class DarkreadingSpider(scrapy.Spider):
    name = "darkreading"
    allowed_domains = ["darkreading.com"]
    start_urls = ["http://www.darkreading.com/attacks-breaches"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.page_num = 1

    def parse(self, response):
        div_selector = response.xpath(
            "//div[contains(@class, 'infinite-scroll-component ')]"
        )
        for article_selector in div_selector.xpath(
            ".//div[contains(@class, 'topic-content-article')]"
        ):
            yield {
                "title": article_selector.xpath(
                    ".//div[contains(@class, 'row')]/div/a/div[contains(@class, 'article-top')]/div[contains(@class, 'article-right')]/span/text()"
                ).get(),
                "url": response.urljoin(
                    article_selector.xpath(
                        ".//div[contains(@class, 'row')]/div/a/@href"
                    ).get()
                ),
                "date": article_selector.xpath(
                    ".//div[contains(@class, 'row')]/div/a/div[contains(@class, 'article-bottom')]/div[contains(@class, 'd-flex justify-content-between align-items-center')]/div[contains(@class, 'arcile-date')]/text()"
                ).get(),
            }

        self.page_num += 1
        next_page = f"https://www.darkreading.com/attacks-breaches?page={self.page_num}"

        if next_page and self.page_num <= 10:
            yield scrapy.Request(response.urljoin(next_page), self.parse)
