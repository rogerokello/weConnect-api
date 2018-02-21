[![Coverage Status](https://coveralls.io/repos/github/rogerokello/weconnect-practice/badge.svg?branch=dev-v1)](https://coveralls.io/github/rogerokello/weconnect-practice?branch=dev-v1)
# weconnect api
An api to enable you manage your business and reviews. Please visit a prototype at https://rogerokello.github.io/weconnect-practice/

## Project Dependencies
1. Ubuntu 14.0 and above
2. Python 3.6.*
3. Flask 0.12.*

## How to run the flask application
1. Create a folder weconnect on your computer
   
2. Download the repository at https://github.com/rogerokello/weconnect-practice/tree/dev-v1 to your computer into the created folder

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

6. Run your app from the terminal like this

    ```
        $ python run.py
    ```

7. Using postman, the url to run the api locally is ```http://127.0.0.1:5000/```.

8. Sample: Use postman to navigate the following endpoints of the api.
-  Register a new business (Using a POST request for postman JSON below)
    Locally:
    ```
    http://127.0.0.1:5000/businesses
    ```

    ```
    {
        "name": "XEDROX",
        "category": "IT",
        "location": "Lira"
    }
    ```
## How to test the flask application
1. Create a folder weconnect on your computer
   
2. Download the repository at https://github.com/rogerokello/weconnect-practice/tree/dev-v1 to your computer into the created folder

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
        $ python app_tests.py
    ```
