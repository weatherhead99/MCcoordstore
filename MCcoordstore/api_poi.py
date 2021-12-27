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
from .db import User, PointOfInterest, RenderStyle
import base64
from MCcoordstore import db
from flask_restless import APIManager, ProcessingException
from .serializers import POISerializer

poi_api = Blueprint("poi", __name__)


@poi_api.route("/gettoken")
@login_required
def get_token():
    if current_user is None:
        return jsonify({"error" : "Require logged in user to get API token"})
    
    token = current_user.generate_api_token(current_app)
    
    return jsonify({"token" : token,
                    "error" : ""})
    

def api_auth_check(*args, **kwargs):
    if not current_user.is_authenticated:
        raise ProcessingException(detail="not authenticated", status=401)
        
def remove_nonpublic_collection_poi(filters, **kwargs):
    if not current_user.is_authenticated:
        filters.append({"name": "public", "op": "eq", "val" : True})

    
def setup_api(app, db):
    manager = APIManager(app, session=db.session)
    
    
    poi_preproc = {"GET_COLLECTION" : [remove_nonpublic_collection_poi],
                   "GET_RESOURCE" : [api_auth_check] }
    manager.create_api(PointOfInterest, methods=["GET"], collection_name="poi",
                       additional_attributes=["coords", "typename"], exclude=["coord_x","coord_y","coord_z", "tags", "poiid"],
                       preprocessors=poi_preproc)
    
    user_preproc = {"GET_COLLECTION" : [api_auth_check],
                    "GET_RESOURCE" : [api_auth_check]}
    
    manager.create_api(User, methods=["GET"],
                       exclude=["hashed_pw", "tags", "userid", "username"],
                       preprocessors=user_preproc)

    style_preproc = {"GET_COLLECTION" : [api_auth_check],
                     "GET_RESOURCE" : [api_auth_check]}
    manager.create_api(RenderStyle, methods=["GET"], collection_name="style",
                       exclude=["styleid"], preprocessors=style_preproc)
