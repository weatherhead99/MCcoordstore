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


from flask import Blueprint, jsonify, current_app, request
from flask.blueprints import BlueprintSetupState
from flask_login import LoginManager, login_required, current_user
from .db import User
import base64
from MCcoordstore import db


poi_api = Blueprint("poi", __name__)


@poi_api.route("/gettoken")
@login_required
def get_token():
    if current_user is None:
        return jsonify({"error" : "Require logged in user to get API token"})
    
    token = current_user.generate_api_token(current_app)
    
    return jsonify({"token" : token,
                    "error" : ""})

@poi_api.route("/")
@login_required
def list_pois():
    
    print("listing_pois")
    return jsonify({"error" : "not implemented yet!"})
    