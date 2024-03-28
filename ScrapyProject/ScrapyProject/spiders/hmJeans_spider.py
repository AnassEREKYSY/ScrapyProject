from jinja2 import Template
import scrapy
import mysql.connector
from mysql.connector import errorcode

class HMJeansSpider(scrapy.Spider):
    name = 'hmspiderJeans'
    allowed_domains = ['www2.hm.com']
    start_urls = [
        'https://www2.hm.com/fr_fr/homme.html', # Men's section
        'https://www2.hm.com/fr_fr/femme.html'  # Women's section
    ]

    men_prices = []
    women_prices = []

    def parse(self, response):
        jeans=[
            response.css('a[href*="/fr_fr/homme/catalogue-par-produit/jeans.html"]::attr(href)').get(),
            response.css('a[href*="/fr_fr/femme/catalogue-par-produit/jeans.html"]::attr(href)').get(),
        ]
        for jean in jeans:
            if '/homme/' in jean:
                yield response.follow(jean, callback=self.parse_jeans, meta={'gender': 'men'})
            elif '/femme/' in jean:
                yield response.follow(jean, callback=self.parse_jeans, meta={'gender': 'women'})


    def parse_jeans(self, response):
        gender = response.meta.get('gender')

        jeans_article = response.xpath('//*[@id="products-listing-section"]/ul/li/section/article')
        prices = [] 
        # Connect to the MySQL database
        # try:
        #     cnx = mysql.connector.connect(
        #         user=self.settings.get('MYSQL_USER'),
        #         password=self.settings.get('MYSQL_PASSWORD'),
        #         host=self.settings.get('MYSQL_HOST'),
        #         database=self.settings.get('MYSQL_DATABASE')
        #     )
        # except mysql.connector.Error as err:
        #     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        #         self.logger.error("Something is wrong with your MySQL user name or password")
        #     elif err.errno == errorcode.ER_BAD_DB_ERROR:
        #         self.logger.error("Database does not exist")
        #     else:
        #         self.logger.error(err)

        # cursor = cnx.cursor()

        # # Insert scraped data into the MySQL table
        # add_data = ("INSERT INTO jeans_data "
        #             "(gender, category, price) "
        #             "VALUES (%s, %s, %s)")
        for article in jeans_article:
            data_article = article.xpath('.//div[@class="eed2a5 ec329a d5728c"]//div[@class="b86b62 ec329a"]')
            category = data_article.xpath('.//a/h2/text()').get()
            price = data_article.xpath('.//p/span/text()').get()
            
            # Convert price to float for comparison
            price_float = float(price.replace('€', '').replace(',', '.'))
            prices.append(price_float)

            # data = (gender, category, price_float)
            # cursor.execute(add_data, data)
            
            yield {
                'gender': gender,
                'category': category,
                'price': price,
            }
        if gender == 'men':
            self.men_prices.append(prices)
        elif gender == 'women':
            self.women_prices.append(prices)
        
        next_page = response.xpath('//a[@class="acae11 e0a93a b92105 a213fe e35f0b"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_jeans, meta={'gender': gender})
        # Commit the transaction
        # cnx.commit()

        # # Close connections
        # cursor.close()
        # cnx.close()

    def closed(self, reason):
        men_average_price = sum(map(sum, self.men_prices)) / sum(len(x) for x in self.men_prices) if self.men_prices else 0
        women_average_price = sum(map(sum, self.women_prices)) / sum(len(x) for x in self.women_prices) if self.women_prices else 0

        men_highest_price = max(map(max, self.men_prices)) if self.men_prices else 0
        women_highest_price = max(map(max, self.women_prices)) if self.women_prices else 0

        men_lowest_price = min(map(min, self.men_prices)) if self.men_prices else 0
        women_lowest_price = min(map(min, self.women_prices)) if self.women_prices else 0

        men_average_price_formatted = "{:.2f}".format(men_average_price)
        women_average_price_formatted = "{:.2f}".format(women_average_price)
        men_highest_price_formatted = "{:.2f}".format(men_highest_price)
        women_highest_price_formatted = "{:.2f}".format(women_highest_price)
        men_lowest_price_formatted = "{:.2f}".format(men_lowest_price)
        women_lowest_price_formatted = "{:.2f}".format(women_lowest_price)

        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Jeans Prices</title>
            <!-- Bootstrap CSS -->
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <!-- Font Awesome -->
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
            <style>
                .navbar {
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add shadow to navbar */
                }
                .card {
                    margin-top: 20px; /* Add margin-top to cards */
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Add shadow to cards */
                }
                .logo {
                    width: 20px;
                    height: auto;
                    margin-right: 5px;
                }
                footer {
                    position: fixed;
                    bottom: 0;
                    width: 100%;
                    background-color: #f8f9fa; /* Light gray background color */
                    text-align: center;
                    padding: 10px 0;
                }
            </style>
        </head>
        <body>
            <!-- Navbar -->
            <nav class="navbar navbar-light bg-light">
                <a class="navbar-brand mx-auto" href="#">
                    <img src="ScrapyLogo.png" class="logo" alt="Scrapy Logo">
                    Scrapy
                </a>
            </nav>

            <!-- Content -->
            <div class="container mt-5">
                <h3 class="text-center mt-4 mb-4">Jeans Statistics</h3>
                <div class="row justify-content-center">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Men <i class="fas fa-male"></i></h5>
                                <ul class="list-group">
                                    <li class="list-group-item"><i class="fas fa-percent"></i> Average Price: {{ men_average_price }} <i class="fas fa-dollar-sign"></i></li>
                                    <li class="list-group-item"><i class="fas fa-arrow-up"></i> Highest Price: {{ men_highest_price }} <i class="fas fa-dollar-sign"></i></li>
                                    <li class="list-group-item"><i class="fas fa-arrow-down"></i> Lowest Price: {{ men_lowest_price }} <i class="fas fa-dollar-sign"></i></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Women <i class="fas fa-female"></i></h5>
                                <ul class="list-group">
                                    <li class="list-group-item"><i class="fas fa-percent"></i> Average Price: {{ women_average_price }} <i class="fas fa-dollar-sign"></i></li>
                                    <li class="list-group-item"><i class="fas fa-arrow-up"></i> Highest Price: {{ women_highest_price }} <i class="fas fa-dollar-sign"></i></li>
                                    <li class="list-group-item"><i class="fas fa-arrow-down"></i> Lowest Price: {{ women_lowest_price }} <i class="fas fa-dollar-sign"></i></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <footer>
                <p>&copy; 2024 H&M. All rights reserved.</p>
            </footer>

            <!-- Bootstrap JS (optional) -->
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
        </html>
        """

        # Render HTML with Jinja2
        template = Template(html_template)
        rendered_html = template.render(
            men_average_price=men_average_price_formatted,
            men_highest_price=men_highest_price_formatted,
            men_lowest_price=men_lowest_price_formatted,
            women_average_price=women_average_price_formatted,
            women_highest_price=women_highest_price_formatted,
            women_lowest_price=women_lowest_price_formatted
        )

        # Write rendered HTML to a file
        with open('template/jeans_prices.html', 'w', encoding='utf-8') as f:
            f.write(rendered_html)