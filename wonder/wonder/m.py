from pathlib import Path

import scrapy
#from ..items import CollectwatchesItem

class QuotesSpider(scrapy.Spider):
    name = "collect"
    
    
    start_urls = ['https://www.tagheuer.com/us/en/']


    def parse(self, response):
        category_links=[response.urljoin(i) for i in response.css('div#footer-collapse-0 li a')]
        yield from response.follow_all(category_links,self.parse_two)
            
       
    def parse_two(self,response):
                product_links=response.css('div.product-tile a')
                yield from response.follow_all(product_links,self.parse_product_info)
                more_products=response.css('div.show-more.text-center a')
                if more_products:
                      yield from response.follow_all(more_products,self.parse_two)
    
    def parse_product_info(self,response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()
        options=response.css('div.recommendation-tiles a.rec-tile')
        tech_specifications=response.css('div.container.technical-spec div.card')
        #property_keys=[i.css('button::text').get().strip() for i in tech_specifications]
        keys=[i.css('span.spec-title::text').getall() for i in tech_specifications]

        #keys = [element for innerList in keys for element in innerList]
        values=[i.css('span.spec-value::text').getall() for i in tech_specifications]
        #values= [element for innerList in values for element in innerList]
        #keys=[i.lower() for i in keys]
        print(keys)
        #keys = list(map(lambda x: x.replace('case', 'case_material'), keys))
        #keys = list(map(lambda x: x.replace('size', 'diameter'), keys))
        #keys = list(map(lambda x: x.replace('water resistance', 'water_resistance'), keys))
        #keys = list(map(lambda x: x.replace('balance frequency', 'frequency'), keys))
        #keys = list(map(lambda x: x.replace('', 'reference number'), keys))
           

                             

        #page = response.css('title::text').get()
        #response.css('#tech-accordion span.spec-value::text').getall()
        #print(extract_with_css("span.sales span.value::text"))
        dic={"Listing Title": extract_with_css("h1.product-name"),
             'type':'watch',
            "price":extract_with_css("span.sales span.value::text"),
            'External URL':extract_with_css("link[rel='alternate'][hreflang='en-ca']::attr(href)"),
            'description':extract_with_css("p#collapseDescription::text"),"Seller Name":'NaN',"Seller Link":'NaN',"Jewels": 'NaN',
}
        for i in range(len(keys)):
                      dic[keys[i]]=values[i]
        
        urls=response.css('div.recommendation-tiles img::attr(srcset)').getall()
        clean=[]
        for i in urls:
                clean.append(response.urljoin(i))
        dic['image_urls']=clean
        yield dic
        yield from response.follow_all(options,self.parse_product_info)