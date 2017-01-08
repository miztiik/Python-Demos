# -*- coding: utf-8 -*-
from flask import Flask, render_template,redirect, url_for, request
import requests,json
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("welcome.html")

@app.route("/<name>")
def hello_name(name):
    return render_template( "welcome.html", userName = name )

@app.route("/mediaMetaData", methods = ["GET", "POST"] )
def mediaMetaData():
    
    if request.method == "POST":
        error = None
        
        # http://www.omdbapi.com/?t=titanic&y=1997&r=json
        omdbUrl = "http://www.omdbapi.com"
    
        mediaName = request.form['mediaTitle']
    
        if not mediaName:
            mediaName = "Inception"
    
        parameters = { "t" : mediaName , "y" :"", "tomatoes":"True", "r" : "json" }
        response = requests.get( omdbUrl, params = parameters)
    
        mediaMetata = response.json()
        return render_template( "mediaMetaData.html" , mediaName = mediaName, result = response.json() )

    # Render just the template when method is "GET"
    return render_template ( "mediaMetaData.html" )

if __name__ == '__main__':
   app.run(debug = True)