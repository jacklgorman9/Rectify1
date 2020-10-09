# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 22:42:13 2020

@author: jackl
"""
import flask
from flask import Flask, Response, render_template, request, redirect, url_for
from wtforms import TextField, Form
from guest_Model import podcastModelGuest
from podcastModelTopic import podcastModelTopic
import json

app = flask.Flask('JRE_Flask')




@app.route("/")
def home():
    return flask.render_template('index1.html')
#prediction model for specific profiles
@app.route("/", methods=["POST","GET"])
def predictor1():
    # if [request.args]:
    #     if request.form.post['chat_in1'] =
    #     print(request.form['chat_in1'])
    #     x_input, predictions = podcastModelGuest((request.form['chat_in1']))
    #     return flask.render_template('predictGuest.html',chat_in1 = x_input, prediction=predictions)
    # else:   
    #     x_input, predictions = podcastModelGuest('Elon Musk')
    #     return flask.render_template('predictGuest.html', chat_in1 = x_input, prediction = predictions)
    if request.method == 'POST':
       
        if request.form['submit'] == 'submit1':
            print('one works')
            x_input, predictions = podcastModelGuest((request.form['chat_in1']))
            return flask.render_template('predictGuest.html',chat_in1 = x_input, prediction=predictions)
        elif request.form['submit'] == 'submit2':
            print('2')
            x_input, predictions = podcastModelTopic((request.form['chat_in2']))
            return flask.render_template('predictGuest.html',chat_in1 = 'Pussy Lips'+x_input, prediction=predictions)          
        else:
            x_input, predictions = podcastModelGuest('Elon Musk')
            return flask.render_template('predictGuest.html',chat_in1 = 'Search Didnt Work', prediction=predictions)

    # elif request.method == 'GET':
    #     return render_template('contact.html', form=form)
#predicition model for specific area of interest

    
                               
    
if __name__=="__main__":
    # For local development, set to True:
    app.run(debug=False)
    # For public web serving:
    #app.run(host='0.0.0.0')
    app.run()
    