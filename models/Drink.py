'''
@author: Keeth S.
@params: [
    json: dict
    sanitizer: util.Sanitizer.DrinkJsonSanitizer
    formatter: util.DrinkFormatter
    embedder: util.DrinkEmbeder
]
@desc: Creates a Drink Object used to embed an ice cold brew
'''
class Drink():


    def __init__(self, json, sanitizer, formatter, embedder):
        self._sanitizer = sanitizer(json)
        _json = self._sanitizer.clean_json()
        self._formatter = formatter(_json)
        self._img = _json.get('strDrinkThumb')
        self._name = _json.get('strDrink')
        self._category = _json.get('strCategory')
        self._alcoholic = _json.get('strAlcoholic')
        self._glass = _json.get('strGlass')
        self._ingredients_string = self._formatter.ingredients_string
        self._instructions = _json.get('strInstructions')
        self.embed = embedder(self).embed
        
        
    def __repr__(self):
        new_line='\n'
        tab = '\t'
        bracket = '{}'
        rerp_string = f'Drink{bracket[0]}{new_line}{tab}name: {self._name},{new_line}{tab}category: {self._category},{new_line}{tab}alcoholic: {self._alcoholic},'
        rerp_string += f'{new_line}{tab}glass: {self._glass},{new_line}{tab}ingredients: {self.ingredients__string},{new_line}{tab}instructions: {self._instructions},'
        rerp_string += f'{new_line}{tab}image: {self._img},{new_line}{tab}embed: {self.embed},{new_line}{tab}{new_line}{tab}sanitzier: {self._sanitizer},'
        rerp_string += f'{new_line}{tab}{new_line}{tab}formatter: {self._formatter},{new_line}{tab}{bracket[1]}'  
        return rerp_string 