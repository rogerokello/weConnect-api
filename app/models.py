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

    # return all businesses as a list of dictionary items
    # which you will return jsonify to return
    @classmethod
    def get_all(self):
        current_businesses = []
        for counter,business in enumerate(businesses):
            a_business = {
                'id' : counter,
                'name' : business.name,
                'category': business.category,
                'location': business.location 
            }
            current_businesses.append(a_business)
        
        return current_businesses