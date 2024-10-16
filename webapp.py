from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route("/")
def render_main():
    return render_template('index.html')
    
@app.route("/p1")
def render_page1():
    country = get_country_options()
    #year = get_year_options()
    #print(states)
    return render_template('page1.html', country_options=country)
    
@app.route("/p2")
def render_page2():
    return render_template('page2.html')


@app.route('/showFact')
def render_fact():
    countries = get_country_options()
    Country = request.args.get('Country')
    
    population1980 = Country_stats_1980(Country)
    
    fact1980 = "During 1980, the percentage of smokers of the total population was " + str(population1980[0]) + " with a total of " + str(population1980[1]) + " people."
    
    fact2012 = ""
    
    return render_template('page1.html', country_options=countries, funFact=fact1980, funFact2=fact2012)
    
def get_country_options():
    """Return the html code for the drop down menu.  Each option is a state abbreviation from the demographic data."""
    with open('smoking.json') as smoking_data:
        data = json.load(smoking_data)
    Country=[]
    for c in data:
        if c["Country"] not in Country:
            Country.append(c["Country"])
    options=""
    for s in Country:
        options += Markup("<option value=\"" + s + "\">" + s + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
    return options
    
def get_year_options():
    """Return the html code for the drop down menu.  Each option is a country from the smoking data."""
    with open('smoking.json') as smoking_data:
        year = json.load(smoking_data)

    options=""
    return options
    
def Country_stats_1980(country):
    """Return the data of a county in the year 1980"""
    with open('smoking.json') as smoking_data:
        data = json.load(smoking_data)
    percentage=0
    population = 0
    print(country)
    for c in data:
        if c["Country"] == country:
            if c["Year"] == 1980:
                percentage = percentage + c['Data']['Percentage']['Total']
                population = population + c['Data']['Smokers']['Total']
    facts = [percentage, population]
    return facts
    
def Country_stats_2012(state):
    """Return the data of a country in the year 2012"""
    with open('smoking.json') as smoking_data:
        data = json.load(demographics_data)
    highest=0
    county = ""
    for c in data:
        if c["State"] == state:
            if c["Age"]["Percent Under 18 Years"] > highest:
                highest = c["Age"]["Percent Under 18 Years"]
                county = c["County"]
    return county


if __name__=="__main__":
    app.run(debug=True)
