import scrapy


class VmwareSpider(scrapy.Spider):
    name = "vmware"
    allowed_domains = ["blogs.vmware.com"]
    start_urls = ["https://blogs.vmware.com/security/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page_num = 1

    def parse(self, response):
        div_selector = response.xpath(
            "//div[@class='wrap']/div[@class='content']/main/section[@class='background-off-white pt-5']/div[@class='container']/div[@class='row']"
        )

        for article_selector in div_selector.xpath(
            ".//div[@class='col-12 col-md-6 col-lg-4 stacked-posts mb-4 category-curl']"
        ):
            yield {
                "title": article_selector.xpath(
                    ".//article/div[@class='content-wrap']/div[@class='content-inner']/h2/a/text()"
                ).get(),
                "url": response.urljoin(
                    article_selector.xpath(
                        ".//article/div[@class='content-wrap']/div[@class='content-inner']/h2/a/@href"
                    ).get()
                ),
                "date": article_selector.xpath(
                    ".//article/div[@class='content-wrap']/div[@class='content-inner']/div[@class='entry-meta']/time/text()"
                ).get(),
            }

        self.page_num += 1
        next_page = response.xpath(
            "//div[@class='wrap']/div[@class='content']/main/section[@class='background-off-white pt-5']/div[@class='container']/div[@class='row']/div[@class='col-12']/nav/div/a[@class='next page-numbers']/@href"
        )

        if next_page and self.page_num <= 5:
            yield scrapy.Request(response.urljoin(next_page.get()), self.parse)
