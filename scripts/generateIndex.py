#!/usr/bin/env python3
import os
from datetime import datetime
import re
from pprint import pprint
from lark import Lark, Token
from dominate import document
from dominate.tags import *

class Recipe:

    with open('scripts/format.lark') as f:
        parser = Lark(f.read(), parser='lalr')

    def __init__(self, path):  # sourcery skip: path-read
        self.path = path
        
        # Open up the files for the recipe and the grammer
        with open(self.path) as f:
            data = f.read()

        # Parse the data
        try:
            self._tree = Recipe.parser.parse(data)
            self._syntax_valid = True
        except Exception as e:
            self._tree = None
            self._syntax_valid = False

        # print(self._tree)

    def get_name(self):
        if not self._syntax_valid:
            return self.path.split('/')[-1].split('.')[0]

        for i in self._tree.find_pred(lambda i: i.data == 'title'):
            name = ' '.join(i.scan_values(lambda i: isinstance(i, Token)))
        return name

    def get_ingredients(self):
        if not self._syntax_valid:
            return []
            
        ingredients = []
        for i in self._tree.find_pred(lambda i: i.data == 'ingredient_name'):
            ingredients.append(' '.join(i.scan_values(lambda i: isinstance(i, Token))).strip())
        return ingredients

    def get_tags(self):
        if not self._syntax_valid:
            return []

        tags = []
        for i in self._tree.find_pred(lambda i: i.data == 'tag'):
            tags.append(' '.join(i.scan_values(lambda i: isinstance(i, Token))).strip())
        return tags

    def is_valid(self):
        return self._syntax_valid

    def get_path(self):
        return os.path.sep + os.path.join(*(self.path.split('/')[1:]))



def to_tag(string):
    # remove anything in parentheses
    tag = re.sub(r'\([^)]*\)', '', string)
    tag = tag.replace('&', 'and')
    tag = tag.strip()
    tag = ''.join([c.lower() if c.isalnum() else '-' for c in tag])
    tag = re.sub(r'-+', '-', tag)

    return tag

if __name__ == "__main__":
    # First, find and parse all the recipes and build them into a list
    recipes = {}
    for i in os.listdir('recipes'):
        full_path = os.path.join('recipes', i)

        if os.path.isdir(full_path):
            recipes[i] = []

            for j in os.listdir(full_path):
                recipe_path = os.path.join(full_path, j)
                recipe = Recipe(recipe_path)
                recipes[i].append(recipe)

    doc = document(title='Index | Recipes')

    with doc.head:
        meta(charset='utf-8')
        meta(http_equiv='X-UA-Compatible', content='IE=edge')
        meta(name='viewport', content='width=device-width, initial-scale=1')

        meta(property='og:title', content='Recipes')
        meta(property='og:locale', content='en_US')
        meta(name='description', content='Food is good')
        meta(property='og:description', content='Food is good')
        link(rel='canonical', href='https://recipes.tux2603.me/')
        meta(property='og:url', content='https://recipes.tux2603.me/')
        meta(property='og:site_name', content='recipes')
        meta(property='og:type', content='website')
        meta(name='twitter:card', content='summary')
        meta(property='twitter:title', content='Recipes')

        link(rel='stylesheet', href='/assets/css/style.css?v=6f706bcd2c3d3c7c0c7cc57bb7b954adf9ad8ea2')

        script(src='/jquery-3.6.0.slim.min.js')
        script(src='/index.js')

    with doc:
        with div(cls='wrapper'):
            with header():
                h1().add(a('recipes', href='https://recipes.tux2603.me/'))
                p('Food is good')

                with p(cls='view'):
                    with a('View the Project on GitHub', href='https://github.com/tux2603/recipes'):
                        small('tux2603/recipes')

            with section():
                h1('Recipes', id='recipes')
                p('A collection of recipes. Food is good. More food coming soon')

                with section(cls='filters'):
                    # make two drop down for tags and ingredients
                    with select(id='tags', name='tags', multiple='multiple'):
                        option('All Tags', value='all', selected='selected')

                        tags = set()
                        for recipe_list in recipes.values():
                            for recipe in recipe_list:
                                tags.update((to_tag(i).replace('-', ' ').title() for i in recipe.get_tags()))
                        tags = sorted(list(tags), key=lambda i: to_tag(i))

                        for tag in tags:
                            option(tag, value=f'tag-{to_tag(tag)}')

                    with select(id='ingredients', name='ingredients', multiple='multiple'):
                        option('All Ingredients', value='all', selected='selected')

                        ingredients = set()
                        for recipe_list in recipes.values():
                            for recipe in recipe_list:
                                ingredients.update((to_tag(i).replace('-', ' ').title() for i in recipe.get_ingredients()))
                        ingredients = sorted(list(ingredients), key=lambda i: to_tag(i))

                        for ingredient in ingredients:
                            option(ingredient, value=f'ing-{to_tag(ingredient)}')


                for category, recipe_list in recipes.items():
                    with section(cls='recipe-section', id=category.replace('_', '-').lower()):
                        h2(category.replace('_', ' ').title())

                        with ul():
                            # sort the recipe list
                            recipe_list.sort(key=lambda i: i.get_name())

                            for recipe in recipe_list:
                                classes = ['recipe']
                                classes.extend([f'tag-{to_tag(i)}' for i in recipe.get_tags()])
                                classes.extend([f'ing-{to_tag(i)}' for i in recipe.get_ingredients()])
                                with li(cls=' '.join(classes)) as dom:
                                    a(recipe.get_name(), href=recipe.get_path().replace('.md', '.html'))
                                    small().add(a('[PDF]', href='/pdf' + recipe.get_path().replace('.md', '.pdf')))

                                    if not recipe.is_valid():
                                        small('syntax error recipe couldn\'t be scanned')

                with p().add(small()) as timestamp:
                    timestamp.add('Auto-generated from ')
                    timestamp.add(a('the source', href='https://github.com/tux2603/recipes'))
                    timestamp.add(f' at {datetime.now()}')

            with footer():
                with p() as dom:
                    dom.add('This project is maintained by ')
                    dom.add(a('tux2603', href='https://github.com/tux2603'))

                with p().add(small()) as dom:
                    dom.add('Hosted on GitHub Pages - Theme by')
                    dom.add(a('orderedlist', href='https://github.com/orderedlist'))

    with open('recipes/index.html', 'w') as f:
        print(doc.render(xhtml=True), file=f)