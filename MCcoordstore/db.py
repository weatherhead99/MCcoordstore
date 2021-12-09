#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 17:55:36 2021

@author: danw
"""

from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import click

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    userid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    displayname = db.Column(db.String(80), nullable=False)


class RenderStyle(db.Model):
    __tablename__ = "renderstyle"
    styleid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=True)
    style = db.Column(db.PickleType)

class PointOfInterest(db.Model):
    __tablename__ = "pointofinterest"
    poiid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    public = db.Column(db.Boolean, default=False)

    userid = db.Column(db.Integer, db.ForeignKey("user.userid"))
    user = db.relationship("User", backref=db.backref("pois"))
    style = db.Column(db.Integer, db.ForeignKey("renderstyle.styleid"))

    coord_x = db.Column(db.Integer)
    coord_y = db.Column(db.Integer)
    coord_z = db.Column(db.Integer)

@click.command("create-db")
@with_appcontext
def create_db_command():
    from flask import current_app
    db.init_app(current_app)

    db_path = db.engine.url
    print(f"creating new database with path: {db_path}")
    db.create_all()

    print("creating default admin and guest users")
    admin_user = User(username="admin", displayname="admin")
    guest_user = User(username="guest", displayname="guest")

    db.session.add(admin_user)
    db.session.add(guest_user)
    db.session.commit()
