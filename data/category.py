"""

Class Category


"""


class Category:
    def __init__(self, bdd, category_name, index):
        """
            Initialize a new Category

            *param bdd: database
            *param category_name: category name
            *param index: id number in Category table
            *type bdd: database.Database
            *type category_name: str
            *type index: int
        """
        self.bdd = bdd
        self.category_name = category_name
        self.index = index

    def add(self):
        """
            Add a new category in Category table
        """

        self.bdd.add_category(self.category_name, self.index)
