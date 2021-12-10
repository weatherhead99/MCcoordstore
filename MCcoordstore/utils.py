#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 21:28:26 2021

@author: danw
"""

from .db import PointOfInterest
import json

def serialize_pois(app, db):
    pois = PointOfInterest.query.all()
    poilist = [_.serialize_to_dict() for _ in pois]
    return json.dumps(poilist)



    
    
    
    
    