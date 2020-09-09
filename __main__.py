#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Purebeurre Application 'MyFoodApp' The Aim of this application is to
suggest a healthiest food than the original choice of a user.

Script Python
Files: settings.py, __main__.py, api.py, config.py, managers.py,
parsecleaner.py, upload.py, view.py
"""

# -tc- si à la racine du projet, renommer main.py

from api import Api
from parsecleaner import Parser
from upload import Upload
from managers import DataMgt
from view import App


def main():
    """Method to launch the app."""

    content = DataMgt()
    if not content.is_database_empty():  # check content of table Product
        api = Api()
        api.load_data()  # if yes, launch api request
        liste = Parser(api.api_result)  # parse api result
        liste.clean()  # clean api result
        data = Upload(liste.products_list)
        data.load_category()  # upload table categories content
        data.load_products()  # upload table products content
    session = App()
    session.start()  # launch the client app


if __name__ == '__main__':
    main()
