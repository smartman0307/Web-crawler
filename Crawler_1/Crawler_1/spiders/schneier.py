import scrapy


class SchneierSpider(scrapy.Spider):
    name = "schneier"
    allowed_domains = ["schneier.com"]
    start_urls = ["http://schneier.com/"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.cnt = 0

    def parse(self, response):
        div_selector = response.xpath("//div[contains(@id, 'content')]")
        scraped_articles = set()

        for article_selector in div_selector.xpath(".//article"):
            tags = article_selector.xpath(
                ".//p[contains(@class, 'entry-tags')]/span/a/text()"
            ).getall()
            if any(
                tag in tags
                for tag in ["cyber", "breach", "hack", "malware", "ransomware"]
            ):
                article_url = response.urljoin(
                    article_selector.xpath(".//div/h2/a/@href").get()
                )
                if article_url not in scraped_articles:
                    scraped_articles.add(article_url)
                    yield {
                        "title": article_selector.xpath(".//div/h2/a/text()").get(),
                        "url": response.urljoin(
                            article_selector.xpath(".//div/h2/a/@href").get()
                        ),
                        "date": article_selector.xpath(
                            ".//div/p[contains(@class, 'posted')]/a/text()"
                        ).get(),
                    }

        next_page = response.xpath("//div[contains(@id, 'content')]/div/a/@href")

        if next_page and self.cnt <= 100:
            self.cnt += 1
            yield scrapy.Request(response.urljoin(next_page.get()), self.parse)
