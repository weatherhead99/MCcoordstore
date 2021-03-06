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


from flask import Flask
import os
from typing import Dict, Any
from .db import create_db_command, change_pw_command, get_db
from flask_migrate import Migrate
from .api_poi import poi_api, setup_api
from .login import lman
from dynaconf import FlaskDynaconf, Validator

extra_file_env_var = "MCCOORDSTORE_CONFIG"


def create_app(test_config: Dict[str, Any] = None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        fls = ["mccoordstore.toml"]
        envfl = os.environ.get(extra_file_env_var)
        if envfl is not None:
            fls.append(envfl)

        FlaskDynaconf(app, settings_files="mccoordstore.toml",
                      validators=[Validator("secret_key", must_exist=True),
                                  Validator("sqlalchemy_database_uri", must_exist=True),
                                  Validator("sqlalchemy_track_modifications", default=False)])
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.cli.add_command(create_db_command)
    app.cli.add_command(change_pw_command)

    print("registering poi_api blueprint")
    app.register_blueprint(poi_api, url_prefix="/api")

    db = get_db(app)
    lman.init_app(app)
    Migrate(app, db, render_as_batch=True)

    with app.app_context():
        setup_api(app, db)
    return app

