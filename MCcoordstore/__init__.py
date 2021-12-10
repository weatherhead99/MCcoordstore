from flask import Flask
import os
from typing import Dict, Any
from .db import create_db_command



def create_app(test_config: Dict[str, Any]=None):
    app = Flask(__name__, instance_relative_config=True)
    
    default_db_path = os.path.join(app.instance_path, "mccoordstore.sqlite")
    
    
    app.config.from_mapping(SECRET_KEY="dev",
                            SQLALCHEMY_DATABASE_URI=f"sqlite:///{default_db_path}")
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.cli.add_command(create_db_command)
    

    return app


    
    