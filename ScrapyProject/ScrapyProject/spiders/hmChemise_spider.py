import scrapy

class HMChemiseSpider(scrapy.Spider):
    name = 'hmspiderChemise'
    custom_settings = {
        'ITEM_PIPELINES': {'ScrapyProject.pipelines.MongoDBPipeline': 300,},
    }
    allowed_domains = ['www2.hm.com']
    start_urls = [
        'https://www2.hm.com/fr_fr/homme.html', # Men's section
        'https://www2.hm.com/fr_fr/femme.html'  # Women's section
    ]

    def parse(self, response):
        # Extracting category links
        men_link=response.xpath('//a[contains(text(), "Homme")]/@href').get()
        women_link=response.xpath('//a[contains(text(), "Femme")]/@href').get()

        chemises=[
            response.css('a[href*="/homme/catalogue-par-produit/chemises.html"]::attr(href)').get(),
            response.css('a[href*="/femme/catalogue-par-produit/chemises.html"]::attr(href)').get(),
        ]
        for chemise in chemises:
            yield response.follow(chemise, callback=self.parse_chemise)


    def parse_chemise(self, response):
        # Here you can scrape the product details from the men's jeans section
        # Example: Extracting product links from the jeans section
        chemise_article = response.xpath('//*[@id="products-listing-section"]/ul/li/section/article')

        for article in chemise_article:
            data_article = article.xpath('.//div[@class="eed2a5 ec329a d5728c"]//div[@class="b86b62 ec329a"]')
            images=[]
            category = data_article.xpath('.//a/h2/text()').get()
            price = data_article.xpath('.//p/span/text()').get()

            image=any

            image_article = article.xpath('.//div[@class="e357ce f8323f a098bf"]/span/img[@imagetype="PRODUCT_IMAGE"]/@src').get()
            
            # Check if the image URL is base64 encoded
            if image_article.startswith('data:image'):
                # Handle base64-encoded image
                image_article = article.xpath('.//div[@class="e357ce f8323f a098bf"]/span/img[@imagetype="PRODUCT_IMAGE"]/@src').get()

            image=image_article
            
            yield {
                'category': category,
                'price': price,
                'image': image,
            }
        next_page = response.xpath('//a[@class="acae11 e0a93a b92105 a213fe e35f0b"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_chemise)
       
