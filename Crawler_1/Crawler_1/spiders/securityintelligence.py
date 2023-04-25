import scrapy


class SecurityintelligenceSpider(scrapy.Spider):
    name = "securityintelligence"
    allowed_domains = ["securityintelligence.com"]
    start_urls = [
        "https://securityintelligence.com/timeline/state-local-government-cyberattacks"
    ]

    def parse(self, response):
        location_1 = ""
        location_2 = ""
        location_3 = ""

        div_selector = response.xpath(
            "//main[contains(@class, 'main')]/div[contains(@class, 'swiper-containers')]/div[contains(@class, 'swiper-wrapper')]/div[contains(@class, 'swiper-slide swiper-slide-timeline')]"
        )

        for subdiv_selector in div_selector.xpath(
            ".//div[contains(@class, 'container')]"
        ):
            for article_selector in subdiv_selector.xpath(
                ".//div[contains(@class, 'row')]/div[contains(@class, 'timeline__content')]/div[contains(@class, 'content__article')]"
            ):
                article_id = article_selector.xpath(
                    ".//div[contains(@class, 'box')]/@data-id"
                ).get()

                title = article_selector.xpath(
                    ".//div[contains(@class, 'box')]/p/text()"
                ).get()

                if title is not None:
                    title = title.strip()

                date = article_selector.xpath(
                    ".//div[contains(@class, 'box')]/div[contains(@class, 'box__date')]/time/text()"
                ).get()

                if date is not None:
                    date = date.replace(" ", "").replace("\n", "")

                location = article_selector.xpath(
                    ".//div[contains(@class, 'box')]/div[contains(@class, 'box__date')]/text()"
                )[1].get()

                if location is not None:
                    location_1 = location.strip()
                    location_2 = location_1.replace("–", "")
                    location_3 = location_2.strip()

                item = {
                    "title": title,
                    "url": response.urljoin(
                        f"https://securityintelligence.com/timeline/state-local-government-cyberattacks/{article_id}"
                    ),
                    "date": date,
                    "location": location_3,
                }

                yield scrapy.FormRequest(
                    url=f"https://securityintelligence.com/wp-content/themes/sapphire/app/jsons/incidents.php?quantity=1&id={article_id}&__amp_source_origin=https%3A%2F%2Fsecurityintelligence.com",
                    method="GET",
                    callback=self.parse_article,
                    meta={"item": item},
                )

    def parse_article(self, response):
        with open("1.txt", "w") as f:
            f.write(response.text)
        item = response.meta["item"]
        item["attack_type"] = response.xpath(
            "//div[@class='container']/div[@class='row']/div[@class='timeline__content']/div[@class='article']/amp-list[@id='list']/div[4]/div/div[@class='row article__stats']/div[@class='article__atk-type'][1]/div[@class='article__stats--subtitle']/text()"
        ).get()
        item["attack_target"] = response.xpath(
            "//main[@class='main']/div[@class='swiper-containers swiper-container-initialized swiper-container-horizontal']/div[@class='swiper-wrapper']/div[@class='swiper-slide swiper-slide-details swiper-slide-visible swiper-slide-active swiper-slide-previous']/div[@class='container']/div[@class='row']/div[@class='timeline__content']/div[@class='article']/amp-list[@id='list']/div[4]/div/div[@class='row article__stats']/div[@class='article__atk-type'][2]/div[@class='article__stats--subtitle']/text()"
        ).get()
        yield item
