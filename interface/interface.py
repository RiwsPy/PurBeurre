"""

Class Interface
Contains all methods which allow the user to interact with PurBeurre interface

"""

from api.locale import URL_PRODUCT, CATEGORIES


class Interface:
    def __init__(self, bdd):
        """
            Interface initialisation
        """
        self.bdd = bdd
        self.initialize()
        self.show_init_menu()

    def initialize(self):
        self.category = None
        self.product = None
        self.option = 0
        self.products_info = []

    def display_menu(self, choices):
        """
            Display header and choices to the PurBeurre's window
            then lauch the corresponding method

            *param choices:
                [0] : text,
                [1] : method to apply if the option is chosen
            *type choices: list(tuple)
            *return: None
        """
        choices.append(("Quitter PurBeurre", self.quit))

        for index, choice in enumerate(choices):
            if index:
                print(f"{index}- {choice[0]}")
            else:
                print("\n" + "*"*len(choice[0]))
                print(choice[0] + "\n")  # header

        option = self.check_error(input(), index)
        self.option = option
        choices[option][1]()

    def show_init_menu(self):
        """
            Displays the 'Welcome' menu
        """
        self.initialize()
        choices = [
            ("Bienvenue sur PurBeurre, veuillez choisir une option :",
                self.show_init_menu),
            ("Substituer un produit.",
                self.show_category_menu),
            ("Retrouver mes produits substitués.",
                self.show_favorite_product)]
        self.display_menu(choices)

    def show_category_menu(self):
        """
            Displays menu with all cateogry product
        """
        self.category = None
        choices = [
            ("Sélectionnez la catégorie du produit :",
                self.show_category_menu)]
        for category in CATEGORIES:
            choices.append((category, self.show_food_menu))
        choices.append(("Revenir au menu précédent", self.show_init_menu))
        self.display_menu(choices)

    def show_food_menu(self):
        """
            Displays menu with all products in the category chosen previously
        """
        if self.category is None:
            self.category = self.option-1
        cat_id = self.category

        products = self.bdd.all_products_in_category(cat_id)
        if not products:
            print("\nOups ! Il n'y aucun produit qui correspond à ces critères !")
            self.wait()
            self.show_init_menu()
            return None

        self.products_info = products
        choices = [
            ("Sélectionnez le produit souhaité :",
                self.show_food_menu)]
        for product in products:
            choices.append((product[0], self.show_result))
        choices.append(("Revenir au menu précédent", self.show_category_menu))
        self.display_menu(choices)

    def show_result(self):
        """
            Displays the search result
            Results are already sorted by nova_score and nutrition_score
        """
        print("\n*********\nRésultat :\n")
        if self.option == 1:
            print("Aucun substitut trouvé !\
                Ce produit est le plus que nous ayons dans cette catégorie.")
        else:
            self.show_product(self.products_info[0][1], self.products_info)

            save = input("\n\nSauvegarder le résultat ? (o/n)").lower()
            if save == 'o':
                self.bdd.save_product(
                    self.products_info[self.option-1][1],
                    self.category,
                    self.products_info[0][1])
                print("Produit sauvegardé.")
        self.wait()
        self.show_init_menu()

    def show_product(self, code_product, products_info=None):
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

        print(f"Nom : {products_info[0][0]} (code {products_info[0][1]})\
            \nScore Nova : {products_info[0][2]},\
            \nNutri-Score : {products_info[0][3].upper()}\
            \nMagasin(s) : {products_info[0][4]}\
            \nLien OFF : {URL_PRODUCT}/{products_info[0][1]}")

    def show_favorite_product(self):
        """
            Display all favorite products and his substitute
        """
        info = self.bdd.all_favorite_product()
        if info:
            print("\n*********\nProduits favoris :")
            for code, category, substitute_code in info:
                print(f"\nCatégorie {self.bdd.category_id_to_name(category)}")
                self.show_product(code)
                print("\n******\nRemplacé par :")
                self.show_product(substitute_code)
                self.wait()
        else:
            print("Aucun produit trouvé !")
            self.wait()
        self.show_init_menu()

    def check_error(self, answer, nb_choice):
        """
            Checks that the answer is indeed an integer
            and corresponds to a possible choice

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

    def wait(self):
        """
            Wait a keyboard event
        """
        input('\nAppuyez sur une touche pour continuer.')

    def quit(self):
        """
            Quit PurBeurre

            *return: None
        """
        print("A bientôt sur PurBeurre.")
        self.bdd.close_connection()
