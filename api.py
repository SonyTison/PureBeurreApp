#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module manage the request of the OpenFoodFact API."""

import requests

from settings import param_categories, NBR_PRODUCT_PER_PAGE, URL


class Api:
    """Download a list of products from the OpenFoodfacts API."""

    def __init__(self):
        self.api_result = []

    def load_data(self):
        """Retrieve products from API OpenFoodfacts by Category."""

        print("Importation des produits...")
        # -tc- Attention, ce n'est pas comme ça qu'on parcours une liste
        # -tc- for category in param_categories
        for i in range(len(param_categories)):
            payload = {
                'action': 'process',
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': param_categories[i],
                'sort_by': 'unique_scans_n',
                'countries': 'France',
                'page_size': str(NBR_PRODUCT_PER_PAGE),
                'json': True
            }
            response = requests.get(URL, params=payload)  # API request
            # -tc- gérer les erreurs réseau + status différents de 200

            # -tc- append() ajoute une liste à ta liste. C'est ce que tu veux ?
   
            # -tc- Je ferais personnellement un return plutôt que de créer un attribut
            self.api_result.append(response.json())  # answer stored in a list
