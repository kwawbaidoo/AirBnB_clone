#!/usr/bin/env python3
"""User.py
with a User() class that inherits from BaseModel
"""

from models.base_model import BaseModel

class User(BaseModel):
	"""User Class Inherit from BaseModel"""
	email = ""
	password = ""
	first_name = ""
	last_name = ""
