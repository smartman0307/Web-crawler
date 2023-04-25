import scrapy


class NakedsecuritySophosSpider(scrapy.Spider):
    name = "nakedsecurity_sophos"
    allowed_domains = ["nakedsecurity.sophos.com"]
    start_urls = ["http://nakedsecurity.sophos.com/"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.page_num = 1

    def parse(self, response):
        div_selector = response.xpath(
            "//div[contains(@id, 'page')]/section[contains(@class, 'cards-panel')]/div/div/div"
        )
        print(div_selector.get())
        # print(response.text)
        for article_selector in div_selector.xpath(".//article"):
            yield {
                "title": article_selector.xpath(
                    ".//div[contains(@class, 'card-content')]/h3/a/text()"
                ).get(),
                "url": response.urljoin(
                    article_selector.xpath(
                        ".//div[contains(@class, 'card-content')]/h3/a/@href"
                    ).get()
                ),
                "date": article_selector.xpath(
                    ".//div[contains(@class, 'card-content')]/div/div/span[contains(@class, 'month')]/text()"
                ).get()
                + ", "
                + article_selector.xpath(
                    ".//div[contains(@class, 'card-content')]/div/div/span[contains(@class, 'day')]/text()"
                ).get(),
            }

        self.page_num += 1
        next_page = response.xpath(
            "//div[contains(@id, 'page')]/section[contains(@class, 'load-more')]/div/a/@href"
        )

        if next_page and self.page_num <= 20:
            yield scrapy.Request(response.urljoin(next_page.get()), self.parse)
