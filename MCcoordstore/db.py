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
Created on Thu Dec  9 17:55:36 2021

@author: danw
"""

from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import click
from typing import Sequence
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "user"
    userid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    displayname = db.Column(db.String(80), unique=True, nullable=False)
    hashed_pw = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    @classmethod
    def create_new_user(cls, username: str, displayname: str, password: str) -> "User":
        pwhash = generate_password_hash(password)
        return User(username = username, displayname=displayname, hashed_pw=pwhash)
    
    def get_id(self):
        return str(self.userid)



class RenderStyle(db.Model):
    __tablename__ = "renderstyle"
    styleid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=True)
    style = db.Column(db.PickleType)

class PointOfInterest(db.Model):
    __tablename__ = "pointofinterest"
    poiid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda : datetime.now(timezone.utc))
    public = db.Column(db.Boolean, default=False)

    userid = db.Column(db.Integer, db.ForeignKey("user.userid"), nullable=False)
    user = db.relationship("User", backref=db.backref("pois"))
    style = db.Column(db.Integer, db.ForeignKey("renderstyle.styleid"))

    coord_x = db.Column(db.Integer)
    coord_y = db.Column(db.Integer)
    coord_z = db.Column(db.Integer)
    
    @property
    def coords(self):
        return (self.coord_x, self.coord_y, self.coord_z)
    
    @coords.setter
    def coords(self, val: Sequence[int]):
        if len(val) != 3:
            raise ValueError("invalid length of coordinate")
        self.coord_x = val[0]
        self.coord_y = val[1]
        self.coord_z = val[2]
        
    def serialize_to_dict(self):
        return {"id" : self.poiid,
                "name" : self.name,
                "created" : str(self.create_date),
                "public" : self.public,
                "username" : self.user.username,
                "coord" : self.coords
                }


def get_db(app):
    db.init_app(app)
    return db


def create_db(admin_pass, db):
    db_path = db.engine.url
    print(f"creating new database with path: {db_path}")
    db.create_all()

    print("creating default admin and guest users")
    admin_user = User.create_new_user("admin", "admin", admin_pass)
    admin_user.is_admin = True
    guest_user = User.create_new_user("guest", "guest", "guest")

    db.session.add(admin_user)
    db.session.add(guest_user)
    db.session.commit()
    


@click.command("create-db")
@click.argument("admin_pass")
@with_appcontext
def create_db_command(admin_pass):
    from flask import current_app
    db.init_app(current_app)
    create_db(admin_pass, db)
    
    


@click.command("change-pw")
@click.argument("username")
@click.argument("new_pass")
@with_appcontext
def change_pw_command(username, new_pass):
    from flask import current_app
    db.init_app(current_app)

    usr = User.query.filter_by(username=username).first()
    pwhash = generate_password_hash(new_pass)
    usr.hashed_pw = pwhash
    db.session.commit()

    

