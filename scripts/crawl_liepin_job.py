import scrapy

class JobSpider(scrapy.Spider):
    name = "companies"

    start_urls = ['https://www.liepin.com/zhaopin/?d_sfrom=search_fp_nvbar&init=1']

    def parse(self, response):
        for job in response.css('div.sojob-result ul.sojob-list li'):
            yield {
                    'job_title': job.xpath('.//h3/a/text()').extract_first().strip(),
                    'salary': job.xpath('.//div/p[@class="condition clearfix"]/span[1]/text()').extract_first(),
                    'location': job.xpath('.//div/p[@class="condition clearfix"]/a/text()').extract_first(),
                    'edu_requirement': job.xpath('.//div/p[@class="condition clearfix"]/span[2]/text()').extract_first(),
                    'exp_requirement': job.xpath('.//div/p[@class="condition clearfix"]/span[3]/text()').extract_first()
                    }



