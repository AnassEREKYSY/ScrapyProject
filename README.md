# ScrapyProject

- This is a web scraping project for the H&M brand. We have selected 7 products to test: jeans, shirts, shoes, accessories, lingerie, T-shirts, and sportswear. Currently, we are scraping the price, name, and gender for each product, but we plan to add more functionalities in future versions, requiring additional information.

- We aim to compare the prices of each product between men's and women's sections, providing statistics such as average, maximum, and minimum prices in a well-designed web page.


## Prerequisites

- Python
- Scrapy
- Docker


## Getting Started

1. Clone the repository: [ScrapyProject](https://github.com/AnassEREKYSY/ScrapyProject)
2. execute the commande : scrapy startprojet nomProjet to create a scrapy project
3. create a spider in /spiders folder to scrap data
4. to execute spider tap this commande : scrapy crawl nomSppider // scrapy crawl nomSpider -O nomSpider.Json

## TODO List

- [x] Create Spiders
- [x] Scrap data 
- [x] Store the scraped Data in json files
- [x] Calculate Average, Max and Min prices for each product 
- [x] Create Template that show Statistics 
    ![alt text](./ScrapyProject/ScrapyProject/statistique.png)
- [x] Create dockerFile, dockerCompose

## Features

- [x] Store scraped data in a containerized MySQL or PostgreSQL database.


## Objectif
1. The current objective of this project is to provide insights into H&M product prices for competitors.
    In the future, we aim to make this project more generalizable so that any store can utilize it to obtain statistics on competitor prices.
2. Another objective is to store the data in a containerized database instead of JSON files.
    Feel free to modify and expand upon this README as needed to accurately reflect your project and its goals.
