"""

    Method to configure, add or otherwise product

"""

from sql import database

class Product:
    def __init__(self):
        pass

    def add(self, bdd, set_info):
        """
            add a new product in Product table
            return: product's code
            rtype: str
        """

        return bdd.add_product(set_info)