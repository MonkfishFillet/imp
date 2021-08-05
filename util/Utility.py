import json
import requests    
from discord import Embed
from enum import Enum

#region Configuration
'''
@author: Keeth S.
@desc: Parent Configuration object used to store the config file
'''
class Configurable():
    def __init__(self):
        self._file = self._get_config_file()
    
    def _get_config_file(self):
        CFG_FILENAME = './config.json'
        with open(CFG_FILENAME) as cfg:
            CFG = json.load(cfg)
        return CFG
#endregion

#region Request
'''
@author: Keeth S.
@parms: requests: requests module object
@desc: Object used to get resources outside of the config file
@TODO: Move urls to config file / Make url entries into attributes /
        Abstract Request as Parent classs(?)
'''
class Request:
    def __init__(self):
        self._requests = requests
        self.urls = {
            "cocktail_db_api": 'https://www.thecocktaildb.com/api/json/v1/1/random.php',
            "battle_music": 'https://www.youtube.com/watch?v=lAGm9MTyRJ8'
        }
    
    def get_drink_json(self):
        return self._requests.get(self.urls['cocktail_db_api']).json()['drinks'][0]

    def get_url(self, url_name):
        return self.urls[url_name]
#endregion

#region Formatter
'''
@author: Keeth S.
@params: arg: Object passed in to be formatted
@desc: Parent Formatter Class
'''
class Formatter():
    
    def __init__(self, arg):
        self.arg = arg


    def get_filth_type(self):
        return f'Type: {str(type(self.arg))}'


'''
@author: Keeth S.
@params: json: dict
@desc: Drink Formatter which formats the ingredient's
        and measurments of a drink
'''
class DrinkFormatter(Formatter):

    def __init__(self, json: dict):
        if(isinstance(json, dict) != True):
            raise TypeError('The argument must be of type dict')
        Formatter.__init__(self, json)
        self.ingredients_string = self.make_ingredients_string(self.arg)

    def make_ingredients_string(self, json):
        ingredients = [json.get(ing) for ing in json if 'Ingredient' in ing and json.get(ing) is not None]
        measurements = [json.get(measure) for measure in json if 'Measure' in measure and json.get(measure) is not None]
        
        if(len(measurements) == 0):
            return ingredients
        
        ingredient_list = []
        for i in range(len(ingredients)):
            if(i < len(measurements)):
                ingredient_list.append(measurements[i].strip() + " " + ingredients[i])
            elif(ingredients[i] == ' '):
                pass
            else:
                ingredient_list.append(ingredients[i])
        return ingredient_list
#endregion

#region Embedder
'''
@author: Keeth S.
@params: drink: Drink object to be embedded
@desc: Embedder which creates and sets an embed with
        information from the Drink object
'''
class DrinkEmbedder():

    def __init__(self, drink):
        self.drink = drink
        embed = Embed(title=self.drink._name, description='A drink for you, good Bud.', color=Colors().dark_navy)
        self.embed = self.embed_drink(embed)
        
    def embed_drink(self, embed):
        embed.set_image(url=self.drink._img)
        embed.add_field(name="Name", value=self.drink._name)
        embed.add_field(name="Category", value=self.drink._category)
        embed.add_field(name="\u200b", value='\u200b')
        embed.add_field(name="Alcoholic?", value=self.drink._alcoholic)
        embed.add_field(name="Glass Type", value=self.drink._glass)
        embed.add_field(name="\u200b", value='\u200b')
        ingredient_string = ""
        for string in self.drink._ingredients_string:
            ingredient_string += string + '\n'
        embed.add_field(name="Ingredients", value=ingredient_string, inline=False)
        embed.add_field(name="Instructions", value=self.drink._instructions, inline=False)
        embed.set_footer(text="Have ideas for additional functionality? Throw them in #robbot_discussion!")
        return embed


'''
@author: Keeth S.
@params: pin: Pin object to be embedded
@desc: Embedder which creates and sets an embed with
        information from the Pin object
'''
class PinEmbedder():
    def __init__(self, pin):
        self.pin = pin
        embed = Embed(title=self.pin.author, description=f'Posted on {self.pin.posted_date}', color=int(Colors().user_colors.get_user_color(self.pin.id)))
        self.embed = self.embed_pin(embed)

    def embed_pin(self, embed):
        pin_embed = embed
        pin_embed.set_thumbnail(url=self.pin.avatar)
        pin_embed.add_field(name="Channel", value=self.pin.channel, inline=False)
        if(self.pin.image is not None):
            pin_embed.set_image(url=self.pin.image)
        if(self.pin.content is not None):
            pin_embed.add_field(name="Message", value=f'[{self.pin.content}]({self.pin.url})', inline=False)
        else:
            pin_embed.add_field(name="Message", value='*This pin had no message*', inline=False)
        return pin_embed
