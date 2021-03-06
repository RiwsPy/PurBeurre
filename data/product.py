"""

    Method to configure, add or otherwise product

"""

from api.locale import FIELDS


class Product:
    def __init__(self, bdd):
        """
            Initialize a new Category

            *param bdd: database
            *type bdd: database.Database
        """
        self.bdd = bdd
        self.is_clean = False
        for field in FIELDS:
            setattr(self, field, None)

    def add(self):
        """
            Add a new product in Product table
            The new product need to be cleaned before (see cleaner method)
        """
        if self.is_clean:
            self.bdd.add_product(self.list_field)

    def cleaner(self, product):
        """
            Verifies that Product has all necessary information

            *param product: all product informations
            *type product: list
            *return: None
        """
        for field in FIELDS:
            if field not in product:
                return None
            setattr(self, field, product[field])
        self.is_clean = True

    @property
    def list_field(self):
        """
            Return a list which contains all important product information

            *rtype: list
        """

        return [getattr(self, field) for field in FIELDS]
