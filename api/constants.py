from os import path

BASE_DIR = path.os.path.dirname(__file__)

DEFAULT_CILY = 'Odessa, Odessa Oblast, Ukraine'

BASE_URL = 'https://maps.googleapis.com/maps/api/'
AUTOCOMPLETE_URL = BASE_URL + 'place/autocomplete/json'
PLACES_URL = BASE_URL + 'place/findplacefromtext/json'
GEOCODING_URL = BASE_URL + 'geocode/json'

COUNTRY_CODES_FILE = BASE_DIR + '/country_codes.csv'
CITY_ID_FILE = BASE_DIR + '/city.list.json'
DELIMITER = ';'
NEWLINE = ''
READ = 'r'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
