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

    #Method to check if a business ID exists
    @classmethod
    def id_exists(self, business_id = None):
        try:
            businesses[int(business_id)]
        except IndexError:
            return False

        try:
            businesses[int(business_id)]
        except ValueError:
            return False

        return True

    #Method to get biz by id
    @classmethod
    def get_by_id(self, id):
        return businesses[id]

    #Method to delete a biz by id
    @classmethod
    def delete(self, id=None):
        if id is not None:
            businesses.pop(int(id))
            return id
        else:
            return None

    #Method to update a business given its id
    @classmethod
    def update(self, id, name, category, location):
        if self.id_exists(id):
            business_to_update = self.get_by_id(id)
            business_to_update.name = name
            business_to_update.category = category
            business_to_update.location = location
            return True
        else:
            return False