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


from flask_login import LoginManager
from flask import g
from .db import User
from flask import jsonify, current_app
from itsdangerous import BadSignature, SignatureExpired

lman = LoginManager()
@lman.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))

@lman.request_loader
def request_loader(request):
    token = request.args.get("token")
    if not token:
        #try header based auth
        token = request.headers.get("Authorization")
        if token:
            token = token.replace("Basic ", "", 1)
    
    if token:
        try:
            usr = User.verify_api_token(current_app, token)
            return usr
        except BadSignature:
            g.login_error_str = "bad signature in JWT"
            return None
        except SignatureExpired:
            g.login_error_str = "JWT signature expired"
    else:
        g.login_error_str = "no API token provided"
        return None


lman.login_message = "you need to login to perform this action"
lman.login_message_category = "flash-error"
lman.login_view = "login"
