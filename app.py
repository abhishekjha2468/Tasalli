import random
#########################################################################################################################
import pandas as pd
import numpy as np
import math
import itertools
import numpy
from flask import Flask, request, render_template, jsonify
from flask_ngrok import run_with_ngrok
from flask import Flask, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
# import sqlite3
# import mysql.connector
import requests
from firebase import firebase
import ast
from flask_cors import CORS
import json

app = Flask(__name__,static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
app.config["DEBUG"] = True
# app._static_folder = os.path.abspath("templates/")
CORS(app)
#run_with_ngrok(app) 

@app.route("/<section>", methods=['GET','POST'])
def pages_render(section):
#     f=open("section"+".html","r")
#     text=f.read()
#     f.close()
    return render_template(section+".html")

@app.route("/", methods=['GET','POST'])
def Landing_page():
#     f=open("homepage_expert.html","r")
#     text=f.read()
#     f.close()
    return render_template("homepage_expert.html")


@app.route("/home", methods=['GET','POST'])
def home():
    return "Welcome"#render_template("homepage_expert.html")

# @app.route("/login", methods=['GET'])
# def loginPage():
#     f=open("login.html","r")
#     text=f.read()
#     f.close()
#     return text

# @app.route("/signup", methods=['GET'])
# def signupPage():
#     f=open("signup.html","r")
#     text=f.read()
#     f.close()
#     return text

def saveUserData(name,emailid,phoneNumber,password):
    f=firebase.FirebaseApplication("https://tasallii-default-rtdb.firebaseio.com/",None)
    data={
        "name" : name,
        "emailid": emailid,
        "phoneNumber"  : phoneNumber,
        "password": password}
    result=f.post("https://tasallii-default-rtdb.firebaseio.com/userData",data)
    return result
#
def readUserDataByEmailID(emailid):
    f=firebase.FirebaseApplication("https://tasallii-default-rtdb.firebaseio.com/",None)
    r=f.get("https://tasallii-default-rtdb.firebaseio.com/userData",'')
    DF=pd.DataFrame()
    DF["id"] = [i for i in r.keys()]
    DF["name"]=[i["name"] for i in r.values()]
    DF["emailid"]=[i["emailid"] for i in r.values()]
    DF["phoneNumber"]=[i["phoneNumber"] for i in r.values()]
    DF["password"]=[i["password"] for i in r.values()]

    if emailid in list(DF['emailid']):
        d = list(DF[DF['emailid']==emailid].to_dict('index').values())[0]
        d['status'] = 'success'
        return d
    return {'status': 'failed','message': 'Email not exists'}

def checkPassword(emailid,password):
    d=readUserDataByEmailID(emailid)
    if d['status']=='failed':
        return False,d['message']
    else:
        if d['password']!=password:
            return False,'Incorrect Password'
        return True,d

# @app.route("/dashboard", methods=['GET','POST'])
# def dashboard():
#     return 'Welcome To Dashboard'

@app.route("/signupSubmit", methods=['GET','POST'])
def signup_submit():
    name = request.form["fullname"]
    emailid=request.form["emailid"]
    phoneNumber=request.form["phonenumber"]
    password=request.form["password"]
    d=readUserDataByEmailID(emailid)
    if d['status']=='success':
        return loginPage()
    else:
        result=saveUserData(name,emailid,phoneNumber,password)
        return dashboard()

@app.route("/loginSubmit", methods=['GET','POST'])
def login_submit():
    emailid = request.form["emailid"]
    password = request.form["password"]
    check,d = checkPassword(emailid, password)
    if check:
        return dashboard()
    else:
        return d

@app.route("/api/testJson/", methods=['GET','POST'])
def test_json():
    data=[{"Task_header": "Bug in buildng sam","Task_defination":"sam command not found","Higest_price":100,"Lowest_price":40},
          {"Task_header": "Bug in buildng docker image","Task_defination":"How to install docker desktop","Higest_price":110,"Lowest_price":45},
          {"Task_header": "How to use postman","Task_defination":"Need to test api's with multiple methods GET,POST,PUT,DELETE, etc..","Higest_price":90,"Lowest_price":50}]
    return jsonify(data)
#
#
#
# @app.route("/projectsavedata", methods=['GET','POST'])
# def save():
#     Analystname=request.form["ayst_n"]
#     Deliveryid=request.form["did"]
#     Chaptername=request.form["chp_name"]
#     Teacherlead=request.form["tch_lead"]
#     Topicname=request.form["tpc_name"]
#     Timeline=request.form["time_line"]
#     result=pro_1_save_data(Deliveryid,Chaptername,Topicname,Teacherlead,Analystname,Timeline)
#     return f'Your Task id is {result["name"]}'
############################################################
app.run()
