# -*- coding: utf-8 -*-
import scrapy


class JobsZhipinSpider(scrapy.Spider):
    name = 'jobs_zhipin'
    #allowed_domains = ['https://www.zhipin.com/']
    start_urls = ['https://www.zhipin.com/']

    def parse(self, response):
        for label in response.css('div.home-box div.common-tab-box.job-tab-box ul'):
            for job in label.xpath('./li'):
                job_detail_url = response.urljoin(job.xpath('./div[@class="sub-li"]/a/@href').extract_first())
                request = scrapy.Request(job_detail_url, callback=self.job_detail)
                yield request
    
    def job_detail(self, response):
        yield {
            'job_name': response.css('div.info-primary div.name h1::text').extract_first(),
            'company_name': response.css('div.info-company h3.name a::text').extract_first(),
            'company_image_url': response.css('div.info-company div.company-logo a img::attr(src)').extract_first(),
            'city': response.xpath('//div[@class="info-primary"]/p/text()[1]').extract_first(),
            'jobyear': response.xpath('//div[@class="info-primary"]/p/text()[2]').extract_first(),
            'education': response.xpath('//div[@class="info-primary"]/p/text()[3]').extract_first(),
            'financing': response.xpath('//div[@class="info-company"]/p/text()[1]').extract_first(),
            'num_of_people': response.xpath('//div[@class="info-company"]/p/text()[2]').extract_first(),
            'field': response.xpath('//div[@class="info-company"]/p/a/text()').extract_first(),
            'pay': response.css('div.info-primary div.name span::text').extract_first()
        }
