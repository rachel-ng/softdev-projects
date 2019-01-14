# Group D'Etat

Roster: Rachel Ng (PM), Ray Onishi, Tina Wong, Maggie Zhao

## Ambrosia

Ambrosia is a website for keeping track of your eating, sleeping, exercising, and water drinking habits. 

Ambrosia uses user input to track how much sleep and exercise you get, how much water you drink, what you eat, and more! Ambrosia also encourages a healthier lifestyle by suggesting workouts to exercise different parts of the body and recipes to fix nutritional deficiencies from the user's diet. 

## How to Run

1. Clone this repo into your folder of choice 

    ```
    $ git clone https://github.com/rachel-ng/group-d-etat.git
    ```

2. Now open your folder

    ```
    $ cd group-d-etat
    ```

3. Activate your virtual environment 

    ```
    . path/to/virtual/environment/bin/activate #for Linux/OS
    source path/to/virtual/environment/Scripts/activate #for Windows
    ```

4. Install the [dependencies](#dependencies) with [requirements.txt](requirements.txt) by running the following command  
<sup>It includes Flask, Wheel, *the stuff we use to keep your password safe*, *render your graphs*, and all that other good stuff!!</sup>

    ```
    pip install -r requirements.txt
    ```

5. Attain your [API Keys (more info below)](#get-your-api-keys) and add them to `keys/[api_name].json` like so  

    ```
    ~ nano keys/workout_manager.json
    ```
    ```
    {
        "WORKOUT_MANAGER_API": "[API_KEY_ATTAINED]"
    }
    ```


    ```
    ~ nano keys/usda_nutrients.json
    ```
    ```
    {
        "USDA_NUTRIENTS_API": "[API_KEY_ATTAINED]"
    }
    ```

6. Now you can run your python file (starting the Flask server)

    ```
    python app.py
    ```

7. Now type this into your browser of choice and start using Ambrosia!  
<sup>or copy and paste</sup>

    ```
    http://127.0.0.1:500/
    ```


## Get your API Keys 

[Workout Manager](https://wger.de/en/user/api-key)

1. Sign up for an account
2. On their [API key page](https://wger.de/en/user/api-key), click on the button "Generate new API key" and it should show up in the box "Your API key" 

[USDA Nutrients](https://api.data.gov/signup/)

1. Sign up for an account
2. Check your email for your new API key! 

## Dependencies 

Install the dependencies with [requirements.txt](requirements.txt) by running the following command

```
pip install -r requirements.txt
```

- os  
`os` is used for miscellaneous operating system dependent functions. A standard Python library that can be imported.

- urllib  
`urllib` is used to get JSON files from APIs. A standard Python library that can be imported. 

- json  
`json` is used to parse JSON files requested from APIs. A standard Python library that can be imported. 

- flask  
`flask` allows the app to be run on `localhost`, needs `wheel`. Installed with [requirements.txt](requirements.txt) 

- wheel  
`wheel` is needed to use `flask`. Installed with [requirements.txt](requirements.txt) 

- Jinja2  
`Jinja2` is used for templating HTML pages. Installed with [requirements.txt](requirements.txt) 

- DateTime  
`DateTime` is used to get the current date and time. Installed with [requirements.txt](requirements.txt) 

- passlib  
`passlib` is used to hash your password. Installed with [requirements.txt](requirements.txt) 

- plotly  
`plotly` is used to render your graphs. Installed with [requirements.txt](requirements.txt) 
