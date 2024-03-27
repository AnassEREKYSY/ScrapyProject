import scrapy
import json

class HMProductSpider(scrapy.Spider):
    name = 'hmspider'
    allowed_domains = ['www2.hm.com']
    start_urls = [
        'https://www2.hm.com/fr_fr/homme.html', # Men's section
        'https://www2.hm.com/fr_fr/femme.html'  # Women's section
    ]

    def parse(self, response):
        # Extracting category links
        men_link=response.xpath('//a[contains(text(), "Homme")]/@href').get()
        women_link=response.xpath('//a[contains(text(), "Femme")]/@href').get()
        jeans=[
            response.css('a[href*="/homme/catalogue-par-produit/jeans.html"]::attr(href)').get(),
            response.css('a[href*="/femme/catalogue-par-produit/jeans.html"]::attr(href)').get(),
        ]
        for jean in jeans:
            yield response.follow(jean, callback=self.parse_jeans)

        chemises=[
            response.css('a[href*="/homme/catalogue-par-produit/chemises.html"]::attr(href)').get(),
            response.css('a[href*="/femme/catalogue-par-produit/chemises.html"]::attr(href)').get(),
        ]
        for chemise in chemises:
            yield response.follow(chemise, callback=self.parse_chemise)

        tShirts=[
            response.css('a[href*="/homme/catalogue-par-produit/t-shirts-et-debardeurs.html"]::attr(href)').get(),
            response.css('a[href*="/femme/catalogue-par-produit/t-shirts-et-debardeurs.html"]::attr(href)').get(),
        ]
        for tshirt in tShirts:
            yield response.follow(tshirt, callback=self.parse_tShirt)

       

    def parse_jeans(self, response):
        # Here you can scrape the product details from the men's jeans section
        # Example: Extracting product links from the jeans section
        jeans_article = response.xpath('//*[@id="products-listing-section"]/ul/li/section/article')

        for article in jeans_article:
            data_article = article.xpath('.//div[@class="eed2a5 ec329a d5728c"]//div[@class="b86b62 ec329a"]')
            images=[]
            category = data_article.xpath('.//a/h2/text()').get()
            price = data_article.xpath('.//p/span/text()').get()

            images_article=article.xpath('//ul[@class="split_list"]/li').getall()
            for li in images_article:
                img_srcset = li.xpath('.//a/div/div/div/span/img/@alt').get()
                if img_srcset:
                    images.append(img_srcset)


            yield {
                'category': category,
                'price': price,
                'image': images,
            }
       
    def parse_chemise(self, response):
        # Here you can scrape the product details from the men's jeans section
        # Example: Extracting product links from the jeans section
        chemise_article = response.xpath('//*[@id="products-listing-section"]/ul/li/section/article')

        for article in chemise_article:
            data_article = article.xpath('.//div[@class="eed2a5 ec329a d5728c"]//div[@class="b86b62 ec329a"]')
            images=[]
            category = data_article.xpath('.//a/h2/text()').get()
            price = data_article.xpath('.//p/span/text()').get()

            images_article=article.xpath('//ul[@class="split_list"]/li').getall()
            for li in images_article:
                img_srcset = li.xpath('.//a/div/div/div/span/img/@alt').get()
                if img_srcset:
                    images.append(img_srcset)


            yield {
                'category': category,
                'price': price,
                'image': images,
            }
       
    def parse_tShirt(self, response):
        # Here you can scrape the product details from the men's jeans section
        # Example: Extracting product links from the jeans section
        jeans_article = response.xpath('//*[@id="products-listing-section"]/ul/li/section/article')

        for article in jeans_article:
            data_article = article.xpath('.//div[@class="eed2a5 ec329a d5728c"]//div[@class="b86b62 ec329a"]')
            images=[]
            category = data_article.xpath('.//a/h2/text()').get()
            price = data_article.xpath('.//p/span/text()').get()

            images_article=article.xpath('//ul[@class="split_list"]/li').getall()
            for li in images_article:
                img_srcset = li.xpath('.//a/div/div/div/span/img/@alt').get()
                if img_srcset:
                    images.append(img_srcset)


            yield {
                'category': category,
                'price': price,
                'image': images,
            }
       
