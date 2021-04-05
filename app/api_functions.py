import json
import requests
# from pprint import pprint


# Given a film (episode) ID, return the integer that corresponds to its API call
def match_film_id(film_id: int) -> int:
    film_map = {1: 4, 2: 5, 3: 6, 4: 1, 5: 2, 6: 3}
    return film_map[film_id]


class APICall:
    # Given an API endpoint, return the JSON object
    @staticmethod
    def dump_json(url: str) -> str:
        req = requests.get(url=url)
        return req.json()

    # Return JSON object containing attributes for every film
    def get_films(self) -> str:
        output_list = []
        films = self.dump_json(url='https://swapi.dev/api/films/')
        results = films['results']
        # Iterate through each film to retrieve attributes, and append to the final list
        for film in results:
            film_dict = {}
            film_id, film_title, film_release = film['episode_id'], film['title'], film['release_date']
            film_dict['id'], film_dict['title'], film_dict['release_date'] = film_id, film_title, film_release
            output_list.append(film_dict)
        # Return formatted list of film attributes (list of dictionaries, to be deserialized by jsonify in backend.py)
        return output_list

    # Given a list of character endpoints, return JSON object of those characters' names and IDs
    def get_film_chars(self, char_list: list) -> str:
        output_list = []
        # Iterate through each character endpoint for the given film
        for item in char_list:
            char_dict = {}
            char_data = self.dump_json(url=item)
            # Retrieve the character ID and name from the API response, append in dict format to the final list
            char_name, char_id = char_data['name'], char_data['url'].split("/")[::-1][1]
            char_dict['name'], char_dict['id'] = char_name, char_id
            output_list.append(char_dict)
        # Return formatted list of characters (list of dictionaries, to be deserialized by jsonify in backend.py)
        return output_list

    # Given an episode ID, return an object (list of dictionaries) of those characters' names and IDs
    def post_chars(self, film_id: int) -> str:
        api_id = match_film_id(film_id=film_id)
        film_url = "https://swapi.dev/api/films/" + str(api_id)
        film_data = self.dump_json(url=film_url)
        char_list = film_data['characters']
        char_json = self.get_film_chars(char_list=char_list)
        return char_json
