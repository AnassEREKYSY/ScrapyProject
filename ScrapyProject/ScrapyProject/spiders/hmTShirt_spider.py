import scrapy
class HMTShirtSpider(scrapy.Spider):
    name = 'hmspiderTShirt'
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
            yield response.follow(next_page, callback=self.parse_tShirt)
       
