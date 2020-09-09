#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module manage all the input and print from the user."""

# -tc- attention à la PEP8
import random
from colorama import Fore, init

from settings import category_app
# -tc- utiliser les managers
from database_xchange.managers import DataMgt

init()


class App:
    """Management of the application."""

    def __init__(self):
        self.launched = True
        self.display_prod_list = {}
        self.id_product_origin = ()
        self.product_origin = None
        self.product_substitute = None

    def intro(self):
        """This method will manage the first screen displayed after launching
        the program."""

        print("\n\n")
        print("                               ---------------------------")
        print("                                Bienvenue sur MyFoodApp !")
        print("                               ---------------------------")
        print("\n\n")
        print(Fore.YELLOW + " Vous avez décidé de mieux consommer "
              "pour votre santé,"
              " MyFoodApp (basé sur l'API OpenFoodFact)\n"
              " vous aidera à selectionner les meilleurs produits.")
        print(Fore.RESET)

    def category_choice(self):
        """display category choice."""

        print(Fore.CYAN)
        print("\n        *** Que souhaitez-vous faire ? *** \n\n")
        print(Fore.RESET)
        print("       1  - Quel aliment souhaitez-vous remplacer ?")
        print("       2  - Retrouver mes aliments substitués")
        print("       3  - Quitter")
        authorised_answer_list, user_answer = ['1', '2', '3'], '0'
        while user_answer not in authorised_answer_list:
            # -tc- attention, on veut répéter l'affichage du menu si le choix n'est pas bon
            print(Fore.GREEN)
            user_answer = input("       Entrer votre choix : ")
            print(Fore.RESET)
        if user_answer == '1':
            # -tc- Imbriquer les appels de fonction de menu n'est pas une bonne idée
            self.category_choice_display()
            # -tc- pourquoi gérer les étapes d'après ici?
            self.display_selected_prod()
            self.display_substitute()
            self.display_save_substitute()
        elif user_answer == '2':
            self.favorites_display()
        elif user_answer == '3':
            self.quit_message()
            self.launched = False
        else:
            self.category_choice()
            print(user_answer)
        print(Fore.RESET)

    def category_choice_display(self):
        """display the choice of the categories."""

        temp_var = DataMgt()
        result = temp_var.get_all_cat()
        print("       ---------------------------------")
        print("                  Catégories :")
        print("       ---------------------------------\n")
        for index, line in enumerate(result, 1):
            print(f"       {index}  -  {line[1]}")
        # -tc- si on a 200 categories, tu ne va pas coder authorised_answer_list à la main
        authorised_answer_list, user_answer = [
            '1', '2', '3', '4', '5', '6', '7'], None
        while user_answer not in authorised_answer_list:
            print(Fore.GREEN)
            user_answer = input("       Entrer un numero de categorie : ")
            print(Fore.RESET)
        if user_answer in authorised_answer_list:
            self.display_prod_by_category(int(user_answer))
        else:
            self.category_choice_display()

    def display_prod_by_category(self, category_selected):
        """display 10 products from the selected category."""

        print("       -------------------------------------")
        print(f"         Categorie {category_app[category_selected]}")
        print("       ------------------------------------- \n")
        temp_var1 = DataMgt()
        result_1 = temp_var1.get_prod_by_category(category_selected)
        # -tc- gérer le random en sql
        selected = random.sample(result_1, 10)
        ordered = sorted(selected, key=lambda x: x[0])
        for index, line in enumerate(ordered, 1):
            print(
                f"       {index}  - Nom        : {line[1]}      Marque: "
                f"* {line[2]} *\n            description: {line[5]}  "
                f"(Nutri-Score: {line[4].upper()}) \n")
            self.display_prod_list.update({index: line})

    def display_selected_prod(self):
        """ask to the user to choose a product."""

        # -tc- si 200 produits, tu ne veux pas coder cette liste à la main
        authorised_answer_list, user_answer = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], None
        while user_answer not in authorised_answer_list:
            print(Fore.GREEN)
            user_answer = input(
                "       Entrer un numéro de produit à remplacer: ")
            print(Fore.RESET)
        if user_answer in authorised_answer_list:
            self.product_origin = self.display_prod_list[int(user_answer)]
            return self.product_origin

    def display_substitute(self):
        """display the substitute suggested."""

        self.display_prod_list = {}
        temp_var = DataMgt()
        result1 = temp_var.suggest_substitute(self.product_origin)
        self.product_substitute = random.choice(result1)
        print(Fore.CYAN)
        print("       Nous vous suggerons :\n")
        print(Fore.RESET)
        print(f"       Nom          : {self.product_substitute[1]}\n"
              f"       Description  : {self.product_substitute[2]}\n"
              f"       Magasin      : {self.product_substitute[3]}\n"
              f"       Lien internet: {self.product_substitute[4]}\n"
              f"       Marque       : {self.product_substitute[5]}\n"
              f"       Nutriscore   : {self.product_substitute[6].upper()}")
        return self.product_substitute

    def display_save_substitute(self):
        """suggest a save of the substitute."""

        authorised_answer_list, user_answer = ['Y', 'N'], None
        while user_answer not in authorised_answer_list:
            print(Fore.GREEN)
            user_answer = input(
                "\n       Souhaiteriez-vous sauvegarder cette proposition ?"
                " [Y/N] :").strip().upper()
            print(Fore.RESET)
        if user_answer == 'Y':
            temp_var = DataMgt()
            product_origin = self.product_origin
            product_substitute = self.product_substitute
            temp_var.save_substitute(product_origin, product_substitute)
            print(' \n       Sauvegarde effectuée avec succès! \n')
        elif user_answer == 'N':
            print("       OK! :)")

    def start(self):
        """Main loop of the application."""

        self.intro()
        while self.launched:
            self.category_choice()

    def favorites_display(self):
        """display favorites content order desc date."""

        temp_var1 = DataMgt()
        result_1 = temp_var1.get_all_favorites()
        if not result_1:
            print("       Vous n'avez pas encore d'enregistrement"
                  " dans vos favoris. ;)")
        else:
            print(Fore.YELLOW)
            print("       ----------------------------")
            print("        Consultations des favoris :")
            print("       ----------------------------\n")
            print(Fore.RESET)
            for line in result_1:
                print(f"       {line[0]} - Choix_initial  : {line[1]}"
                      f"  ({line[2].upper()})\n"
                      f"           Produit_suggéré: {line[5]} "
                      f"({line[6].upper()})  "
                      f"Date: {line[7].strftime('%Y-%m-%d %H:%M:%S'):>10}\n")

    def quit_message(self):
        """quit the app."""

        print(Fore.YELLOW)
        print("\n       ***  Merci pour l'utilisation de nos services."
              " A bientôt.  **** \n")
        print(Fore.RESET)
