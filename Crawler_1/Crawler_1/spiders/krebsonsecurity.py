import scrapy


class KrebsSpider(scrapy.Spider):
    name = "krebsonsecurity"
    allowed_domains = ["krebsonsecurity.com"]
    start_urls = ["https://krebsonsecurity.com/category/data-breaches/"]

    def parse(self, response, **kwargs):
        div_selector = response.xpath("//div[contains(@id,'content')]")

        for article_selector in div_selector.xpath(".//article"):
            yield {
                "title": article_selector.xpath(
                    ".//h2[contains(@class,'entry-title')]/a/text()"
                ).get(),
                "url": article_selector.xpath(
                    ".//h2[contains(@class,'entry-title')]/a/@href"
                ).get(),
                "date": article_selector.xpath(
                    ".//div[contains(@class,'btm-wrap')]//div[contains(@class,'adt')]/span/text()"
                ).get(),
                # "company": post.xpath(".//p/b[contains(text(),'COMPANY:')]/following-sibling::text()[1]").get().strip(),
                # "type": post.css("div.entry-content p strong ~ span::text").get(),
            }

        next_page = response.xpath(
            "//div[contains(@class, 'nav-previous alignleft')]/a/@href"
        )

        if next_page:
            yield scrapy.Request(response.urljoin(next_page.get()), self.parse)
