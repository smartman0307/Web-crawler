import scrapy


class MicrosoftSpider(scrapy.Spider):
    name = "microsoft"
    allowed_domains = ["microsoft.com"]
    start_urls = ["https://www.microsoft.com/en-us/security/blog/"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.page_num = 1

    def parse(self, response):
        div_selector = response.xpath(
            "//div[@id='page']/section[@class='wrap']/main[@id='mainContent']/div[@id='posts-river-container']"
        )

        for article_selector in div_selector.xpath(
            ".//div[@class = 'article-card-wrap']"
        ):
            yield {
                "title": article_selector.xpath(".//section/h3/a/text()").get(),
                "url": response.urljoin(
                    article_selector.xpath(".//section/h3/a/@href").get()
                ),
                "date": article_selector.xpath(".//section/span/time/@datetime").get(),
                "summary": article_selector.xpath(
                    ".//section/div[@class = 'c-paragraph']/a/text()"
                )
                .get()
                .strip(),
            }

        self.page_num += 1

        next_page = response.xpath(
            "//div[@id='page']/section[@class='wrap']/main[@id='mainContent']/ul[@class = 'm-pagination']/li[last()]/a/@href"
        )

        if next_page and self.page_num <= 10:
            yield scrapy.Request(response.urljoin(next_page.get()), self.parse)
