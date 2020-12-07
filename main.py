"""
    PurBeurre application

    to launch application :
    > python3 main.py

    one argument is accepted : -updateBD (or -uDB)
    for upload the database from Open Fact Foods API

"""

from interface import interface
from sql import database
from api import openfoodfacts
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-uDB", "--updateDB",
        help="Update database with API Data",
        action="store_true")
    args = parser.parse_args()

    bdd = database.Database()
    if bdd.open_connection():
        if args.updateDB:
            openfoodfacts.call_api(bdd)

        interface.Interface(bdd)
        bdd.close_connection()
