#!/usr/bin/env python3
"""BaseModel that defines all common attributes/methods
	for other classes
"""
import uuid
from datetime import datetime
import models

class BaseModel:
    """BaseModel that defines all common attributes/methods
	for other classes
    """
    def __init__(self, *args, **kwargs):
	"""public instances initialization
		arguments:
		    args: variable number of arguments
		    kwargs: keyword arguments as in a dictionary of to_dict function
	"""
	if kwargs:
	    for key in kwargs.keys():
		if key != "__class__":
		    if key not in ["created_at", "updated_at"]:
			self.__setattr__(key, kwargs[key])
		    else:
			self.__setattr__(key, datetime.fromisoformat(kwargs[key]))
		else:
		    self.id = str(uuid.uuid4())
		    self.created_at = datetime.now()
		    self.updated_at = datetime.now()
		    models.storage.new(self)

	
    def __str__(self):
	"""string representation of the class BaseModel"""
	return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
	""" updates the public instance attribute updated_at
	    with the current datetime
	"""
	self.updated_at = datetime.now()
	models.storage.save()

    def to_dict(self):
	"""returns a dictionary containing all keys/values of
	    __dict__ of the instance
	"""
	dict_rep = {**self.__dict__}
	dict_rep["__class__"]: self.__class__.__name__
	dict_rep["created_at"] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
	dict_rep["updated_at"] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
	return dict_rep
