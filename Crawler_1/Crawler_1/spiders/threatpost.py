import scrapy


class ThreatpostSpider(scrapy.Spider):
    name = "threatpost"
    allowed_domains = ["threatpost.com"]
    start_urls = ["http://threatpost.com/"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.page_num = 1

    def parse(self, response):
        div_selector = response.xpath("//div[contains(@id, 'latest_news_container')]")

        for article_selector in div_selector.xpath(".//article"):
            yield {
                "title": article_selector.xpath(
                    ".//div/div[contains(@class, 'o-col-8@md o-col-4@lg c-card__col-title')]/h2/a/text()"
                ).get(),
                "url": response.urljoin(
                    article_selector.xpath(
                        ".//div/div[contains(@class, 'o-col-8@md o-col-4@lg c-card__col-title')]/h2/a/@href"
                    ).get()
                ),
                "date": article_selector.xpath(
                    ".//div/div[contains(@class, 'o-col-8@md o-col-4@lg c-card__col-title')]/div[contains(@class, 'c-card__info')]/div[contains(@class, 'c-card__time')]/time/text()"
                ).get(),
            }

        data = {
            "action": "loadmore",
            "query": "%7B%22ignore_sticky_posts%22%3Atrue%2C%22posts_per_page%22%3A5%2C%22post_type%22%3A%5B%22post%22%2C%22tp_microsites%22%5D%2C%22post__not_in%22%3A%5B%22180492%22%2C%22180490%22%2C%22180487%22%2C%22180481%22%5D%2C%22error%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A0%2C%22post_parent%22%3A%22%22%2C%22subpost%22%3A%22%22%2C%22subpost_id%22%3A%22%22%2C%22attachment%22%3A%22%22%2C%22attachment_id%22%3A0%2C%22name%22%3A%22%22%2C%22pagename%22%3A%22%22%2C%22page_id%22%3A0%2C%22second%22%3A%22%22%2C%22minute%22%3A%22%22%2C%22hour%22%3A%22%22%2C%22day%22%3A0%2C%22monthnum%22%3A0%2C%22year%22%3A0%2C%22w%22%3A0%2C%22category_name%22%3A%22%22%2C%22tag%22%3A%22%22%2C%22cat%22%3A%22%22%2C%22tag_id%22%3A%22%22%2C%22author%22%3A%22%22%2C%22author_name%22%3A%22%22%2C%22feed%22%3A%22%22%2C%22tb%22%3A%22%22%2C%22paged%22%3A0%2C%22meta_key%22%3A%22%22%2C%22meta_value%22%3A%22%22%2C%22preview%22%3A%22%22%2C%22s%22%3A%22%22%2C%22sentence%22%3A%22%22%2C%22title%22%3A%22%22%2C%22fields%22%3A%22%22%2C%22menu_order%22%3A%22%22%2C%22embed%22%3A%22%22%2C%22category__in%22%3A%5B%5D%2C%22category__not_in%22%3A%5B%5D%2C%22category__and%22%3A%5B%5D%2C%22post__in%22%3A%5B%5D%2C%22post_name__in%22%3A%5B%5D%2C%22tag__in%22%3A%5B%5D%2C%22tag__not_in%22%3A%5B%5D%2C%22tag__and%22%3A%5B%5D%2C%22tag_slug__in%22%3A%5B%5D%2C%22tag_slug__and%22%3A%5B%5D%2C%22post_parent__in%22%3A%5B%5D%2C%22post_parent__not_in%22%3A%5B%5D%2C%22author__in%22%3A%5B%5D%2C%22author__not_in%22%3A%5B%5D%2C%22search_columns%22%3A%5B%5D%2C%22suppress_filters%22%3Afalse%2C%22cache_results%22%3Atrue%2C%22update_post_term_cache%22%3Atrue%2C%22update_menu_item_cache%22%3Afalse%2C%22lazy_load_term_meta%22%3Atrue%2C%22update_post_meta_cache%22%3Atrue%2C%22nopaging%22%3Afalse%2C%22comments_per_page%22%3A%2250%22%2C%22no_found_rows%22%3Afalse%2C%22order%22%3A%22DESC%22%7D",
            "page": str(self.page_num),
        }

        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
        }

        yield scrapy.FormRequest(
            url="https://threatpost.com/wp-admin/admin-ajax.php",
            method="POST",
            formdata=data,
            headers=headers,
            callback=self.parse_ajax,
        )

    def parse_ajax(self, response):
        for article_selector in response.xpath("//article"):
            yield {
                "title": article_selector.xpath(
                    ".//div/div[contains(@class, 'o-col-8@md o-col-4@lg c-card__col-title')]/h2/a/text()"
                ).get(),
                "url": response.urljoin(
                    article_selector.xpath(
                        ".//div/div[contains(@class, 'o-col-8@md o-col-4@lg c-card__col-title')]/h2/a/@href"
                    ).get()
                ),
                "date": article_selector.xpath(
                    ".//div/div[contains(@class, 'o-col-8@md o-col-4@lg c-card__col-title')]/div[contains(@class, 'c-card__info')]/div[contains(@class, 'c-card__time')]/time/text()"
                ).get(),
            }

        self.page_num += 1

        data = {
            "action": "loadmore",
            "query": "%7B%22ignore_sticky_posts%22%3Atrue%2C%22posts_per_page%22%3A5%2C%22post_type%22%3A%5B%22post%22%2C%22tp_microsites%22%5D%2C%22post__not_in%22%3A%5B%22180492%22%2C%22180490%22%2C%22180487%22%2C%22180481%22%5D%2C%22error%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A0%2C%22post_parent%22%3A%22%22%2C%22subpost%22%3A%22%22%2C%22subpost_id%22%3A%22%22%2C%22attachment%22%3A%22%22%2C%22attachment_id%22%3A0%2C%22name%22%3A%22%22%2C%22pagename%22%3A%22%22%2C%22page_id%22%3A0%2C%22second%22%3A%22%22%2C%22minute%22%3A%22%22%2C%22hour%22%3A%22%22%2C%22day%22%3A0%2C%22monthnum%22%3A0%2C%22year%22%3A0%2C%22w%22%3A0%2C%22category_name%22%3A%22%22%2C%22tag%22%3A%22%22%2C%22cat%22%3A%22%22%2C%22tag_id%22%3A%22%22%2C%22author%22%3A%22%22%2C%22author_name%22%3A%22%22%2C%22feed%22%3A%22%22%2C%22tb%22%3A%22%22%2C%22paged%22%3A0%2C%22meta_key%22%3A%22%22%2C%22meta_value%22%3A%22%22%2C%22preview%22%3A%22%22%2C%22s%22%3A%22%22%2C%22sentence%22%3A%22%22%2C%22title%22%3A%22%22%2C%22fields%22%3A%22%22%2C%22menu_order%22%3A%22%22%2C%22embed%22%3A%22%22%2C%22category__in%22%3A%5B%5D%2C%22category__not_in%22%3A%5B%5D%2C%22category__and%22%3A%5B%5D%2C%22post__in%22%3A%5B%5D%2C%22post_name__in%22%3A%5B%5D%2C%22tag__in%22%3A%5B%5D%2C%22tag__not_in%22%3A%5B%5D%2C%22tag__and%22%3A%5B%5D%2C%22tag_slug__in%22%3A%5B%5D%2C%22tag_slug__and%22%3A%5B%5D%2C%22post_parent__in%22%3A%5B%5D%2C%22post_parent__not_in%22%3A%5B%5D%2C%22author__in%22%3A%5B%5D%2C%22author__not_in%22%3A%5B%5D%2C%22search_columns%22%3A%5B%5D%2C%22suppress_filters%22%3Afalse%2C%22cache_results%22%3Atrue%2C%22update_post_term_cache%22%3Atrue%2C%22update_menu_item_cache%22%3Afalse%2C%22lazy_load_term_meta%22%3Atrue%2C%22update_post_meta_cache%22%3Atrue%2C%22nopaging%22%3Afalse%2C%22comments_per_page%22%3A%2250%22%2C%22no_found_rows%22%3Afalse%2C%22order%22%3A%22DESC%22%7D",
            "page": str(self.page_num),
        }

        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
        }

        if self.page_num <= 30:
            yield scrapy.FormRequest(
                url="https://threatpost.com/wp-admin/admin-ajax.php",
                method="POST",
                formdata=data,
                headers=headers,
                callback=self.parse_ajax,
            )
