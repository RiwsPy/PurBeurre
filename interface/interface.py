"""

Class Interface
Contains all methods which allow the user to interact with PurBeurre interface

"""

import sys
from api.locale import URL_PRODUCT, CATEGORIES

class Interface:
    def __init__(self, bdd):
        """
            Interface initialisation
        """
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
        """
            Displays the 'Welcome' menu
        """
        choices = [
            ["Bienvenue sur PurBeurre, veuillez choisir une option :", 'show_init_menu'],
            ["Je souhaite substituer un produit.", 'show_category_menu'],
            ["Retrouver mes produits substitués.", 'show_favorite_product']]
        self.display_menu(choices)

    def show_category_menu(self):
        """
            Displays menu with all cateogry product
        """
        choices = [
            ["Sélectionnez la catégorie du produit :", 'show_category_menu']]
        for category in CATEGORIES:
            choices.append([category, 'show_food_menu'])
        self.display_menu(choices, 'category')

    def show_food_menu(self):
        """
            Displays menu with all products in the category chosen previously
        """
        cat_id = self.option-1
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
            Results are already sorted by nova_score and nutrition_score
        """
        print("Résultat :")
        if self.option == 1:
            print("Aucun produit trouvé.")
            return None

        self.show_product(self.products_info[0][1], self.products_info)

        save = input("Sauvegarder le résultat ? (o/n)").lower()
        if save == 'o':
            self.bdd.save_product(self.products_info[self.option-1][1], self.products_info[0][1])

    def show_product(self, code_product, products_info = None):
        """
            Display all product informations and API URL
            Informations can be added directly in parameters (faster)

            *param code_product: product code to display
            *param products_info: products informations
            *type code_product: int
            *type products_info: tuple(tuple)
        """
        if not products_info:
            products_info = self.bdd.all_info_product(code_product)

        print(f"{products_info[0][0]} (code {products_info[0][1]})\
            \nScore Nova : {products_info[0][2]},\
            \nNutri-Score : {products_info[0][3].upper()}\
            \nMagasin(s) : {products_info[0][4]}\
            \nLien OFF : {URL_PRODUCT}/{products_info[0][1]}")

    def show_favorite_product(self):
        """
            Display all favorite products and his substitute
        """
        print("Produits favoris :")
        for couple in self.bdd.all_favorite_product():
            self.show_product(couple[0])
            print('Remplacé par :')
            self.show_product(couple[1])

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
            Quit PurBeurre

            *return: None
        """
        print("A bientôt sur PurBeurre.")
        sys.exit()