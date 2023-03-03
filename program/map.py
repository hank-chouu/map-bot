import requests
import logging

from program.config import MAP_API_KEY


logger = logging.getLogger("uvicorn")

class Search_map(object):

    def __init__(self):
        self.api_key = MAP_API_KEY
        
    def __set_latitude(self, latitude):
        self.latitude = str(latitude)
    def __set_longitude(self, longitude):
        self.longitude = str(longitude)

    def set_coordinates(self, latitude, longnitude):
        self.__set_latitude(latitude)
        self.__set_longitude(longnitude)
        

    def set_radius(self, radius):
        self.radius = str(radius)
    
    def set_type(self, location_type):
        self.type = str(location_type)

    def get_result(self):

        attrs = ['latitude', 'longitude', 'type', 'radius']
        if all(hasattr(self, attr) for attr in attrs):

            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}%2C{}&radius={}&type={}&key={}&opennow=true&language=zh-TW".format(
                self.latitude, self.longitude, self.radius, self.type, self.api_key
            )
            response = requests.request("GET", url)

            return response.text
    
