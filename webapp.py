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
    year = get_year_options()
    return render_template('page2.html', year_options=year )




@app.route('/showFact')
def render_fact():
    countries = get_country_options()
    Country = request.args.get('Country')
    
    population1980 = Country_stats_1980(Country)
    population2012 = Country_stats_2012(Country)
    
    Word1 = ""
    if population1980[0] > population2012[0]:
        Word1 = "However,"
    else:
        Word1 = "Unfortunately,"
        
    cigarettesGraph = get_Graph()
    graphdata = get_data(Country)
    
    print(graphdata)

    fact1980 = "During 1980, the percentage of smokers out of the country population was " + str(population1980[0]) + "% with a total population of " + str(population1980[1]) + " smokers."
    
    fact2012 = Word1 + " in 2012, the percentage of smokers was " + str(population2012[0]) + "% with a population of " + str(population2012[1]) + " smokers!"
    
    
    return render_template('page1.html', country_options=countries, funFact=fact1980, funFact2=fact2012, graph=cigarettesGraph, graphdata = graphdatanum)
    
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
        data = json.load(smoking_data)
    Year=[]
    for c in data:
        if c["Year"] not in Year:
            Year.append(c["Year"])
    options=""
    for s in Year:
        options += Markup("<option value=\"" + str(s) + "\">" + str(s) + "</option>") #Use Markup so <, >, " are not escaped lt, gt, etc.
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
    
def Country_stats_2012(country):
    """Return the data of a country in the year 2012"""
    with open('smoking.json') as smoking_data:
        data = json.load(smoking_data)
    percentage=0
    population = 0
    print(country)
    for c in data:
        if c["Country"] == country:
            if c["Year"] == 2012:
                percentage = percentage + c['Data']['Percentage']['Total']
                population = population + c['Data']['Smokers']['Total']
    facts = [percentage, population]
    return facts

def get_Graph():
    """Return the Graph command"""
    graph = Markup("<div id=""chartContainer"" style=""height: 300px; width: 100%;""></div>")
    #Use Markup so <, >, " are not escaped lt, gt, etc.
    return graph
    

def get_data(country):
    with open('smoking.json') as smoking_data:
        data = json.load(smoking_data)
    graphdata = []
    for c in data:
        if c["Country"] == country:
            datapoint = { "label": c["Year"], "y": c["Data"]["Daily cigarettes"]}
            graphdata = [datapoint]
            #graphdata.push()
    return graphdata

if __name__=="__main__":
    app.run(debug=True)
