import requests
import urllib.parse as urllib
import csv
import json
from .constants import *
from .api_keys import *


class GoogleAPI():

    # ===== PUBLIC METHODS =====

    def get_locations_by_input(self, user_input):
        safe_input = self._make_url_safe(user_input)
        params = {
            'input': safe_input,
            'types': '(cities)',
            'key': GOOGLE_API_KEY}
        response = self._get_json_from_request(AUTOCOMPLETE_URL, params)
        return self._get_suggestions_from_json(response)


    # ===== PROTECTED METHODS =====

    def _make_url_safe(self, text):
        no_spaces = ''.join([char for char in text if char != ' '])
        return urllib.quote(no_spaces)


    def _get_json_from_request(self, url, params):
        response = requests.get(url, params)
        return response.json()


    def _get_suggestions_from_json(self, json_file):
        suggestions = []
        for item in json_file['predictions']:
            suggestions.append(item['description'])
        return suggestions


class WeatherAPI():

    # ===== PUBLIC METHODS =====

    def get_weather_by_city(self, city, country):
        country_code = self._get_country_code(country)
        city_id = self._get_city_id(city, country_code)
        if city_id:
            params = {
                'id': city_id,
                'APPID': WEATHER_API_KEY}
        else:
            params = {
                'q': f'{city},{country_code}',
                'APPID': WEATHER_API_KEY}
        weather = self._get_weather_from_request(WEATHER_URL, params)
        return weather


    # ===== PROTECTED METHODS =====

    def _get_weather_from_request(self, url, params):
        response = requests.get(url, params)
        weather = response.json()['weather'][0]['main']
        return weather


    def _get_country_code(self, city):
        with open(COUNTRY_CODES_FILE, READ,
                  newline=NEWLINE) as csv_file:
            reader = csv.DictReader(
                csv_file, delimiter=DELIMITER)
            result = [line for line in reader if city.upper() in line.values()]
            return result[0]['country_code'] if result else None


    def _get_city_id(self, city, country_code):
        with open(CITY_ID_FILE, READ) as file:
            cities_list = json.load(file)
            for entry in cities_list:
                if entry['name'] == city and entry['country'] == country_code:
                    return entry['id']
