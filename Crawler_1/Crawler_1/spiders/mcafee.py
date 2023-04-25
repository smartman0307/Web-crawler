import scrapy


class McafeeSpider(scrapy.Spider):
    name = "mcafee"
    allowed_domains = ["mcafee.com"]
    start_urls = ["https://www.mcafee.com/blogs/security-news"]

    def parse(self, response):
        div_selector = response.xpath(
            "//div[@class = 'container-fluid main-cont sticky-top p-0 new-category-template']/article/div[@class = 'container-fluid p-0']/div[@class = 'row center-cont']/div[2]/div[@class = 'card-deck cyber flex-container homepage-topics new-category-grid']"
        )

        for article_selector in div_selector.xpath(".//div[@class = 'card']"):
            yield {
                "title": article_selector.xpath(
                    ".//div[@class = 'card-body']/h5/a/text()"
                ).get(),
                "url": response.urljoin(
                    article_selector.xpath(
                        ".//div[@class = 'card-body']/h5/a/@href"
                    ).get()
                ),
                "date": article_selector.xpath(
                    ".//div[@class = 'card-footer']/p/small[1]/text()"
                ).get(),
            }

        next_page = response.xpath(
            "//div[@class = 'container-fluid main-cont sticky-top p-0 new-category-template']/article/div[@class = 'container-fluid p-0']/div[@class = 'row center-cont']/div[2]/div[@class = 'wrap-section cat-pagination']/div/div/ul/li[last()]/a/@href"
        )

        if next_page:
            yield scrapy.Request(response.urljoin(next_page.get()), self.parse)
