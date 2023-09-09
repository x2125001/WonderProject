from pathlib import Path

import scrapy
#from ..items import CollectwatchesItem

class QuotesSpider(scrapy.Spider):
    name = "collect"
    
    
    start_urls = ['https://www.tagheuer.com/us/en/timepieces/collections/tag-heuer-formula-1/',
                  'https://www.tagheuer.com/us/en/smartwatches/collections/tag-heuer-connected/',
                  'https://www.tagheuer.com/us/en/timepieces/collections/tag-heuer-carrera/',
                  'https://www.tagheuer.com/us/en/timepieces/collections/tag-heuer-aquaracer/',
                  'https://www.tagheuer.com/us/en/timepieces/collections/tag-heuer-monaco/',
                  'https://www.tagheuer.com/us/en/timepieces/collections/tag-heuer-autavia/',
                  'https://www.tagheuer.com/us/en/timepieces/collections/tag-heuer-link/']


    def parse(self, response):
         product_links=response.css('div.product-tile a')
         yield from response.follow_all(product_links,self.parse_product_info)
         more_products=response.css('div.show-more.text-center a')
         if more_products:
                yield from response.follow_all(more_products,self.parse)
            
       
    
    
    def parse_product_info(self,response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()
        options=response.css('div.recommendation-tiles a.rec-tile')
        tech_specifications=response.css('div.container.technical-spec div.card')
        #property_keys=[i.css('button::text').get().strip() for i in tech_specifications]
        keys=[i.css('span.spec-title::text').getall() for i in tech_specifications]

        keys = [element for innerList in keys for element in innerList]
        values=[i.css('span.spec-value::text').getall() for i in tech_specifications]
        values= [element for innerList in values for element in innerList]
        values=[i.strip() for i in values]
        keys=[i.lower().strip() for i in keys]
        keys = list(map(lambda x: x.replace('case', 'case_material'), keys))
        keys = list(map(lambda x: x.replace('size', 'diameter'), keys))
        keys = list(map(lambda x: x.replace('water resistance', 'water_resistance'), keys))
        keys = list(map(lambda x: x.replace('balance frequency', 'frequency'), keys))
        keys[-1]='reference number'
        #keys = list(map(lambda x: x.replace('', 'reference number'), keys))
        dic={"Listing Title": extract_with_css("h1.product-name::text")+extract_with_css("p.product-sub-collection::text"),
             'type':'watch',
            "price":extract_with_css("span.sales span.value::text"),
            'External URL':extract_with_css("link[rel='alternate'][hreflang='en-ca']::attr(href)"),
            'description':extract_with_css("p#collapseDescription::text"),"Currency": "USD", 'Brand':'tagheuer'}
        for i in range(len(keys)):
                      dic[keys[i]]=values[i]
        
        urls=response.css('div.recommendation-tiles img::attr(srcset)').getall()
        clean=[]
        for i in urls:
                clean.append(response.urljoin(i))
        dic['image_urls']=clean
        yield dic
        yield from response.follow_all(options,self.parse_product_info)