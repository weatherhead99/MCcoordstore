from flask import Flask, g
import os
from typing import Dict, Any
from .db import create_db_command, User, change_pw_command, get_db
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config: Dict[str, Any]=None):
    app = Flask(__name__, instance_relative_config=True)
    
    default_db_path = os.path.join(app.instance_path, "mccoordstore.sqlite")
    
    
    app.config.from_mapping(SECRET_KEY="dev",
                            SQLALCHEMY_DATABASE_URI=f"sqlite:///{default_db_path}")
    
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.cli.add_command(create_db_command)
    app.cli.add_command(change_pw_command)
    
    
    lman = LoginManager()
    lman.login_view = "login"
    lman.init_app(app)
    
    @lman.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))
    
    
    db = get_db(app)
    migrate = Migrate(app,db)
    
    
    

    return app


    
    