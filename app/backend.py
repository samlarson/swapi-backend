from flask import Flask
from flask import jsonify
from app import api_functions
from flask_caching import Cache

# Configuration for caching capabilities
config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 3600
}

# Declaration of flask application and cache
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


# Base route, with a debug message to confirm from the CLI/browser that the app is running
@app.route('/')
def app_root():
    return 'SWAPI application is online. Try using a supported endpoint.'


# Endpoint to GET all films, which returns a JSON object of film data from SWAPI
@app.route('/films', methods=['GET'])
@cache.cached(timeout=3600)
def get_films():
    call = api_functions.APICall()
    return jsonify(call.get_films())


# Endpoint to POST a film ID, which returns a JSON object of character data from SWAPI
@app.route('/characters/<film_id>', methods=['POST'])
@cache.cached(timeout=3600)
def post_characters(film_id):
    call = api_functions.APICall()
    return jsonify(call.post_chars(film_id=int(film_id)))
