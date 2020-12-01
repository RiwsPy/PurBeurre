"""

Class Interface
Contains all methods which allow the user to interact with PurBeurre interface

"""

import sys
from api.locale import URL_PRODUCT

class Interface:
    def __init__(self, bdd):
        self.bdd = bdd
        self.category = None
        self.product = None
        self.option = 0
        self.products_info = []
        self.show_init_menu()

    def display_menu(self, choices, attribut = None):
        """
            Display header and choices to the PurBeurre's window then lauch the corresponding method

            *param choices: [0] : text, [1] : method to apply if the option is chosen
            *param attribut: if not None, save the user choice in self.attribut
            *type choices: list
            *type attribut: str
            *return: None
        """
        choices.append(["Quitter PurBeurre", 'quit'])
        for index, choice in enumerate(choices):
            if index:
                print(f"{index}- {choice[0]}")
            else:
                print(choice[0] + "\n") #  header

        option = self.check_error(input(), len(choices)-1)
        self.option = option

        if attribut:
            setattr(self, attribut, choices[option][0])

        getattr(self, choices[option][1])()

    def show_init_menu(self):
        choices = [
            ["Bienvenue sur PurBeurre, veuillez choisir une option :", 'show_init_menu'],
            ["Je souhaite substituer un produit.", 'show_category_menu'],
            ["Retrouver mes produits substitués.", 'show_init_menu']]
        self.display_menu(choices)

    def show_category_menu(self):
        categories = self.bdd.all_categories_name()
        choices = [
            ["Sélectionnez la catégorie du produit :", 'show_category_menu']]
        for category in categories:
            choices.append([category[0], 'show_food_menu'])
        self.display_menu(choices, 'category')

    def show_food_menu(self):
        cat_id = self.bdd.category_name_to_id(self.category)[0][0]
        products = self.bdd.all_products_in_category(cat_id)
        self.products_info = products
        choices = [
            ["Sélectionnez le produit souhaité :", 'show_food_menu']]
        for product in products:
            choices.append([product[0], 'show_result'])
        self.display_menu(choices)

    def show_result(self):
        """
            Displays the search result 
            Results are already sorted
        """
        print("Résultat :")
        if self.option == 1:
            print("Aucun produit trouvé.")
            return None

        print(f"{self.products_info[0][0]} (code {self.products_info[0][1]})\
            \nScore Nova : {self.products_info[0][2]},\
            \nNutri-Score : {self.products_info[0][3].upper()}\
            \nMagasin(s) : {self.products_info[0][4]}\
            \nLien OFF : {URL_PRODUCT}/{self.products_info[0][1]}")
        save = input("Sauvegarder le résultat ? (o/n)").lower()
        if save == 'o':
            self.bdd.save_product(self.products_info[self.option-1][1], self.products_info[0][1])

    def check_error(self, answer, nb_choice):
        """
            Checks that the answer is indeed an integer and corresponds to a possible choice

            *param answer: user answer put in the input
            *param nb_choice: number of possible responses
            *type answer: str
            *type nb_choice: int
            *return: user choice, 0 if the choice is incorrect
            *rtype: int between 0 and nb_choice
        """
        if not answer.isnumeric():
            return 0
        answer = int(answer)
        if answer < 1 or answer > nb_choice:
            return 0
        return answer

    def quit(self):
        """
            quit PurBeurre
            *return: None
        """
        print("A bientôt sur PurBeurre.")
        sys.exit()