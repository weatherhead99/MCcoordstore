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
Created on Thu Dec  9 18:23:28 2021

@author: danw
"""

from flask import render_template, redirect, flash, current_app, g
from markupsafe import Markup
from sqlalchemy import select
from werkzeug.security import check_password_hash
from flask_login import login_required, current_user, login_user, logout_user

from MCcoordstore import create_app
from .plots import LocationsPlot
from .forms import AddPOIForm, SignupForm, LoginForm
from .db import get_db, User, PointOfInterest
from .utils import serialize_pois

app = create_app()
db = get_db(app)

@app.route("/", methods=["POST", "GET"])
def index():
    locplot = LocationsPlot()


    if current_user.is_authenticated:
        pois = PointOfInterest.query.all()
    else:
        pois = PointOfInterest.query.filter_by(public=True).all()
    

    locplot.xdat = [_.coords[0] for _ in pois]
    locplot.zdat = [_.coords[2] for _ in pois]
    locplot.update_plot()

    form = AddPOIForm()
    if form.validate_on_submit():
        #TODO: user guest only for now
        poi = PointOfInterest(name=form.data["name"], public=form.data["public"], user=current_user)
        poi.coords = form.coords
        db.session.add(poi)
        db.session.commit()
        return redirect("/")

    return render_template("index.htm", map_html_2d = Markup(locplot.rendered_html),
                           poi_table_data = pois, form=form)


@app.route("/add_manual", methods=["POST","GET"])
@login_required
def add_manual():
    form = AddPOIForm()
    if form.validate_on_submit():
        #TODO: user guest only for now
        poi = PointOfInterest(name=form.data["name"], public=form.data["public"], user=current_user)
        poi.coords = form.coords
        db.session.add(poi)
        db.session.commit()
        return redirect("/")

    return render_template("add_manual.htm", form=form)

@app.route("/signup", methods=["POST","GET"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        #check user is unique
        existing_usrname = User.query.filter_by(username=form.data["username"]).first()
        if existing_usrname:
            flash("either username or displayname is already in use!", "flash-error")
            return redirect("/signup")

        existing_displayname = User.query.filter_by(displayname=form.data["displayname"]).first()
        if existing_displayname:
            flash("displayname is already in use!", "flash-error")
            return redirect("/signup")

        new_usr = User.create_new_user(form.data["username"], form.data["displayname"],
                                       form.data["password"])
        db.session.add(new_usr)
        db.session.commit()

        flash("signup successful, you can now login", "flash-success")
        return redirect("/")
    return render_template("signup.htm", form=form)

@app.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.data["username"]).first()
        if not user or not check_password_hash(user.hashed_pw, form.data["password"]):
            flash("unable to login!", "flash-error")
            return redirect("/login")
        
        login_user(user)
        flash("successfully logged in", "flash-success")
        return redirect("/")
    return render_template("login.htm", form=form)


#TODO: implement REST DELETE METHOD
@app.route("/poi/delete/<idx>", methods=["GET"])
@login_required
def delete_poi(idx):
    try:
        intid = int(idx)
    except ValueError as err:
        flash("unable to interpret idx as int", "flash-error")
        return redirect("/")
    
    poi = PointOfInterest.query.filter_by(poiid=intid).first()
    
    if not poi:
        flash("invalid POI idx", "flash-error")
        return redirect("/")
    
    if poi.user != current_user and not current_user.is_admin:
        flash("no permission to delete POI!", "flash-error")
        return redirect("/")

    db.session.delete(poi)
    db.session.commit()

    flash("POI deleted", "flash-success")
    return redirect("/")



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/dump_pois")
@login_required
def dump_pois():
    return serialize_pois(app, db)

    
    
    
