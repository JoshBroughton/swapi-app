'''
A Flask server providing an interface for interacting with the SWAPI
Star Wars API. Specifically, allows the user to search for information
about their favourite Star Wars characters.
'''
import json


from flask import Flask, request, render_template
import requests

app = Flask(__name__)
API_URL = 'https://swapi.py4e.com/api/people/'

@app.route('/')
def homepage():
    '''A homepage which links to the character form'''
    return render_template('home.html')



@app.route('/character')
def character_search():
    #I used requests.get and a for loop to build this, but didn't want to make 90 API
    #calls every time the page was reloaded so I just saved the dictionary here. 
    names = {1: 'Luke Skywalker', 2: 'C-3PO', 3: 'R2-D2', 4: 'Darth Vader', 5: 'Leia Organa', 6: 'Owen Lars', 7: 'Beru Whitesun lars', 8: 'R5-D4', 9: 'Biggs Darklighter', 10: 'Obi-Wan Kenobi', 11: 'Anakin Skywalker', 12: 'Wilhuff Tarkin', 13: 'Chewbacca', 14: 'Han Solo', 15: 'Greedo', 16: 'Jabba Desilijic Tiure', 18: 'Wedge Antilles', 19: 'Jek Tono Porkins', 20: 'Yoda', 21: 'Palpatine', 22: 'Boba Fett', 23: 'IG-88', 24: 'Bossk', 25: 'Lando Calrissian', 26: 'Lobot', 27: 'Ackbar', 28: 'Mon Mothma', 29: 'Arvel Crynyd', 30: 'Wicket Systri Warrick', 31: 'Nien Nunb', 32: 'Qui-Gon Jinn', 33: 'Nute Gunray', 34: 'Finis Valorum', 35: 'Padmé Amidala', 36: 'Jar Jar Binks', 37: 'Roos Tarpals', 38: 'Rugor Nass', 39: 'Ric Olié', 40: 'Watto', 41: 'Sebulba', 42: 'Quarsh Panaka', 43: 'Shmi Skywalker', 44: 'Darth Maul', 45: 'Bib Fortuna', 46: 'Ayla Secura', 47: 'Ratts Tyerel', 48: 'Dud Bolt', 49: 'Gasgano', 50: 'Ben Quadinaros', 51: 'Mace Windu', 52: 'Ki-Adi-Mundi', 53: 'Kit Fisto', 54: 'Eeth Koth', 55: 'Adi Gallia', 56: 'Saesee Tiin', 57: 'Yarael Poof', 58: 'Plo Koon', 59: 'Mas Amedda', 60: 'Gregar Typho', 61: 'Cordé', 62: 'Cliegg Lars', 63: 'Poggle the Lesser', 64: 'Luminara Unduli', 65: 'Barriss Offee', 66: 'Dormé', 67: 'Dooku', 68: 'Bail Prestor Organa', 69: 'Jango Fett', 70: 'Zam Wesell', 71: 'Dexter Jettster', 72: 'Lama Su', 73: 'Taun We', 74: 'Jocasta Nu', 75: 'R4-P17', 76: 'Wat Tambor', 77: 'San Hill', 78: 'Shaak Ti', 79: 'Grievous', 80: 'Tarfful', 81: 'Raymus Antilles', 82: 'Sly Moore', 83: 'Tion Medon', 84: 'Finn', 85: 'Rey', 86: 'Poe Dameron', 87: 'BB8'}
    character_id = request.args.get('id_input')
    context = {'names': names}
    if character_id:
        search_url = API_URL + character_id
        response = requests.get(search_url, timeout=5.0)
        if response.status_code == 404:
            context = {
                'error': f'Character ID "{character_id}" does not exist'
            }
        else:
            char_obj = json.loads(response.content)

            homeworld_url = char_obj['homeworld']
            response = requests.get(homeworld_url, timeout=5.0)
            homeworld_obj = json.loads(response.content)

            film_list = char_obj['films']
            film_names = []

            for film_url in film_list:
                response = requests.get(film_url, timeout=5.0)
                content = json.loads(response.content)
                film_names.append(content['title'])

            context = {
                'char_obj': char_obj,
                'homeworld_obj': homeworld_obj,
                'film_names': film_names,
                'names': names,
            }

        return render_template('character.html', **context)
    return render_template('character.html', **context)

    



if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)