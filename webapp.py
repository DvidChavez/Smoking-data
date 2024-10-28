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
    years = get_year_options()
    
    return render_template('page2.html', year_options=years)

@app.route("/showFactYear")
def render_factP2():
    years = get_year_options()
    Year = request.args.get('Year')
    
    countryhighestpop = get_greatest_population(int(Year))
    highestGender = get_gender_population(int(Year))
    
    fact3 = "The country with the greatest percentage of smokers in the year " + Year + " is " + countryhighestpop[0] + " with the greatest percetnage of " + str(countryhighestpop[1]) + "% and a total population of " + str(countryhighestpop[2]) + " smokers."
    
    fact4 = "The Country with the highest percentage of male smokers during the year " + Year + " is " + highestGender[0] + " with a percentage of X% from a populaton of X total. Additionally, the Country with the highest population of women is Xwith a percanage of X% from a population of X." 
    
    return render_template('page2.html', year_options=years, year_fact=fact3, year_fact2 = fact4, year=Year)


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
    
    
    txt1 = "This graph shows the daily usage of cigarettes on average per smoker"
    
    fact1980 = "During 1980, the percentage of smokers out of the " + Country + " population was " + str(population1980[0]) + "% with a total population of " + str(population1980[1]) + " smokers."
    
    fact2012 = Word1 + " in 2012, the percentage of smokers was " + str(population2012[0]) + "% with a population of " + str(population2012[1]) + " smokers!"
    
    
    return render_template('page1.html', country_options=countries, funFact=fact1980, funFact2=fact2012, graph=cigarettesGraph, graphdatanum=str(graphdata), text1=txt1, selected_Country=Country)
    
    
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
            datapoint = {"label": c["Year"], "y": c["Data"]["Daily cigarettes"]}
            graphdata.append(datapoint)
            
            #graphdata.push()
    return graphdata
    
def get_greatest_population(year):
    """Return the country with highest percentage and its total population based on year input."""
    with open('smoking.json') as smoking_data:
        data = json.load(smoking_data)
    country=""
    percentage=0
    population=0
    for c in data:
        if c["Year"] == year:
            if c["Data"]["Percentage"]["Total"] > population:
                percentage = c["Data"]["Percentage"]["Total"]
                population= c["Data"]["Smokers"]["Total"]
                country = c["Country"]
                
    facts = [country, percentage, population]
    return facts

def get_gender_population(year):
    """Return the country with highest percentage and its total population based on year input."""
    with open('smoking.json') as smoking_data:
        data = json.load(smoking_data)
    countryM=""
    countryF=""
    population=0
    population2=0
    malepercent = 0
    femalepercent = 0
    for c in data:
        if c["Year"] == year:
            if c["Data"]["Percentage"]["Male"] > malepercent:
                malepercent = c["Data"]["Percentage"]["Total"]
                population= c["Data"]["Smokers"]["Total"]
                countryM = c["Country"]
            if c["Data"]["Percentage"]["Female"] > femalepercent:
                femalepercent = c["Data"]["Percentage"]["Total"]
                population2 = c["Data"]["Smokers"]["Total"]
                countryF = c["Country"]
                
    facts = [countryM, countryF, malepercent, femalepercent, population, population2]
    return facts

def county_most_under_18(state):
    
    with open('demographics.json') as demographics_data:
        counties = json.load(demographics_data)
    highest=0
    county = ""
    for c in counties:
        if c["State"] == state:
            if c["Age"]["Percent Under 18 Years"] > highest:
                highest = c["Age"]["Percent Under 18 Years"]
                county = c["County"]
    return county
    
if __name__=="__main__":
    app.run(debug=True)

