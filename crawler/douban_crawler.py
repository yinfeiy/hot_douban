from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import simplejson as json

class DoubanCrawler(CrawlSpider):
    name = "douban"
    #allowed_domains = ["movie.douban.com"]
    #start_urls = ["http://movie.douban.com/top250"]
    allowed_domains = ["fling.seas.upenn.edu/"]
    start_urls = ["http://movie.douban.com/~yinfeiy/"]

    rules = (
        Rule(
            SgmlLinkExtractor(
                allow = (r'http://movie\.douban\.com/top250\?start=\d+&filter=&type=',))),
        Rule(
            SgmlLinkExtractor(
                allow = (r'http://movie\.douban\.com/subject/\d+', )),
            callback = 'parse_page', follow = True)
        )

    def parse_page(self, response) :
        sel = Selector(response)
        item = dict()
        item['name'] = sel.xpath('//h1/span[@property="v:itemreviewed"]/text()').extract()
        item['description'] = sel.xpath('//div/span[@property="v:summary"]/text()').extract()
        item['url'] = response.url
        print json.dumps(item)
        return item

if __name__ == '__main__':
    DoubanCrawler()
