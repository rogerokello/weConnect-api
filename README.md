[![Build Status](https://travis-ci.org/rogerokello/weconnect-practice.svg?branch=dev-v6)](https://travis-ci.org/rogerokello/weconnect-practice) <a href='https://coveralls.io/github/rogerokello/weconnect-practice?branch=dev-v6'><img src='https://coveralls.io/repos/github/rogerokello/weconnect-practice/badge.svg?branch=dev-v6' alt='Coverage Status' /></a>
 <a href="https://codeclimate.com/github/rogerokello/weconnect-practice/maintainability"><img src="https://api.codeclimate.com/v1/badges/203bec3842f23583461b/maintainability" /></a>
</br>
# weConnect API
This API brings businesses and individuals together. By using it one will be able to create awareness of businesses and give users the ability to write reviews about the businesses that they have interacted with. Please visit a prototype at https://rogerokello.github.io/weconnect-practice/

## How to run the flask application
1. Create a folder weconnect on your computer
   
2. Clone the app to your folder by issuing this command

    ```
        $ git clone https://github.com/rogerokello/weconnect-practice.git
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

7. Using postman, the url to run the API locally is ```http://127.0.0.1:5000```.

    More on setting up postman: Please visit (https://www.getpostman.com/)

8. You may use postman to use the following endpoints of the API locally.

| Method | End Point | Description |
| --- | --- | --- |
|  POST |   `/api/auth/register` |        This registers a new user |
|  POST | `/api/auth/login`  |          This logins an already registered user |
|  POST | `/api/auth/logout` |          This logs out a user |
|  POST | `/api/auth/reset-password`  |  This changes the password of a user |
|  POST | `/api/businesses` |           This registers a new business |
|  PUT | `/api/businesses/<businessId>` | This updates a business profile |
|  DELETE | `/api/businesses/<businessId>` | This removes a business |
|  GET | `/api/api/businesses`            |  This gets all the existing businesses. You may also specify a get parameter pageNo, q or limit. The limit parameter will return a specified number of results, pageNo the results at a certain page while q will return businesses according to name, category or location |
|  GET | `/api/businesses/<businessId>` |  This gets a business |
|  POST | `/api/businesses/<businessId>/reviews`  |  This makes a review for a business |
|  GET | `/api/businesses/<businessId>/reviews` |  This gets the reviews that belong to a business |
|  GET | `/api/businesses/search` | This searches for a business using the business name with a get parameter q. Visit the API docs to verify how to use it |
|  GET | `/api/businesses/filter` | This filters out businesses using category or location using get parameter categoryorlocation. Visit the api docs to verify how to use it |
|  GET | `/api/businesses/paginate` | This limits the number of businesses returned using get parameter limit. Visit the API docs to verify how to use it |
