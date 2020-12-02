"""

Class Category


"""

class Category:
    def __init__(self, category_name, index):
        self.category_name = category_name
        self.index = index

    def add(self, bdd):
        """
            add a new product in Product table
        """

        bdd.add_category(self.category_name, self.index)