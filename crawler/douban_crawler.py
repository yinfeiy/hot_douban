from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
import simplejson as json
from items import DoubanMovieItem

class DoubanCrawler(CrawlSpider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]
    #allowed_domains = ["fling.seas.upenn.edu/"]
    #start_urls = ["https://fling.seas.upenn.edu/~yinfeiy/"]

    rules = (
        Rule(
            SgmlLinkExtractor(
                allow = (r'http://movie\.douban\.com/top250\?start=\d+&filter=&type=',))),
        Rule(
            SgmlLinkExtractor(
                allow = (r'http://movie\.douban\.com/subject/\d+', )),
            callback = 'parse_page', follow = True)
        )

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        for i,url in enumerate(self.start_urls):
            yield Request(url,cookies={'over18':'1'}, callback=self.parse_page, headers=headers)

    def parse_page(self, response) :
        sel = Selector(response)
        item = DoubanMovieItem()
        item['name'] = sel.xpath('//h1/span[@property="v:itemreviewed"]/text()').extract()
        item['desc'] = sel.xpath('//div/span[@property="v:summary"]/text()').extract()
        item['url'] = response.url
        return item
