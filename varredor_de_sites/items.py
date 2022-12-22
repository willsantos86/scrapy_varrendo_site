# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join

def tira_espaco_em_branco(valor):
   return valor.strip()

def processar_caracteres_especiais(valor):
    return valor.replace(u"\u201c",'').replace(u"\u201d",'').replace(u"\u2014",'—').replace(u"\u2019",'')

def nome_autores_maiusculo(valor):
    return valor.upper()

def mudar_separador(valor):
    return valor.replace(u",",';')

class CitacaoItem(scrapy.Item):
    frase = scrapy.Field(
        input_processor=MapCompose(
            tira_espaco_em_branco, processar_caracteres_especiais),
        output_processor=TakeFirst()
    )
    autor = scrapy.Field(
        output_processor=TakeFirst()
    )
    tags = scrapy.Field(
        output_processor=Join(',')
    )


class CitacaoGoodReadsItem(scrapy.Item):
    frase = scrapy.Field(
        input_processor=MapCompose(
            processar_caracteres_especiais,tira_espaco_em_branco),
        output_processor=TakeFirst()
    )
    autor = scrapy.Field(
        input_processor=MapCompose(
            nome_autores_maiusculo,tira_espaco_em_branco),
        output_processor=TakeFirst()
    )
    tags = scrapy.Field(
        output_processor=Join(';')
    )
