#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 16:51:02 2021

@author: danw
"""

from flask_restless import Serializer
from flask_login import current_user
from .db import PointOfInterest, User
from typing import Dict
from sqlalchemy import inspect
from abc import abstractmethod

class APISerializer(Serializer):
    DB_MODEL_CLASS = None
    def __init__(self):
        if self.DB_MODEL_CLASS is None:
            raise TypeError("no DB_MODEL_CLASS defined")
        self._inspector = inspect(self.DB_MODEL_CLASS)
        
    @abstractmethod
    def _init_override(self):
        pass

class POISerializer(APISerializer):
    
        
        
    @property
    def attributes_columns(self):
        return set(self.attributes)
    
    @property
    def relationships_columns(self):
        return set(self.relationships)
    
    def serialize(instance: PointOfInterest, only=None) -> Dict:
        pass

