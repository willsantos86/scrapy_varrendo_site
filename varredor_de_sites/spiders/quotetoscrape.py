import scrapy

# CamelCase
class QuotesToScrapeSpider(scrapy.Spider):
    # Identidade
    name = 'frasebot'
    # Request
    def start_requests(self):
        # Definir urls a varrer
        urls = ['https://quotes.toscrape.com/']

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)
    # Response
    def parse(self, response):
        # Onde irá processar o que é retornado do response
        for elemento in response.xpath("//div[@class='quote']"):
            yield {
                'frase': elemento.xpath(".//span[@class='text']/text()").get(),
                'autor': elemento.xpath(".//small[@class='author']/text()").get(),
                'tags': elemento.xpath(".//a[@class='tag']/text()").getall(),
            }

        # Como varrer várias paginas:
        
        # Tentar encontrar o botão próximo, se encontrar, vou varrer essas páginas
        try:
            link_proxima_pagina = response.xpath("//li[@class='next']/a/@href").get()
            if link_proxima_pagina is not None:
                link_proxima_pagina_completo = response.urljoin(link_proxima_pagina)
                yield scrapy.Request(url=link_proxima_pagina_completo,callback=self.parse)
        except:
            # Se não encontrar, vou parar automação.
            print('Chegamos na última pagina')