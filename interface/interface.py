"""

Class Interface
Contains all methods which allow the user to interact with PurBeurre interface

"""

import sys

class Interface:
    def __init__(self):
        self.show_init_menu()

    def display_menu(self, choices):
        """
            Display header and choices to the PurBeurre's window then lauch the corresponding method

            *param choices: [0] : text, [1] : method to apply if the option is chosen
            *type choices: list
            *return: None
        """
        choices.append(["Quitter PurBeurre", 'quit'])
        for index, choice in enumerate(choices):
            if index:
                print(f"{index}- {choice[0]}")
            else:
                print(choice[0] + "\n") #  header

        option = self.check_error(input(), len(choices)-1)

        getattr(self, choices[option][1])()

    def show_init_menu(self):
        choices = [
            ["Bienvenue sur PurBeurre, veuillez choisir une option :", 'show_init_menu'],
            ["Je souhaite substituer un aliment.", 'show_category_menu'],
            ["Retrouver mes aliments substitués.", 'show_init_menu']]
        self.display_menu(choices)

    def show_category_menu(self):
        choices = [
            ["Sélectionnez la catégorie de l'aliment :", 'show_category_menu'],
            ["catégorie 1", 'show_food_menu'],
            ["catégorie 2", 'show_food_menu']]
        self.display_menu(choices)

    def show_food_menu(self):
        choices = [
            ["Sélectionnez l'aliment souhaité :", 'show_food_menu'],
            ["aliment 1", 'show_result'],
            ["aliment 2", 'show_result']]
        self.display_menu(choices)

    def show_result(self):
        print("Résultat :")
        print("****")
        print("Sauvegarder le résultat ? (o/n)")

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