import scrapy


class DuoSpider(scrapy.Spider):
    name = "duo"
    allowed_domains = ["duo.com"]
    start_urls = ["https://duo.com/blog"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page_num = 1

    def parse(self, response):
        div_selector = response.xpath("//div[@class='page']/div[last()]")

        items = []

        for article_selector in div_selector.xpath(".//article"):
            item = {
                "title": article_selector.xpath(
                    ".//div[@class='article__content-wrap']/h3/a/text()"
                ).get(),
                "url": response.urljoin(
                    article_selector.xpath(
                        ".//div[@class='article__content-wrap']/h3/a/@href"
                    ).get()
                ),
                "date": article_selector.xpath(
                    ".//div[@class='article__content-wrap']/h6/time/text()"
                ).get(),
                "summary": article_selector.xpath(
                    ".//div[@class='article__content-wrap']/p/text()"
                ).get(),
            }
            items.append(item)

        self.page_num += 1

        next_page = response.xpath(
            "//div[@class='page']/div[last()]/ul/li[@class='paginate__item paginate__next']/a/@href"
        )

        if next_page and self.page_num <= 10:
            yield scrapy.Request(response.urljoin(next_page.get()), self.parse)

        for item in items:
            if (
                "Cyber" in item["title"]
                or "Malware" in item["title"]
                or "Ransomware" in item["title"]
                or "Attack" in item["title"]
                or "Hack" in item["title"]
                or "Breach" in item["title"]
            ):
                print(item["title"])
                yield item

            else:
                continue
