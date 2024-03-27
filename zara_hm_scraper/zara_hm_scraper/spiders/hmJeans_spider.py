import scrapy
import json

class HMProductSpider(scrapy.Spider):
    name = 'hmspiderJeans'
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
                img_src = li.xpath('.//a/div/div/div/span/img/@src').get()
                if img_src:
                    images.append(img_src)


            yield {
                'category': category,
                'price': price,
                'image': images,
            }