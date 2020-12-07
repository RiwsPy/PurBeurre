"""

Class Database
Has a method to connect and request data from sql database

"""

# pipenv install
# pipenv install mysql.connector
# pipenv shell


import mysql.connector
import os
import sys
# import settings


class Database:
    def __init__(self):
        """ For configurate and connect to Database, configure '.env' file """
        self.bd_name = os.getenv("DATABASE")
        self.bd_user = os.getenv("SQL_USER")
        self.bd_password = os.getenv("SQL_PASSWORD")
        self.cnx = None
        self.cursor = None

    def open_connection(self):
        """
            Open connection to Database
            return: True if the connection is ok, False otherwise
            rtype: bool
        """

        if self.init_connection():
            self.create_database()
            self.execute_sql_file_in_database('sql/tables_queries.sql')
            self.create_index_nova_nutri_score()
            return True

        self.close_connection()
        return False

    def create_database(self):
        """
            Create local Database and use it
        """
        self.execute("CREATE DATABASE IF NOT EXISTS " + self.bd_name)
        self.execute("USE " + self.bd_name)

    def execute_sql_file_in_database(self, filename):
        """
            Execute filename in database like a SOURCE command

            *param filename: file name to load
            *type filename: str
            *return: query return
            *rtype: list
        """

        with open(filename, 'r') as bdd:
            sql_queries = bdd.read().split(';')

        for query in sql_queries[:-1]:  # last value is ignored
            self.execute(query)

    def clear_all_tables(self):
        """
            Drop all table in database
        """
        self.execute("DROP TABLE IF EXISTS Assoc_product_category")
        self.execute("DROP TABLE IF EXISTS Favorite_product")
        self.execute("DROP TABLE IF EXISTS Product")
        self.execute("DROP TABLE IF EXISTS Category")

    def execute(self, query, data=None):
        """
            Execute query in Database with data (facultative)
            See mysql.connector.connect.execute for more informations
            Print error, commit or rollback if necessary

            *param query: query to execute
            *param data: data in query
            *type query: str
            *type data: tuple
            *return: True if the query is valid, False otherwise
            *rtype: bool
        """
        # "you must commit the data after a sequence of
        # INSERT, DELETE, and UPDATE statements."
        # For more informations :
        # https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

        need_commit = False
        first_statement = query.split(" ")[0].upper()
        if first_statement in ["INSERT", "DELETE", "UPDATE"]:
            need_commit = True

        try:
            self.cursor.execute(query, data)
            if need_commit:
                self.cnx.commit()
        except mysql.connector.Error as error:
            print(error)
            if need_commit:
                self.cnx.rollback()
            return False

        return True

    def init_connection(self):
        """ Open connection

            *return: True if the connection is ok, False otherwise
            *rtype: bool
        """

        # print("Connexion à la base de données.")

        try:
            self.cnx = mysql.connector.connect(
                database=self.bd_name,
                user=self.bd_user,
                password=self.bd_password
                )
            self.cursor = self.cnx.cursor()
            # other connect method
            # self.cnx = mysql.connector.connect(option_files='data/my.conf',
            # option_groups=['connector_python'])
        except mysql.connector.Error as error:
            print("Erreur lors de la connexion à la base de données.")
            print(error)
            return False

        return True

    def close_connection(self):
        """ Close connection """
        # print("Déconnexion de la base de données.")
        self.cursor.close()
        self.cnx.close()
        sys.exit()

    def add_product(self, product):
        """
            Add a product in Product table

            *param product: list with 6 parameters :
                code, product_name, nova_score, nutrition_score,
                store_name, categories
            *type product: list
        """

        add_line = "INSERT INTO Product \
            (code, product_name, nova_score, nutrition_score, store_name) \
            VALUES (%s, %s, %s, %s, %s)\
            ON DUPLICATE KEY UPDATE\
                code = %s,\
                product_name = %s,\
                nova_score = %s,\
                nutrition_score = %s,\
                store_name = %s"

        data_line = (
            product[0], product[1], product[2], product[3], product[4],
            product[0], product[1], product[2], product[3], product[4])
        self.execute(add_line, data_line)

    def add_category(self, name, index):
        """
            Add a category in Category table

            *param name: category name
            *param index: category index
            *type name: str
            *type index: int
        """
        add_line = "INSERT INTO Category (id, category_name)\
            VALUES (%s, %s)\
            ON DUPLICATE KEY UPDATE\
            id = %s, category_name = %s"
        data_line = (index, name[:100], index, name[:100])
        self.execute(add_line, data_line)

    def category_name_to_id(self, name):
        """
            Selects the id category by its name

            *param name: category name
            *type name: str
            *return: query return
            *rtype: tuple
        """
        add_line = "SELECT id FROM Category WHERE category_name = %s"
        data_line = (name,)
        self.execute(add_line, data_line)
        return self.cursor.fetchall()

    def add_assoc_pro_cat(self, product, cat_id):
        """
            Insert in table Assoc_product_category the followed parameters

            *param product: product to add
            *param cat_id: product category identifier
            *type product: product.Product
            *type cat_id: int
        """
        if product.is_clean:
            add_line = "INSERT INTO Assoc_product_category (code, id) \
                VALUES (%s, %s)"
            data_line = (product.code, cat_id)
            self.execute(add_line, data_line)

    def create_index_nova_nutri_score(self):
        """
            Create index between two columns : nova_score and nutrition_score
            The result is : the sorting is faster
        """
        self.execute("ALTER TABLE Product ADD INDEX ind_nova_nutri\
            (nova_score, nutrition_score)")

    def all_info_product(self, code_product):
        """
            Select and return product informations stored in Product table
            for one product

            *param code_product: product code to search
            *type code_product: int
            *return: 5 product informations
            *rtype: tuple
        """
        add_line = "SELECT product_name, code, nova_score, nutrition_score, store_name\
        FROM Product WHERE code = %s"
        data_line = (code_product,)
        self.execute(add_line, data_line)
        return self.cursor.fetchall()

    def all_products_in_category(self, cat):
        """
            Select and return all products in the category

            *param cat: products category
            *type cat: int
            *return: codes of all products
            *rtype: tuple
        """
        self.execute("SELECT p.product_name, p.code, p.nova_score, p.nutrition_score, p.store_name\
            FROM Product AS p\
            INNER JOIN Assoc_product_category AS a\
                ON a.code = p.code\
            WHERE a.id = %s\
            ORDER BY nova_score, nutrition_score, code\
            LIMIT 50", (cat,))
        return self.cursor.fetchall()

    def all_favorite_product(self):
        """
            Select and return all code product
            and code of their substitute product

            *rtype: tuple(tuple)
        """
        add_line = "SELECT code, substitute_code FROM Favorite_product"
        self.execute(add_line)
        return self.cursor.fetchall()

    def save_product(self, product_code, substitute_code):
        """
            Save in Favorite_product table a product code
            and the code of this subtitute product

            *param product_code: code product
            *param substitute_code: code of the subtitute product
            *type product_code: int
            *type substitute_code: int
        """
        add_line = "\
            INSERT INTO Favorite_product (code, substitute_code)\
            VALUES (%s, %s)\
            ON DUPLICATE KEY UPDATE\
                code = %s, substitute_code = %s"
        data_line = (product_code, substitute_code,
                     product_code, substitute_code)
        self.execute(add_line, data_line)
