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
    character_id = request.args.get('id_input')

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
            context = {
                'char_obj': char_obj,
                'homeworld_obj': homeworld_obj,
            }

        return render_template('character.html', **context)

    return render_template('character.html')



if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)