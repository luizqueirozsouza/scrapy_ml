import scrapy

class MlSpider(scrapy.Spider):
    name = "ml"

    start_urls = ['https://www.mercadolivre.com.br/ofertas']

    def parse(self, response, **kwargs):
        for i in response.xpath('//ol[@class="items_container"]/li[contains(@class,"promotion-item")]'):
            title = i.xpath('.//p[@class="promotion-item__title"]/text()').get()
            price = i.xpath('.//span[@class="andes-money-amount__fraction"]//text()').get()
            link = i.xpath('.//a/@href').get()

            #acessa a página individual do produto para buscar informações // passa via cb_kwargs para função parse_vendas para montar o dicionário completo.
            yield response.follow(link, callback=self.parse_vendas, cb_kwargs=
            {
                'title' : title,
                'price' : price,
                'link' : link 
            })

        next_page = response.xpath('//a[contains(@title,"Próxima")]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_vendas(self, response, title, price, link):
        vendas = response.xpath('//strong[@class="ui-pdp-seller__sales-description"]/text()').get()

        yield{
            'title' : title,
            'price' : price,
            'link' : link ,
            'vendas': vendas         
        }