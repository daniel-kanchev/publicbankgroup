import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from publicbankgroup.items import Article


class publicbankgroupSpider(scrapy.Spider):
    name = 'publicbankgroup'
    start_urls = ['https://www.publicbankgroup.com/News-Announcements/Press-Release']

    def parse(self, response):
        articles = response.xpath('//div[@id="accordion"]/div[@class="panel panel-default"]')
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article.xpath('.//div[@class="col-lg-8 col-md-8 col-sm-8 col-xs-5 header-title"]/text()').get()
            if title:
                title = title.strip()

            date = article.xpath('.//div[@class="col-lg-3 col-md-3 col-sm-3 col-xs-5 text-right header-title-date"]/text()').get()
            if date:
                date = " ".join(date.split())

            content = article.xpath('.//div[@class="news-content"]//text()').getall()
            content = [text.strip() for text in content if text.strip() and '{' not in text]
            content = " ".join(content).strip()

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()



