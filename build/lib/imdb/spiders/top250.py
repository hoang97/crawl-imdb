import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Top250Spider(CrawlSpider):
    name = 'top250'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/chart/top']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//tbody[@class = 'lister-list']/tr/td[2]/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        
        trend = response.xpath("//span[contains(@class, 'popularity')]/text()").get()
        if trend:
            trend = trend.replace(',','')
            value = int(trend)
            negative = response.xpath("//span[contains(@class, 'popularityDown')]")
            if negative: value *= -1
        else:
            value = None

        rank = response.xpath('(//span[@class = "subText"])[3]/text()[1]').get()
        if rank:
            rank = rank.strip('(').strip()

        yield {
            'name': response.xpath('normalize-space(//div[@class = "title_wrapper"]/h1/text()[1])').get(),
            'star': response.xpath('//span[@itemprop="ratingValue"]/text()').get(),
            'tags': response.xpath('//div[@class = "subtext"]/span[3]/preceding-sibling::a//text()').getall(),
            'rank': rank,
            'trend': value
        }