#endregion

#region Sanitizers
'''
@author: Keeth S.
@params: filth: Object which needs to be sanitized
@desc: Parent Sanitizer Class
'''
class Sanitizer:
    
    def __init__(self, filth):
        self.filth = filth


'''
@author: Keeth S.
@params: json: dict
@desc: Drink Sanitizer which returns a sanitized version of the drink 
        json passed into it
'''
class DrinkJsonSanitizer(Sanitizer):
    

    def __init__(self, json: dict):
        Sanitizer.__init__(self, json)
    

    def clean_json(self):
        drink_dict = {}
        for key in self.filth:
            if(self.filth[key] != None):
                drink_dict[key] = self.filth[key]  

        return drink_dict
#endregion

#region Colors
'''
@author: Keeth S.
@desc: Configuration Child Object which stores the color values for each 
        user in the server
'''
class UserColors(Configurable):
    def __init__(self):
        Configurable.__init__(self)
        self._user_color_list = self._get_user_color_list()
        self.brady = self._user_color_list['Brady']
        self.carlie = self._user_color_list['Carlie']
        self.derick = self._user_color_list['Derick']
        self.keeth = self._user_color_list['Keeth']
        self.james = self._user_color_list['James']
        self.rob = self._user_color_list['Rob']
        self.robbot = self._user_color_list['Robbot']
    
    def _get_user_color_list(self):
        user_color_list = {}
        
        for guid, obj in self._file['users'].items():
            user_color_list[obj['name']] = obj['embed_color']
        return user_color_list
    
    def get_user_color(self, guid: str):
        if guid is not None:
            guid = str(guid)
            
        __user_list = self._file['users']
        if guid in __user_list:
            return __user_list[guid]['embed_color']


'''
@author: Keeth S.
@desc: Configuration Child which stores the values of 
        colors which can be accessed globally.
'''
class Colors(Configurable):
    def __init__(self):
        Configurable.__init__(self)
        self.user_colors = UserColors()
        self._color_list = self._file['colors']
        self.aqua = self._get_color('AQUA')
        self.green = self._get_color('GREEN')
        self.blue = self._get_color('BLUE')
        self.purple = self._get_color('PURPLE')
        self.gold = self._get_color('GOLD')
        self.orange = self._get_color('ORANGE')
        self.red = self._get_color('RED')
        self.grey = self._get_color('GREY')
        self.light_grey = self._get_color('LIGHT_GREY')
        self.navy = self._get_color('NAVY')
        self.dark_aqua = self._get_color('DARK_AQUA')
        self.dark_green = self._get_color('DARK_GREEN')
        self.dark_blue = self._get_color('DARK_BLUE')
        self.dark_purple = self._get_color('DARK_PURPLE')
        self.dark_gold = self._get_color('DARK_GOLD')
        self.dark_orange = self._get_color('DARK_ORANGE')
        self.dark_red = self._get_color('DARK_RED')
        self.dark_grey = self._get_color('DARK_GREY')
        self.darker_grey = self._get_color('DARKER_GREY')
        self.dark_navy = self._get_color('DARK_NAVY')
        self.vivid_pink = self._get_color('LUMINOUS_VIVID_PINK')
        self.dark_vivd_pink = self._get_color('DARK_VIVID_PINK')

    def _get_color(self, color):
        return self._color_list[color]
#endregion

#region Channels
'''
@author: Keeth S.
@desc: Enum of all channel ids
'''
class Channels(Enum):
        AnNNOUNCEMENTS = 834465768703787079
        GENERAL = 834465065234726945
        MAPS = 834471436538216448
        FIGURES = 834471455789416499
        IDEAS = 834473748441595905
        CONCERNS = 834473790683218000
        MUSIC_STAGE = 834485620843085884
        THE_BAR = 834465065234726946
        THE_BACK_ROOMS = 834473457504616458
        SHIT_POST_ALLEY = 834469160045248534
        DM_SCREENS = 872602011512733737
        DM_RESOURCES = 872916292804440146
        BOT_TESTING = 872604886984958022
#endregion