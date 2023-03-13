import requests
import logging

from program.config import MAP_API_KEY


logger = logging.getLogger("uvicorn")

class Search_map(object):

    def __init__(self):
        self.api_key = MAP_API_KEY
        self.latitude = None
        self.longitude = None
        self.keyword = None
        self.radius = None
        
    def __set_latitude(self, latitude):
        self.latitude = str(latitude)
    def __set_longitude(self, longitude):
        self.longitude = str(longitude)

    def set_coordinates(self, latitude, longnitude):
        self.__set_latitude(latitude)
        self.__set_longitude(longnitude)        

    def set_radius(self, radius):
        self.radius = str(radius)
    
    def set_keyword(self, keyword):
        self.keyword = str(keyword)

    def get_result(self):

        if None not in [self.latitude, self.longitude, self.keyword, self.radius]:

            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}%2C{}&radius={}&keyword={}&key={}&opennow=true&language=zh-TW".format(
                self.latitude, self.longitude, self.radius, self.keyword, self.api_key
            )
            response = requests.request("GET", url)

            return response.text
    
