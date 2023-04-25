import scrapy
import json


class RecordedfutureSpider(scrapy.Spider):
    name = "recordedfuture"
    allowed_domains = ["recordedfuture.com"]
    start_urls = [
        "https://cms.recordedfuture.com/api/resources?populate[0]=cardImage&populate[1]=cardImage.desktop&populate[2]=cardImage.mobile&populate[3]=cardImage.tablet&populate[4]=countryTags&populate[5]=downloadResource&populate[6]=downloadResource.type&populate[7]=eventResource&populate[8]=eventResource.type&populate[9]=industryTags&populate[10]=integrationResource&populate[11]=integrationResource.tags&populate[12]=newsAndResearchResource&populate[13]=newsAndResearchResource.researchPreviewImage&populate[14]=newsAndResearchResource.researchPreviewImageDesktop&populate[15]=newsAndResearchResource.researchPreviewImageMobile&populate[16]=newsAndResearchResource.researchPreviewImageTablet&populate[17]=newsAndResearchResource.type&populate[18]=page&populate[19]=productTags&populate[20]=threatTags&populate[21]=topicTags&filters[$or][0][downloadResource][type][key][$in][0]=blog&filters[$or][1][eventResource][type][key][$in]=&filters[$or][2][newsAndResearchResource][type][key][$in][0]=blog&filters[$and][4][topicTags][name][$in][0]=Cybercrime&pagination%5BpageSize%5D=12&pagination%5Bpage%5D=1&sort%5B0%5D=newsAndResearchResource.date%3Adesc"
    ]

    def parse(self, response):
        with open("1.json", "w") as f:
            f.write(response.text)

        parsed_data = json.loads(response.text)
