#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#      MCcoordstore - simple web based store for Minecraft points of interest
#      Copyright (C) 2021  Daniel Philip Weatherill

#      This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.

#      This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.

#      You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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

    
