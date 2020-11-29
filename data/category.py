"""

Class Category


"""

from sql import database

class Category:
    def __init__(self):
        pass

    def add(self, bdd, categories):
        """
            add a new product in Product table
            return: set that contains all category id
            rtype: set
        """
        list_category = categories.split(",")
        result_set = set()
        for name in list_category:
            id = bdd.add_category(name.lstrip())
            result_set.add(id)

        return result_set