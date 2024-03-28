# ScrapyProject

# First step create a project with scrapy startproject ScrapyProject
# second step is to create spriders for booth Zara and H&M :  scrapy genspider <spider_name> <domain>



# to store data in the database run these commandes
# docker run --name some-postgres -e POSTGRES_PASSWORD=your_postgres_password -d postgres
# docker exec -it some-postgres psql -U postgres
# CREATE DATABASE productDataScraping;

docker run -d --name mongodb mongo
docker exec -it mongodb bash
apt-get update
apt-get install -y mongodb-clients



docker pull postgres
docker network create mynetwork

docker run --name my_postgres_container -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 --network=mynetwork postgres

docker run -it --rm --network=mynetwork postgres psql -h my_postgres_container -U postgres

pip install psycopg2-binary scrapy
pip install psycopg2-binary



pip install mysql-connector-python
pip install mysqlclient
