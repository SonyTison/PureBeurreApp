#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module manage the data receive from the api (parse and clean)."""

import re

from settings import NBR_PRODUCT_PER_PAGE, param_categories, fields


class Parser:
    """process the data retrieve from the API openfoodfact."""

    def __init__(self, api_result):
        self.api_result = api_result
        self.products_list = []  # list of all the cleaned product

    def clean(self):
        """clean, filter and valid the data from the api and return a list of product ready to be
        upload to purebeurre database."""

        for category in range(len(param_categories)):
            for num_product_per_category in range(NBR_PRODUCT_PER_PAGE):
                product = {}  # initialisation of a product as a dict
                product_completeness = True
                for i in range(len(fields)):
                    try:
                        # test if content
                        if (self.api_result[category]['products']
                                [num_product_per_category]
                                [fields[i]]) != "":
                            # if yes, remove whitespace
                            result = (
                                self.api_result[category]['products']
                                [num_product_per_category][fields[i]]).strip()
                            if isinstance(result, str):  # if result == str
                                # regex used to remove unwanted characters
                                result = re.sub(
                                    "[.,;\t\n\r\x0b\x0c]", '', result)
                                product.update({fields[i]: result})
                            product.update({fields[i]: (
                                self.api_result[category]['products']
                                [num_product_per_category][fields[i]]).strip()}
                                           )
                        else:
                            product_completeness = False
                            break
                    except KeyError:
                        product_completeness = False
                        break
                if product_completeness:
                    # add id_category field and value for the product
                    product.update({'id_category': (category + 1)})
                    self.products_list.append(product)
        return self.products_list
