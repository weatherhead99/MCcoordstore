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



from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import Enum, MetaData
import click
from typing import Sequence
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer
import enum
from random import randint
from flask_migrate import stamp
import os

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}



metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

USER_MIN_ALTERNATE_ID = 1000
USER_MAX_ALTERNATE_ID = 1000000


def _server_random_sqlite_range():
    return "abs(random() % ( {max} - {min} )) + {min}".format(min=USER_MIN_ALTERNATE_ID, max=USER_MAX_ALTERNATE_ID)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    MIN_ALTERNATE_ID=USER_MIN_ALTERNATE_ID
    MAX_ALTERNATE_ID=USER_MAX_ALTERNATE_ID
    
    userid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    displayname = db.Column(db.String(80), unique=True, nullable=False)
    hashed_pw = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    alternate_id = db.Column(db.Integer, unique=True, nullable=False, server_default=_server_random_sqlite_range())
    default_styleid = db.Column(db.Integer, db.ForeignKey("renderstyle.styleid", use_alter=True), nullable=True)
    default_style = db.relationship("RenderStyle", foreign_keys=[default_styleid])
   
    
    @classmethod
    def create_new_user(cls, username: str, displayname: str, password: str) -> "User":
        pwhash = generate_password_hash(password)
        altid = cls.random_unique_alternateid()
        return User(username = username, displayname=displayname, 
                    hashed_pw=pwhash, alternate_id=altid)

    def get_id(self):
        return str(self.userid)

    def generate_api_token(self, app, expiration_seconds: int = 86400) -> bytes:
        secret_key = app.config["SECRET_KEY"]
        ser = TimedJSONWebSignatureSerializer(secret_key, expiration_seconds)
        return ser.dumps({"userid" : self.alternate_id}).decode("ASCII")
    
    @classmethod
    def verify_api_token(cls, app, token: bytes):
        secret_key = app.config["SECRET_KEY"]
        ser = TimedJSONWebSignatureSerializer(secret_key)
        data = ser.loads(token)
        user = cls.query.filter_by(alternate_id=data["userid"]).one()
        return user        

    @classmethod
    def random_unique_alternateid(cls):
        randchoice = randint(cls.MIN_ALTERNATE_ID, cls.MAX_ALTERNATE_ID)
        rcquery = lambda s :  cls.query.filter_by(alternate_id=s).limit(1).first()
        while rcquery(randchoice) is not None:
            randchoice = randint(cls.MIN_ALTERNATE_ID, cls.MAX_ALTERNATE_ID)
        return randchoice



class RenderStyle(db.Model):
    __tablename__ = "renderstyle"
    styleid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=True)
    style = db.Column(db.PickleType)
    userid = db.Column(db.Integer, db.ForeignKey("user.userid"))
    user = db.relationship("User", backref=db.backref("styles"), foreign_keys=[userid])
    styleversion = db.Column(db.Integer,  default=1, nullable=False, server_default="1")
    is_removable = db.Column(db.Boolean, default=True)
    

class CoordType(enum.IntEnum):
    OVERWORLD = 1,
    NETHER = 2,
    END = 3,
    UNDEFINED = 0

POI_NAME_LOOKUP = {CoordType.OVERWORLD : "Overworld",
                   CoordType.NETHER : "The Nether",
                   CoordType.END : "The End",
                   CoordType.UNDEFINED : "undefined"}



poi_tag_association = db.Table("poi_tag_association", db.metadata,
                            db.Column("poi_id", db.ForeignKey("pointofinterest.poiid"), primary_key=True),
                            db.Column("tag_id", db.ForeignKey("tag.tagid"), primary_key=True))


class PointOfInterest(db.Model):
    __tablename__ = "pointofinterest"
    poiid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda : datetime.now(timezone.utc))
    public = db.Column(db.Boolean, default=False)

    userid = db.Column(db.Integer, db.ForeignKey("user.userid"), nullable=False)
    user = db.relationship("User", backref=db.backref("pois"))
    styleid = db.Column(db.Integer, db.ForeignKey("renderstyle.styleid"))
    style = db.relationship("RenderStyle")
    
    coord_x = db.Column(db.Integer)
    coord_y = db.Column(db.Integer)
    coord_z = db.Column(db.Integer)
    
    coordtype = db.Column(Enum(CoordType, default=str(CoordType.UNDEFINED.value), nullable=False,
                               server_default=str(CoordType.OVERWORLD.value),
                               values_callable = lambda enum: [str(_.value) for _ in enum]))

    @property
    def coords(self):
        return (self.coord_x, self.coord_y, self.coord_z)
    
    @property
    def typename(self):
        return POI_NAME_LOOKUP[self.coordtype]
    
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
                "coord" : self.coords,
                "coord_type" : POI_NAME_LOOKUP[self.coordtype]
                }

class Tag(db.Model):
    __tablename__ = "tag"
    tagid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), nullable=False, default= lambda: datetime.now(timezone.utc))
    
    userid = db.Column(db.Integer, db.ForeignKey("user.userid"), nullable=False)
    owning_user = db.relationship("User", backref=db.backref("tags"))
    style = db.Column(db.Integer, db.ForeignKey("renderstyle.styleid"))
    
    pois = db.relationship("PointOfInterest", secondary=poi_tag_association, backref="tags")


def get_db(app):
    db.init_app(app)
    return db

DEFAULT_STYLE = {"marker.symbol" : "circle",
                 "marker.size" : 10,
                 "marker.color" : "#3584E4",
                 "marker.line.width" : 0,
                 "marker.opacity" : 0.7,
                 "marker.line.color" : "#000000"}

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


    print("creating default render style")
    default_style = RenderStyle(name="default", style=DEFAULT_STYLE,
                                user=admin_user, is_removable=False)
    db.session.add(default_style)
    db.session.commit()
    


@click.command("create-db")
@click.argument("admin_pass")
@with_appcontext
def create_db_command(admin_pass):
    from flask import current_app
    db.init_app(current_app)
    create_db(admin_pass, db)
    migdir = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + "migrations"
    stamp(directory=migdir)
    


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

    

