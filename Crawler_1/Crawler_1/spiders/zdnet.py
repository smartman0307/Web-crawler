import scrapy


class ZdnetSpider(scrapy.Spider):
    name = "zdnet"
    allowed_domains = ["zdnet.com"]
    start_urls = ["http://zdnet.com/topic/ransomware"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.page_num = 1

    def parse(self, response):
        div_selector = response.xpath(
            "//div[contains(@data-component, 'lazyloadImages')]"
        )

        for article_selector in div_selector.xpath(".//article"):
            yield {
                "title": article_selector.xpath(
                    ".//div/a/div[contains(@class, 'content content-thumb')]/h3/text()"
                ).get(),
                "url": response.urljoin(article_selector.xpath(".//div/a/@href").get()),
                "date": article_selector.xpath(".//div/div/p/span[1]/@data-date").get(),
            }

        self.page_num += 1
        next_page = f"https://www.zdnet.com/topic/ransomware/{self.page_num}/"

        if next_page and self.page_num <= 20:
            yield scrapy.Request(response.urljoin(next_page), self.parse)
