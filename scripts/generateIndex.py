#!/usr/bin/env python3
import os
from datetime import datetime
import re
from pprint import pprint
from lark import Lark

index_header = '''# Recipes

A collection of recipes. Food is good, more coming soon.
'''

index_footer = '''
'''

with open('scripts/format.lark') as f:
    parser = Lark(f.read())

def get_recipe_name(file_path):
    with open(file_path, 'r') as recipe_file:
        for line in recipe_file.readlines():
            line = line.strip()
            if line[0] == '#':
                return line[1:].strip()

def get_ingredients(file_path):
    # Ingredients will be in the middle column of the table
    with open(file_path, 'r') as recipe_file:
        # Make a regex to find all three column tables
        r = re.compile(r'\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|')
        return [i[1] for i in r.findall(recipe_file.read())[2:]]

def check_format(file_path):
    with open(file_path) as recipe_file:
        try:
            parser.parse(recipe_file.read())
            return True
        except Exception as e:
            return False

if __name__ == "__main__":

    with open(os.path.join('recipes/index.md'), 'w') as f:
        print(index_header, file=f)

        for i in sorted(os.listdir('recipes')):
            # We don't need to include the index in the recipes
            full_path = os.path.join('recipes', i)

            if os.path.isdir(full_path):
                recipes = sorted((get_recipe_name(os.path.join(full_path, j)), os.path.join(i, j)) for j in os.listdir(full_path))

                if recipes:
                    print(f'\n## {i.replace("_", " ").title()}\n', file=f)

                    for j in recipes:
                        ingredients = get_ingredients(os.path.join('recipes', j[1])) 
                        classes = ' '.join(i.lower().replace(' ', '-') for i in ingredients)
                        valid_format = check_format(os.path.join('recipes', j[1]))
                        entry_string = f'- <span class="recipe-link {classes}"> [{j[0]}]({j[1]}) - <small>[\[PDF\]](pdf/{j[1].replace(".md", ".pdf")})</small> {"" if valid_format else "<small>! syntax error</small>"} </span>'
                        print(entry_string, file=f)


        print(f'\n<small>Auto-generated from [the source](https://github.com/tux2603/recipes) at {datetime.now().strftime("%d/%m/%Y %H:%M:%S")} UTC</small>\n', file=f)

        print(index_footer, file=f)
