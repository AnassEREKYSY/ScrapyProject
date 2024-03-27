import scrapy
import json

class HMProductSpider(scrapy.Spider):
    name = 'hmspiderTShirt'
    allowed_domains = ['www2.hm.com']
    start_urls = [
        'https://www2.hm.com/fr_fr/homme.html', # Men's section
        'https://www2.hm.com/fr_fr/femme.html'  # Women's section
    ]

    def parse(self, response):
        # Extracting category links
        men_link=response.xpath('//a[contains(text(), "Homme")]/@href').get()
        women_link=response.xpath('//a[contains(text(), "Femme")]/@href').get()
        tShirts=[
            response.css('a[href*="/homme/catalogue-par-produit/t-shirts-et-debardeurs.html"]::attr(href)').get(),
            response.css('a[href*="/femme/catalogue-par-produit/t-shirts-et-debardeurs.html"]::attr(href)').get(),
        ]
        for tshirt in tShirts:
            yield response.follow(tshirt, callback=self.parse_tShirt)

              
    def parse_tShirt(self, response):
        # Here you can scrape the product details from the men's jeans section
        # Example: Extracting product links from the jeans section
        tshirt_article = response.xpath('//*[@id="products-listing-section"]/ul/li/section/article')

        for article in tshirt_article:
            data_article = article.xpath('.//div[@class="eed2a5 ec329a d5728c"]//div[@class="b86b62 ec329a"]')
            images_article=article.css('ul.split_list::attr(id)').get()
            images=[]
            category = data_article.xpath('.//a/h2/text()').get()
            price = data_article.xpath('.//p/span/text()').get()

            for li in images_article:
                img_src = li.xpath('.//a/div/div/span/img[@imagetype="PRODUCT_IMAGE"]/@src').get()
                if img_src:
                    images.append(img_src)


            yield {
                'category': category,
                'price': price,
                'image': images_article,
            }
       
