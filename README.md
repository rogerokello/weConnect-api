[![Build Status](https://travis-ci.org/rogerokello/weconnect-practice.svg?branch=dev-v3-trial)](https://travis-ci.org/rogerokello/weconnect-practice) <a href='https://coveralls.io/github/rogerokello/weconnect-practice?branch=dev-v3-trial'><img src='https://coveralls.io/repos/github/rogerokello/weconnect-practice/badge.svg?branch=dev-v3-trial' alt='Coverage Status' /></a>
 <a href="https://codeclimate.com/github/rogerokello/weconnect-practice/maintainability"><img src="https://api.codeclimate.com/v1/badges/203bec3842f23583461b/maintainability" /></a>
</br>
# weconnect api
An api to enable you manage your business and reviews. Please visit a prototype at https://rogerokello.github.io/weconnect-practice/

## How to run the flask application
1. Create a folder weconnect on your computer
   
2. Clone the app to your folder by issuing this command

    ```
        $ git clone -b dev-v4 https://github.com/rogerokello/weconnect-practice.git
    ```
    NB: Read these resources to install git: https://git-scm.com/downloads
3. Navigate into cloned folder

    ```
        $ cd weconnect-practice
    ```
4. Create and activate  virtual environment.

    ```
        $ virtualenv  venv

        $ source venv/bin/activate
    ```

    More on setting up Virtual environment: [how to set up virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

5. Install the packages in requirements.txt
   While at your prompt initiate the following command

    ``` $ pip install -r requirements.txt ```

6. Run your app from the terminal like this

    ```
        $ python run.py
    ```

7. Using postman, the url to run the api locally is ```http://127.0.0.1:5000/```.

8. You may use postman to use the following endpoints of the api locally.
-  POST /api/auth/register        # This registers a new user
-  POST /api/auth/login           # This logins an already registered user
-  POST /api/auth/logout          # This logs out a user
-  POST /api/auth/reset-password  # This changes the password of a user
-  POST /api/businesses           # This registers a new business
-  PUT /api/businesses/<businessId> # This updates a business profile
-  DELETE /api/businesses/<businessId> # This removes a business
-  GET /api/api/businesses             # This gets all the existing businesses
-  GET /api/businesses/<businessId> # This gets a business
-  POST /api/businesses/<businessId>/reviews # This makes a review for a review
-  GET /api/businesses/<businessId>/reviews # This gets the reviews that belong to a business
-  GET /api/businesses/search # This searches for a business using the business name with a get parameter q. Visit the api docs to verify how to use it
-  GET /api/businesses/filter # This filters out businesses using category or location using get parameter categoryorlocation. Visit the api docs to verify how to use it
-  GET /api/businesses/paginate # This limits the number of businesses returned using get parameter limit. Visit the api docs to verify how to use it
9. API documentation and live API
-  You may visit the api documention for the persistent application live at https://we-connect-api-persistent.herokuapp.com/apidocs/ to have a feel of the api

## How to test the flask application
1. Create a folder weconnect on your computer
   
2. Download the repository at https://github.com/rogerokello/weconnect-practice/tree/dev-v4 to your computer into the created folder

3. Navigate into created folder

    ```
        $ cd weconnect-practice
    ```
4. Create and activate  virtual environment.

    ```
        $ virtualenv  venv

        $ source venv/bin/activate
    ```

    More on setting up Virtual environment: [how to set up virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

5. Install the packages in requirements.txt
   While at your prompt initiate the following command

    ``` $ pip install -r requirements.txt ```

6. Run your tests from the terminal like this to see how many have passed

    ```
        $ python manage.py testv1
    ```
