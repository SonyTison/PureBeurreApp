#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module manage....................."""

from database_xchange.database import db # db = my_database with mysql-connector

from database_xchange.managers import CategoryManager, ProductManager, FavoriteManager


class Category:

    # -tc- pas nécessaire si on veut simplifier les imports
    objects = CategoryManager(db)
    
    # -tc- Pourquoi l'id de la catégorie est à None ? Ajouer
    # -tc- id_category à la liste des paramètres.
    def __init__(self, name=None, products=None):
        self.id_category = None
        self.name = name
        self.products = products

class Product:
    
    # -tc- pour simplifier, enlever
    objects = ProductManager(db)

    # -tc- ajouter l'id aux paramètres. Il ne vaut pas toujours None
    def __init__(self,
                 name=None,
                 description=None,
                 nutriscore=None,
                 url=None,
                 store=None,
                 categories=None,
                 ):
        self.id_product = None
        self.name = name
        self.description = description
        self.nutriscore = nutriscore
        self.url = url
        self.store = store
        self.categories = categories

class Favorite:

    # -tc- pour simplifier, enlever
    objects = FavoriteManager(db)

    # -tc- ajouter l'id aux paramètres, il ne vaut pas toujours None
    def __init__(self,
                 id_product_origin=None,
                 id_product_substitute=None, 
                 request_date=None
                 ):
        self.id_favorite = None
        self.id_product_origin = id_product_origin
        self.id_product_substitute = id_product_substitute
        self.request_date = request_date
