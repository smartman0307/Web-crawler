import scrapy


class CheckpointSpider(scrapy.Spider):
    name = "checkpoint"
    allowed_domains = ["research.checkpoint.com"]
    start_urls = ["https://research.checkpoint.com/category/threat-research/"]

    def parse(self, response):
        div_selector = response.xpath(
            "//section[@class='blog-post-wrapper blog-post-wrapper- section-padding background-blue-- ']/div[@class='container container-wide']/div[@class='flex-row align-items-start']/div[@class='flex-8 font-white']/div[@class='flex-row align-items-start col-margin-wrap post-pagination data-responce list-posts']"
        )

        with open("1.txt", "w", encoding="utf-8") as f:
            f.write(response.text)

        for article_selector in div_selector.xpath(".//div[@class='flex-12']"):
            yield {
                "title": article_selector.xpath(
                    ".//div[@class='box col-margin relative border-dotted']/div[@class='display-flex desktop-view-socialshare']/h3/a/text()"
                ).get(),
                "url": response.urljoin(
                    article_selector.xpath(
                        ".//div[@class='box col-margin relative border-dotted']/div[@class='display-flex desktop-view-socialshare']/h3/a/@href"
                    ).get()
                ),
                "date": article_selector.xpath(
                    ".//div[@class='box col-margin relative border-dotted']/div[@class='blog-wrap-top mob-view-socialshare']/div[@class='date small-font']/text()"
                ).extract_first(),
            }
