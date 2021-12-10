#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 18:23:28 2021

@author: danw
"""

from flask import Flask, render_template, request, redirect
import numpy as np
from .plots import LocationsPlot
from markupsafe import Markup
from .forms import AddPOIForm, SignupForm
from MCcoordstore import create_app
from .db import get_db, User, PointOfInterest
from sqlalchemy import select

app = create_app()
db = get_db(app)

@app.route("/")
def index():
    locplot = LocationsPlot()
    
    pois = PointOfInterest.query.filter_by(public=True).all()
    locplot.xdat = [_.coords[0] for _ in pois]
    locplot.zdat = [_.coords[2] for _ in pois]
    locplot.update_plot()
    
    return render_template("index.htm", map_html_2d = Markup(locplot.rendered_html),
                           poi_table_data = pois)


@app.route("/add_manual", methods=["POST","GET"])
def add_manual():
    form = AddPOIForm()
    if form.validate_on_submit():
        #TODO: user guest only for now
        stmt = select(User).where(User.username == "guest")
        result = db.session.execute(stmt)
        guest_usr = result.fetchone()[0]

        poi = PointOfInterest(name=form.data["name"], public=True, user=guest_usr)
        poi.coords = form.coords
        db.session.add(poi)
        db.session.commit()

        return redirect("/")    
    else:
        return render_template("add_manual.htm", form=form)
    
@app.route("/signup", methods=["POST","GET"])
def signup():
    form = SignupForm()

    return render_template("signup.htm", form=form)

