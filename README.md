# Group D'Etat

Roster: Rachel Ng (PM), Ray Onishi, Tina Wong, Maggie Zhao


## Ambrosia

Ambrosia is a website for keeping track of your eating, sleeping, exercising, and water drinking habits. 

Ambrosia uses user input to track how much sleep and exercise you get, how much water you drink, what you eat, and more! Ambrosia also encourages a healthier lifestyle by suggesting workouts to exercise different parts of the body and recipes to fix nutritional deficiencies from the user's diet. 

[Checkout our video demo here](https://www.youtube.com/)

## How to Run

1. Clone this repo into your folder of choice 

    ```
    $ git clone git@github.com:rachel-ng/group-d-etat.git
    ```

2. Now open your folder

    ```
    $ cd group-d-etat
    ```

3. Activate your virtual environment and upgrade `pip`  
<sup>Need a virtual environment? Follow the [instructions below](#dependencies)</sup>  

    ```
    $ . path/to/venv/bin/activate    # for Linux / OS
    $ source path/to/venv/Scripts/activate    # for Windows
    
    (venv) $ pip install --upgrade pip
    ```
    
4. Install the [dependencies](#dependencies) with [requirements.txt](requirements.txt) by running the following command  
<sup>It includes Flask, Wheel, *the stuff we use to keep your password safe*, *render your graphs*, and all that other good stuff!!</sup>


    ```
    (venv) $ pip install -r requirements.txt
    ```

5. Attain your [API keys (more info below)](#APIs) and add them to `keys/[api_name].json` like so  

    ```
    $ nano keys/workout_manager.json
    ```
    ```
    {
        "WORKOUT_MANAGER_API": "[API_KEY_ATTAINED]"
    }
    ```


    ```
    $ nano keys/usda_nutrients.json
    ```
    ```
    {
        "USDA_NUTRIENTS_API": "[API_KEY_ATTAINED]"
    }
    ```

6. Now you can run the python file (starting the Flask server)

    ```
    (venv) $ python app.py
    ```

7. Now type either one into your browser of choice and start using Ambrosia!  
<sup>or copy and paste</sup>

    ```
    http://127.0.0.1:500/
    ```
    
    ```
    localhost:5000
    ```

## APIs 

### [Workout Manager](https://wger.de/en/user/api-key)

Workout Manager is used to recommend exercises for different areas of the body. 

**How to attain your API key**

1. Sign up for an account
2. On their [API key page](https://wger.de/en/user/api-key), click on the button "Generate new API key" and it should show up in the box "Your API key" 
3. Add it to `keys/workout_manager.json` 

    ```
    $ nano keys/workout_manager.json
    ```
    ```
    {
        "WORKOUT_MANAGER_API": "[API_KEY_ATTAINED]"
    }
    ```

### [USDA Nutrients](https://api.data.gov/signup/)

USDA Nutrients is used to get information about nutrients and their values in various portions of different foods. 

**How to attain your API key**

1. Sign up for an account  
<sup>If you're looking at [Data.gov](https://api.data.gov/signup/), that's the correct site!</sup>
2. Check your email for your new API key! 
3. Add it to `keys/usda_nutrients.json` 

    ```
    $ nano keys/usda_nutrients.json
    ```
    ```
    {
        "USDA_NUTRIENTS_API": "[API_KEY_ATTAINED]"
    }
    ```


## Dependencies 

Install the dependencies with [requirements.txt](requirements.txt) by running the following command

```
(venv) $ pip install -r requirements.txt
```

- venv  
`venv` is used to create an isolated environment for whatever version of Python (and whatever libraries you're installing) you're using to wreak havoc in. `venv` allows you to use different versions of Python so you don't need to worry about compatibility issues or breaking your computer. Run the following to install if you don't already have it: 

    ```
    $ python3 -m venv venv_name 
    ```
    
    For versions older than Python 3.0.0:  
    ```
    $ pip install virtualenv
    $ virtualenv venv_name  
    ```

- pip  
`pip` is used to install and manage Python packages. Usually comes installed with Python, check out [this page for instructions](https://pip.pypa.io/en/stable/installing/) if you find that further action is required. Remember to upgrade! 

    ```
    (venv) $ pip install --upgrade pip
    ```

- os  
`os` is used for miscellaneous operating system dependent functions. A standard Python library with no further action required.

- urllib  
`urllib` is used to get JSON files from APIs. A standard Python library with no further action required. 

- json  
`json` is used to parse JSON files requested from APIs. A standard Python library with no further action required. 

- flask  
`flask` allows the app to be run on `localhost`, needs `wheel`. Installed with [requirements.txt](requirements.txt) 

    ```
    (venv) $ pip3 install flask
    ```

- wheel  
`wheel` is needed to use `flask`. Installed with [requirements.txt](requirements.txt) 

    ```
    (venv) $ pip3 install wheel
    ```

- Jinja2  
`Jinja2` is used for templating HTML pages. Installed with [requirements.txt](requirements.txt), installed when you install `flask`

- DateTime  
`DateTime` is used to get the current date and time. Installed with [requirements.txt](requirements.txt) 

    ```
    (venv) $ pip install DateTime
    ```

- passlib  
`passlib` is used to hash your password. Installed with [requirements.txt](requirements.txt) 

    ```
    (venv) $ pip install passlib
    ```

- plotly  
`plotly` is used to render your graphs. Installed with [requirements.txt](requirements.txt) 

    ```
    (venv) $ pip install plotly
    ```
