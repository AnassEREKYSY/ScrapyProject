from scrapy.exceptions import DropItem

class MySQLPipeline:
    def open_spider(self, spider):
        pass  # No need to open connection here

    def close_spider(self, spider):
        pass  # No need to close connection here

    def process_item(self, item, spider):
        # Use spider settings to get MySQL connection details
        mysql_host = spider.settings.get('MYSQL_HOST')
        mysql_user = spider.settings.get('MYSQL_USER')
        mysql_password = spider.settings.get('MYSQL_PASSWORD')
        mysql_database = spider.settings.get('MYSQL_DATABASE')

        # Connect to the MySQL database
        connection = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = connection.cursor()

        # Insert item into the appropriate table
        table_name = spider.name.lower()
        insert_query = f"""
            INSERT INTO {table_name} (gender, category, price)
            VALUES (%s, %s, %s)
        """
        try:
            cursor.execute(insert_query, (item['gender'], item['category'], item['price']))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise DropItem(f"Failed to insert item into {table_name}: {e}")
        finally:
            cursor.close()
            connection.close()

        return item
