import scrapy
from scrapy import Selector


class CyberarkSpider(scrapy.Spider):
    name = "cyberark"
    allowed_domains = ["cyberark.com"]
    start_urls = ["https://www.cyberark.com/resources/threat-research"]

    def parse(self, response):
        selector = Selector(text=response.text)

        div_selector = selector.xpath(
            "//div[@class='main clearfix']/div[@class='hubs-container']/div[@class='page-width']/div[@class='page-aligner']/section[@class='level-two']/div[@id='collection-items']/ul[@class='clearfix collection-items-container']"
        )

        with open("1.txt", "w", encoding="utf-8") as f:
            f.write(response.text)

        for article_selector in div_selector.xpath(".//li[@data-id]"):
            yield {
                "title": article_selector.xpath(
                    ".//div[@class='description']/h3/text()"
                ).get(),
                "url": response.urljoin(article_selector.xpath(".//a[1]/@href").get()),
                "date": article_selector.xpath(
                    ".//div[@class='description']/div[@class='friendly-timestamp']/abbr/@title"
                ).get(),
            }
