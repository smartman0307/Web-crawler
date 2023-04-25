import scrapy


class TrellixSpider(scrapy.Spider):
    name = "trellix"
    allowed_domains = ["trellix.com"]
    start_urls = ["https://www.trellix.com/en-us/index.html"]

    def parse(self, response):
        result = response.encode("utf-8")

        div_selector = result.xpath(
            "//main[@class='main newsroom']/div[@class='wrap-section padding-medium medium container']/div[@class='padding-medium medium container blog card-container']/div[@class='row']/div[@class='col-md-9 col-sm-12']"
        )
        with open("1.txt", "w") as f:
            f.write(result)

        for story_selector in div_selector.xpath(
            ".//div[@class='row listing']/div[@class='col-md-4']"
        ):
            yield {
                "title": story_selector.xpath(".//h3/a/text()").get(),
                "url": response.urljoin(story_selector.xpath(".//h3/a/@href").get()),
                "date": story_selector.xpath(".//p/text()[following-sibling::a]").get(),
                "summary": story_selector.xpath(".//p[2]/text()").get(),
            }
