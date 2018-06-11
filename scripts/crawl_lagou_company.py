import scrapy

class CompanySpider(scrapy.Spider):
    name = "companies"

    start_urls = ['https://www.lagou.com/gongsi/']

    def parse(self, response):
        for company in response.css('div#company_list ul li'):
            yield {
                    'logo_url': company.xpath('.//div/p/a/img/@src').extract_first(),
                    'name': company.xpath('.//div/p[@class="company-name wordCut"]/a/text()').extract_first(),
                    'description': company.xpath('.//div/p[@class="indus-stage wordCut"]/text()').extract_first(),
                    'slogan': company.xpath('.//div/p[@class="advantage wordCut"]/text()').extract_first()
                    }



