#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module manage the uploading of the cleaned data in MySQL."""

import mysql.connector

from database_xchange.config import info_bdd
from settings import param_categories

# -tc- A quoi servent tes managers si tu ne t'en sert pas
# -tc- pour l'insertion des données ?

class Upload:
    """This class will populate the DB with cleaned data from the module
    parsecleaner."""

    def __init__(self, product_list):
        # -tc- pourquoi une nouvelle connexion? Tu t'est déjà connecté
        # -tc- dans database.py. Récupérer cette connexion.
        self.my_database = mysql.connector.connect(**info_bdd)
        self.my_cursor = self.my_database.cursor()
        self.product_list = product_list

    def load_category(self):
        """Load data in Categories TABLE."""

        # -tc- ce ne sont pas ces categories que tu veux enregistrer
        # -tc- en base, mais les catégories des produits

        # -tc- for category in param_categories
        for i in range(len(param_categories)):
            cat = (param_categories[i]).title()
            # -tc- si tu enregistre les catégories des produits, il faut faire attention aux doublons
            self.my_cursor.execute(
                "INSERT INTO Categories (name) VALUES (%s)", (cat,))
            self.my_database.commit()
        self.my_cursor.close()
        # -tc- attention à ne pas toujours ouvrir et fermer une connexion
        self.my_database.close()

    def load_products(self):
        """Load data in Products TABLE."""

        self.my_database = mysql.connector.connect(**info_bdd)
        self.my_cursor = self.my_database.cursor()
        # -tc- revoir l'usage de for avec les listes

        # -tc- la structure de la base ne me semble pas afapté aux besoins du projet.
        # -tc- On ne peut stocker stores dans une colonne de la table Products.
        # -tc- Un produit devrait contenir plusieurs categories
        for i in range(len(self.product_list)):
            query = ('INSERT INTO Products '
                     '(name, brand, description, nutriscore, store, url,'
                     ' id_category) '
                     'VALUES (%(product_name)s, %(brands)s, '
                     '%(generic_name)s, %(nutriscore_grade)s, '
                     # -tc- D'oû vient id_category ?
                     '%(stores)s, %(url)s, %(id_category)s)')
            data = self.product_list[i]
            self.my_cursor.execute(query, data)
            self.my_database.commit()
        self.my_cursor.close()
        self.my_database.close()
        print('Database updated. Ready to be used...')
