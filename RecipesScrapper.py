import requests
from bs4 import BeautifulSoup
import json

def get_recipe(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    recipe = {}

    # Recipe Title
    recipe['name'] = soup.find('h1', class_='headline').get_text(strip=True)

    # Ingredients
    ingredients = soup.find_all('span', class_='ingredients-item-name')
    recipe['ingredients'] = [i.get_text(strip=True) for i in ingredients]

    # Instructions
    steps = soup.find_all('li', class_='subcontainer instructions-section-item')
    recipe['instructions'] = [step.get_text(strip=True) for step in steps]

    # Dietary Tags (we'll just look for keywords)
    recipe['dietary_tags'] = []
    if 'vegan' in recipe['name'].lower(): recipe['dietary_tags'].append('vegan')
    if 'gluten' in recipe['name'].lower(): recipe['dietary_tags'].append('gluten-free')

    # Nutrition Info
    nutrition_section = soup.find('div', class_='nutrition-top')
    if nutrition_section:
        recipe['nutrition'] = nutrition_section.get_text(strip=True)
    else:
        recipe['nutrition'] = "Not Available"

    return recipe


url = "https://www.allrecipes.com/"
data = get_recipe(url)

with open('recipe_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
