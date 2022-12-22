import scrapy
from scrapy.loader import ItemLoader
from varredor_de_sites.items import CitacaoGoodReadsItem

# CamelCase
class GoodReadsSpider(scrapy.Spider):
    # Identidade
    name = 'quotebot'

    # Request
    def start_requests(self):
        # Definir urls a varrer
        urls = ['https://www.goodreads.com/quotes?page=1']

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    # Response

    def parse(self, response):
        # Onde irá processar o que é retornado do response
        for elemento in response.xpath("//div[@class='quote']"):
            loader = ItemLoader(item=CitacaoGoodReadsItem(),selector=elemento,response=response)
            loader.add_xpath('frase', ".//div[@class='quoteText']/text()")
            loader.add_xpath('autor', ".//span[@class='authorOrTitle']/text()")
            loader.add_xpath('tags', ".//div[@class='greyText smallText left']/a/text()")
            yield loader.load_item()

        # try:
        #     link_proxima_pagina = response.xpath("//a[@class='next_page']/@href").get()
        #     if link_proxima_pagina is not None: 
        #         link_proxima_pagina_completo = response.urljoin(link_proxima_pagina)
        #         yield scrapy.Request(url=link_proxima_pagina_completo,callback=self.parse)
        # except:
        #     print("Chegamos a ultima página")
        numero_proxima_pagina = response.xpath(".//a[@class='next_page']/@href").get().split("=")[1]
        print('#'*20)
        print(numero_proxima_pagina)
        print('#'*20)
        if numero_proxima_pagina is not None:
            link_proxima_pagina = f'https://www.goodreads.com/quotes?page={numero_proxima_pagina}'
            print('#'*20)
            print(numero_proxima_pagina)
            print('#'*20)
            yield scrapy.Request(url=link_proxima_pagina,callback=self.parse)