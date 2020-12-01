from interface import interface
from sql import database
from api import openfoodfacts

if __name__ == "__main__":
    bdd = database.Database()
    #openfoodfacts.call_api(bdd)
    interface.Interface(bdd)
    #bdd.execute("SELECT id FROM Category")
    #cat = bdd.cursor.fetchall()[10][0]
    #bdd.find_substitute(cat=cat)
    bdd.close_connection()