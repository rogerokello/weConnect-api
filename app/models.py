from .db import businesses

class Business(): 
    #initialise business   
    def __init__(self, name, category, location):
        """Initialize the business with an name, category and location."""
        self.name = name
        self.category = category
        self.location = location

    #Create a class method to add the business
    @classmethod
    def add(self, business):
        businesses.append(business)