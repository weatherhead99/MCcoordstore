#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 17:55:36 2021

@author: danw
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    userid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    displayname = db.Column(db.String(80), nullable=False)


class RenderStyle(db.Model):
    styleid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=True)
    style = db.Column(db.PickleType)

class PointOfInterest(db.Model):
    poiid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    public = db.Column(db.Boolean, default=False)

    userid = db.Column(db.Integer, db.ForeignKey("user.userid"))
    user = db.relationship("Category", backref=db.backref("pois"))
    style = db.Column(db.Integer, db.ForeignKey("renderstyle.styleid"))

    coord_x = db.Column(db.Integer)
    coord_y = db.Column(db.Integer)
    coord_z = db.Column(db.Integer)
    
    

