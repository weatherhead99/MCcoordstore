#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 18:23:28 2021

@author: danw
"""

from flask import Flask, render_template, request
import numpy as np
from plots import LocationsPlot
from markupsafe import Markup

app = Flask(__name__)

@app.route("/")
def index():
    
    locplot = LocationsPlot()
    locplot.xdat = np.random.normal(0., 1., 5)
    locplot.zdat = np.random.normal(0, 1, 5)
    locplot.update_plot()
    return render_template("index.htm", map_html_2d = Markup(locplot.rendered_html))


@app.route("/add_manual", methods=["POST","GET"])
def add_manual():
    
    if request.method == "POST":
        print("posted form!")
        
    else:
        return render_template("add_manual.htm")
    