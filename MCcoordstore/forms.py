#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 22:33:46 2021

@author: danw
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo

def _reqfield(func, *args, **kwargs):
    return func(*args, **kwargs, validators=[DataRequired()])

class AddPOIForm(FlaskForm):
    name = _reqfield(StringField, "name")
    x = _reqfield(IntegerField, "x")
    y = _reqfield(IntegerField, "y")
    z = _reqfield(IntegerField, "z")
    public = BooleanField("public")
    
    @property
    def coords(self):
        return (self.data["x"], self.data["y"], self.data["z"])
    

class SignupForm(FlaskForm):
    username = _reqfield(StringField, "username")
    displayname = _reqfield(StringField, "display name")
    password = PasswordField("password", [DataRequired(), 
                                          EqualTo("confirm", message="passwords must match")])
    confirm  = PasswordField("confirm password", [DataRequired()])

class LoginForm(FlaskForm):
    username = _reqfield(StringField, "username")
    password = _reqfield(PasswordField, "password")
    remember = BooleanField("remember me")

    