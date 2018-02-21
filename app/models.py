from .db import businesses, reviews, users

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

class Review():
    # create a review object
    def __init__(self, review_summary, review_description,
                star_rating, business_id):
        self.review_summary = review_summary
        self.review_description = review_description
        self.star_rating = star_rating
        self.business_id = business_id

    # add review object to database
    @classmethod
    def add(self, a_review):
        reviews.append(a_review)

    # return all reviews as a list of dictionary items
    # which you will return jsonify to return
    @classmethod
    def get_all_business_reviews(self, id):
        business_reviews = []
        for counter,one_review in enumerate(reviews):
            #check for reviews with same business id
            if int(one_review.business_id) == int(id):
                #dict to store review
                a_review = {
                    'review_summary' : one_review.review_summary,
                    'review_description' : one_review.review_description,
                    'star_rating': one_review.star_rating,
                    'business_id': one_review.business_id 
                }
                #attach what was found into business reviews
                business_reviews.append(a_review)
        #return an object you can easily jsonify when sending back
        return business_reviews

class User():
    # create user object
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logged_in = False
        self.active = True

    # method to add user to the datbase
    @classmethod
    def add(self, a_user):
        users.append(a_user)

    # method to find user by username
    @classmethod
    def get_by_username(self, username):
        for user in users:
            if user.username == username:
                return user

        return False
    
    #check if password is valid
    def check_password_is_valid(self, password):
        if self.password == password:
            return True
        else:
            return False

    #check if user already logged in
    def check_already_logged_in():
        if self.logged_in:
            return True
        else:
            return False
