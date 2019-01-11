import json
import plotly

def config() :
    with open('data/keys.json', 'r') as f:
        api_dict = json.load(f)

    plotly.tools.set_credentials_file(username= api_dict["PLOTLY_USERNAME"], api_key=api_dict["PLOTLY_API"])

    print("hooray!")
