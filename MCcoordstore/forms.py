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
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.fields import  HiddenField, IntegerRangeField, DecimalRangeField
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import ColorInput
from markupsafe import Markup
from .db import CoordType, POI_NAME_LOOKUP, RenderStyle, PointOfInterest

def _reqfield(func, *args, **kwargs):
    return func(*args, **kwargs, validators=[DataRequired()])

class AddPOIForm(FlaskForm):
    name = _reqfield(StringField, "name")
    x = _reqfield(IntegerField, "x")
    y = _reqfield(IntegerField, "y")
    z = _reqfield(IntegerField, "z")
    
    typechoice = [(str(i.value), POI_NAME_LOOKUP[i]) for i in CoordType]
    
    coordtp = _reqfield(SelectField, "type", choices=typechoice)
    public = BooleanField("public")

    style = _reqfield(SelectField, "style", id="styleselectfield", coerce=int)
    
    @property
    def coords(self):
        return (self.data["x"], self.data["y"], self.data["z"])

    def load_style_choices(self, db):
        stmt = db.select(RenderStyle)
        choices = []
        for style in db.session.execute(stmt).scalars():
            choices.append((style.styleid, style.name))
        self.style.choices = choices

    def prefill(self, poi: PointOfInterest):
        self.name.data = poi.name
        self.x.data = poi.coord_x
        self.y.data = poi.coord_y
        self.z.data = poi.coord_z
        self.style.data = poi.style.styleid
        self.coordtp.data = poi.coordtype.value
        self.public.data = poi.public

    def update_object(self, poi: PointOfInterest):
        poi.name = self.data["name"]
        poi.coords = self.coords
        poi.coordtype = self.data["coordtp"]
        poi.public = self.data["public"]
        poi.styleid = self.data["style"]

        
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


octpl = Markup("updatePlot('{}','{}')")
    
class StyleEditForm(FlaskForm):
    STYLE_VERSION = 1
    MAPPING = {"symbolname" : "marker.symbol",
               "fillcolor" : "marker.color",
               "linecolor" : "marker.line.color",
               "linewidth" : "marker.line.width",
               "symbolsize" : "marker.size",
               "opacity" : "marker.opacity"}
    
    stylename = _reqfield(StringField, "style name", id="symbolname")
    fillcolor = _reqfield(StringField, "fill colour", widget=ColorInput(),
                          id="fillcolor", render_kw={"onchange" : octpl.format("fillcolor", "marker.color")})
    linecolor = _reqfield(StringField, "line colour", widget=ColorInput(),
                          id="linecolor", render_kw = {"onchange" : octpl.format("linecolor", "marker.line.color")})
    
    linewidth = _reqfield(IntegerRangeField, "line width", 
                          id="linewidth", render_kw = {"onchange" : octpl.format("linewidth", "marker.line.width")})
    symbolsize = _reqfield(IntegerRangeField, "symbol size",
                           id="symbolsize", render_kw = {"onchange" : octpl.format("symbolsize", "marker.size")})

    symbolname = _reqfield(StringField, id="symtype")
    opacity = _reqfield(DecimalRangeField, "opacity", id="opacity", places=1,
                        render_kw = {"onchange" : octpl.format("opacity", "marker.opacity")})


    def prefill(self, style: RenderStyle):
        self.stylename.data = style.name

        for k,v in self.MAPPING.items():
            getattr(self, k).data = style.style[v]

    def update_object(self, style: RenderStyle):
        style.style = self.db_json
        style.name = self.data["stylename"]

    @property
    def db_json(self):
        rdrdct = {v : self.data[k] for k,v in self.MAPPING.items()}
        return rdrdct
        
