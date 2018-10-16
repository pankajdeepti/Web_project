
from scrapy import Spider, Request
from esabna.items import EsabnaItem
import re

class EsabnaSpider(Spider):
    name = 'esabna_spider'
    allowed_urls = ['https://www.esabna.com/']
    start_urls = ['https://www.esabna.com/us/en/products/index.cfm?fuseaction=home.category&categoryId=8']

    def parse(self, response):
        allcatagories_tab = response.xpath('//ul[@class="lev3 show-for-medium-up"]//a/@href')[1:].extract()   #***********Good
        
        products_tab_urls = ['https://www.esabna.com/{}'.format(i) for i in allcatagories_tab]

        

        for url in products_tab_urls:
            yield Request(url=url, callback=self.parse_product_page)
 
    def parse_product_page(self, response):

        try:
            num_products = response.xpath('//div[@class="pagination-centered"]//p/text()').extract_first().strip()

            if num_products % 50 != 0:
                num_pages = (int(re.search('Showing 1 - \d+ of (\d+)', num_products).group(1)) // 50) + 1
            else:
                num_pages = int(re.search('Showing 1 - \d+ of (\d+)', num_products).group(1))
        except:
            num_pages = 1


        pages_urls = [response.url + '&pageno=' + str(x) for x in range(1, num_pages+3)]

        for url in pages_urls:
            yield Request(url=url, callback=self.parse_product_top)

    def parse_product_top(self, response):

        products_urls = response.xpath('//div[@class="row marg_top"]//a/@href').extract()

        new_product_urls=['https://www.esabna.com'+ x for x in products_urls]

        for url in new_product_urls:
            yield Request(url=url, callback=self.parse_product_tab1)
       
    
    def parse_product_tab1(self, response):

        
        first_tab = {}
        first_tab['product_detail'] = response.xpath('//div[@class="large-9 columns"]/h1/span/text()').extract()
        first_tab['introduction'] = response.xpath('//div[@class="medium-6 columns"]/p/text()').extract() 
        first_tab['headings'] = response.xpath('//div[@class="medium-6 columns"]//h2/text()').extract()
        first_tab['industries_welding'] = response.xpath('//div[@class="medium-6 columns"]//ul/li/text()').extract()


        yield Request(url=response.url + '&tab=2', callback=self.parse_product_tab2, meta=first_tab)


    def parse_product_tab2(self, response):     

        elements = response.xpath('//div[@class="medium-8 columns"]//strong/text()').extract()
        values = response.xpath('//div[@class="medium-8 columns"]//td/text()').extract()

        product_detail = response.meta['product_detail']
        introduction = response.meta['introduction']
        headings = response.meta['headings']
        industries_welding = response.meta['industries_welding']
       
         
        item = EsabnaItem() 
        item['product_detail'] = product_detail
        item['introduction'] = introduction
        item['headings'] = headings
        item['industries_welding'] = industries_welding
        item['elements'] = elements
        item['values'] = values
        yield item

