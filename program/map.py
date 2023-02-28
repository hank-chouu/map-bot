import requests
import logging

from program.config import MAP_API_KEY


logger = logging.getLogger("uvicorn")

class Search_map(object):

    def __init__(self):
        self.api_key = MAP_API_KEY
    def __set_longitude(self, longnitude):
        self.longnitude = str(longnitude)
    def __set_latitude(self, latitude):
        self.latitude = str(latitude)

    def set_coordinates(self, longnitude, latitude):
        self.__set_longitude(longnitude)
        self.__set_latitude(latitude)

    def set_radius(self, radius):
        self.radius = str(radius)
    
    def set_type(self, location_type):
        self.type = str(location_type)

    def get_result(self):

        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}%2C{}&radius={}&type={}&key={}&opennow=true".format(
            self.latitude, self.longnitude, self.radius, self.type, self.api_key
        )



        response = requests.request("GET", url)

        return response.text
    
Search = Search_map()