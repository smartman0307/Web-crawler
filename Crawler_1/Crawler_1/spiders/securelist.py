import scrapy


class SecurelistSpider(scrapy.Spider):
    name = "securelist"
    allowed_domains = ["securelist.com"]
    start_urls = ["https://securelist.com/threat-category/cybersecurity"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.page_num = 1

    def parse(self, response):
        div_selector = response.xpath(
            "//div[contains(@class, 'c-page')]/section[contains(@class, 'c-block c-block--spacing-b-small@md c-block--divider-internal')]/div/div/div/div[contains(@class, 'o-row o-row--small-gutters js-post-items')]"
        )

        for article_selector in div_selector.xpath(
            ".//div[contains(@class, 'o-col-12 c-card__dividers c-card__dividers--hide-first@xs js-post-item js-post-item-has-divider')]"
        ):
            item = {
                "title": article_selector.xpath(
                    ".//article/div[contains(@class, 'c-card__body')]/header/h3/a/text()"
                ).get(),
                "url": response.urljoin(
                    article_selector.xpath(".//article/a/@href").get()
                ),
                "summary": article_selector.xpath(".//article/div/div/p/text()").get(),
            }
            yield scrapy.Request(
                item["url"], callback=self.parse_article, meta={"item": item}
            )

        next_page = response.xpath(
            "//div[contains(@class, 'c-page')]/section[contains(@class, 'c-block c-block--spacing-b-small@md c-block--divider-internal')]/div/div/div/div[contains(@class, 'c-block__footer u-justify-center')]/a/@href"
        ).get()

        self.page_num += 1

        if next_page and self.page_num <= 10:
            yield scrapy.Request(response.urljoin(next_page), self.parse)

    def parse_article(self, response):
        item = response.meta["item"]
        item["date"] = response.xpath(
            "//div[contains(@class, 'o-container-fluid')]/article/header/div[contains(@class, 'c-article__info')]/p[2]/time/text()"
        ).get()
        yield item
