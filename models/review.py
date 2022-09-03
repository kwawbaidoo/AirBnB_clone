#!/usr/bin/env python3
"""review.py
"""
from models.base_model import BaseModel

class Review(BaseModel):
	"""Review class inherit from BaseModel"""
	place_id = ""
	user_id = ""
	text = ""
