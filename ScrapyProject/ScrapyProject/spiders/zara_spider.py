import scrapy

class ZaraFRClothingSpider(scrapy.Spider):
    name = 'zaraspider'
    start_urls = ['https://www.zara.com/fr/']

    def parse(self, response):
        # Extract URLs for men's and women's clothing categories
        mens_url = None
        womens_url = None
        category_links = response.css('a.layout-categories-category__link')
        for link in category_links:
            category_name = link.css('span.layout-categories-category__name::text').get()
            href = link.attrib.get('href')
            if 'homme' in href and any(category in category_name.lower() for category in ['jeans', 'hoodies', 'baskets', 'chemises']):
                mens_url = response.urljoin(href)
            elif 'femme' in href and any(category in category_name.lower() for category in ['jeans', 'chemises', 'robes', 'sacs']):
                womens_url = response.urljoin(href)

        if mens_url:
            yield scrapy.Request(mens_url, callback=self.parse_category)
        if womens_url:
            yield scrapy.Request(womens_url, callback=self.parse_category)

    def parse_category(self, response):
        # Parse the category page and extract item details
        category_name = response.css('h1::text').get().strip()
        items = response.css('div.product-list > article')

        for item in items:
            item_name = item.css('a.name-link::text').get().strip()
            item_price = item.css('span.price::text').get().strip()

            yield {
                'category': category_name,
                'name': item_name,
                'price': item_price
            }
