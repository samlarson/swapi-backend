import os
import sys
import json
import time
import pytest
import warnings

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import API functions and flask application object from backend
import api_functions
from backend import app
# Supress deprecation warnings from pytest
warnings.simplefilter("error", DeprecationWarning)


# Test that the flask app returns a 200 OK HTTP status code, with the debug statement in the body
def test_status():
    response = app.test_client().get('/')

    print("\nTesting Flask Application Status...")
    print("Flask App Status Code: " + str(response.status_code))
    print("Flask App Response: \n" + str(response.data))

    assert response.status_code == 200
    assert response.data == b'SWAPI application is online. Try using a supported endpoint.'


# Test that the flask endpoint for films returns OK and has the specified fields in the first film entry
def test_films():
    response = app.test_client().get('/films')

    print("\nTesting Films API Call...")
    print("Films API Call Status Code: " + str(response.status_code))
    print("Films API Call Response: \n" + str(response.data))

    json_data = json.loads(response.data)
    first_item = json_data[0]
    assert response.status_code == 200
    assert 'id' in first_item
    assert 'title' in first_item
    assert 'release_date' in first_item


# Tests that the flask endpoint for characters returns OK and has the specified fields in the first character entry
# Tests that a given character response is cached by the app (by comparing elapsed time)
def test_characters():
    start_time = time.time()
    response = app.test_client().post('/characters/1')
    print("\nTesting Characters API Call...")
    print("Characters API Call Status Code: " + str(response.status_code))
    print("Characters API Call Response: \n" + str(response.data))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("(POST 1) Elapsed Time: " + str(elapsed_time) + " seconds")

    json_data = json.loads(response.data)
    first_item = json_data[0]
    assert response.status_code == 200
    assert 'id' in first_item
    assert 'name' in first_item

    start_time = time.time()
    cached_response = app.test_client().post('/characters/1')
    end_time = time.time()
    cached_elapsed_time = end_time - start_time
    print("(POST 2) Elapsed Time: " + str(cached_elapsed_time) + " seconds")

    assert elapsed_time > (cached_elapsed_time * 100)


# Tests that the flask endpoint for characters returns a KeyError from api_functions.match_film_id() for invalid films
def test_invalid_characters():
    print("\nTesting Invalid Characters API Call...")

    with pytest.raises(KeyError) as e:
        response = app.test_client().post('/characters/9999')

    assert e.value.args[0] == 9999


# Tests that the SWAPI endpoint for characters returns a 'not found' message for invalid characters
def test_invalid_swapi_characters():
    print("\nTesting Invalid Characters SWAPI Call...")

    response = api_functions.APICall.dump_json(url='https://swapi.dev/api/people/9999/')
    print(response)

    assert response['detail'] == "Not found"


# Tests that the SWAPI endpoint for films returns an object in the expected format
def test_swapi_films():
    response = api_functions.APICall.dump_json(url='https://swapi.dev/api/films/')
    first_item = response['results'][0]

    print("\nTesting SWAPI Films Call...")
    print("Films SWAPI Call Response: \n" + str(response))

    assert 'results' in response
    assert 'episode_id' in first_item


# Tests that the SWAPI endpoint for characters returns an object in the expected format
def test_swapi_characters():
    response = api_functions.APICall.dump_json(url='https://swapi.dev/api/people/1')

    print("\nTesting SWAPI People Call...")
    print("Films SWAPI Call Response: \n" + str(response))

    assert 'name' in response
    assert 'url' in response
