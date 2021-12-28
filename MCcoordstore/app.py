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


from flask import render_template, redirect, flash, request, url_for
from markupsafe import Markup
from werkzeug.security import check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
import pytz
import json

from MCcoordstore import create_app
from .forms import AddPOIForm, SignupForm, LoginForm, StyleEditForm
from .db import get_db, User, PointOfInterest, POI_NAME_LOOKUP, RenderStyle
from .utils import serialize_pois

app = create_app()
db = get_db(app)

def get_default_style(db):
    stmt = db.select(RenderStyle).where(RenderStyle.name == "default")
    results = db.session.execute(stmt)
    return results.scalars().one()



@app.route("/", methods=["POST", "GET"])
def index():
    
    form = AddPOIForm()
    form.load_style_choices(db)
    if form.validate_on_submit():
        poi = PointOfInterest(name=form.data["name"], public=form.data["public"], user=current_user,
                              coordtype=form.data["coordtp"])
        poi.coords = form.coords
        style = get_default_style(db)
        poi.style = style
        
        db.session.add(poi)
        db.session.commit()
        return redirect("/")

    return render_template("index.htm", form=form)


@app.route("/add_manual", methods=["POST","GET"])
@login_required
def add_manual():
    form = AddPOIForm()
    form.load_style_choices(db)
    if form.validate_on_submit():
        #TODO: user guest only for now
        poi = PointOfInterest(name=form.data["name"], public=form.data["public"], user=current_user,
                              coordtype=form.data["coordtp"])
        
        print("coordtp: %s" % form.data["coordtp"])
        print("coordtp tp : %s" % str(type(form.data["coordtp"])))
        poi.coords = form.coords
        poi.styleid = form.data["style"]
        db.session.add(poi)
        db.session.commit()
        return redirect("/")

    return render_template("add_manual.htm", form=form)

@app.route("/editpoi/<int:poiid>", methods=["POST","GET"])
@login_required
def edit_poi(poiid: int):
    stmt = db.select(PointOfInterest).filter(PointOfInterest.poiid == poiid)
    poi = db.session.execute(stmt).scalars().one()

    if not poi.user == current_user:
        flash("you do not have permission to edit this POI", "flash-error")
        return redirect("/")
    
    form = AddPOIForm()
    form.load_style_choices(db)

    if form.validate_on_submit():
        form.update_object(poi)
        db.session.commit()
        flash("POI edited", "flash-success")
        return redirect("/")
    else:
        form.prefill(poi)
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

@app.route("/styleedit")
@login_required
def style_select():

    stmt = db.select(RenderStyle).filter(RenderStyle.user == current_user)
    styles = db.session.execute(stmt).scalars()
    
    
    return render_template("style_select.htm", styledats=styles)

@app.route("/styleedit/<int:styleid>", methods=["GET","POST"])
@login_required
def style_edit(styleid: int):
    stmt = db.select(RenderStyle).filter(RenderStyle.styleid == styleid)
    style = db.session.execute(stmt).scalars().one()

    if not style.user == current_user:
        flash("you do not have permission to edit this style", "flash-error")
        return redirect("/")
    
    form = StyleEditForm()
        
    if form.validate_on_submit():
        print(db.session.is_modified(style))
        print(style.style)
        form.update_object(style)
        print(style.style)
        print(db.session.is_modified(style))
        db.session.commit()
        
        flash("style updated", "flash-success")
        form.prefill(style)
        return redirect("/styleedit")
    
    try:
        form.prefill(style)
    except KeyError:
        print("missing key, probably not in style db data, continuing...")
    
    
    return render_template("style_edit.htm", form=form, datamapping=json.dumps(form.MAPPING))


@app.route("/newstyle", methods=["GET","POST"])
@login_required
def style_create():
    form = StyleEditForm()
    if form.validate_on_submit():

        rdrdct = form.db_json
        print(rdrdct)
        style = RenderStyle(name = form.data["stylename"],
                            styleversion = form.STYLE_VERSION,
                            style = rdrdct,
                            user = current_user)    
        db.session.add(style)
        db.session.commit()
        flash("style created", "flash-success")
        return render_template("style_edit.htm", form=form)
    elif request.method=="POST":
        flash("form not validated!", "flash-error")
    
        print(json.dumps(form.MAPPING))
    return render_template("style_edit.htm", form=form, datamapping=json.dumps(form.MAPPING))

