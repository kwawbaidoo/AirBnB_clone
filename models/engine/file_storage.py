#!/usr/bin/env python3
"""file_storage.py
	FileStorage class that serializes instances to a JSON file 
	and deserializes JSON file to instances
"""
import json
from models.base_model import BaseModel
from models.user import User
class FileStorage:
    """FileStorage that serializes instances to a JSON file
    and deserializes JSON file to instances
    private class attributes:
	__file_path string
	__objects dictionary
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
	"""Returns the dictionary __objects"""
	return FileStorage.__objects
	
    def new(self, obj):
	"""sets in __objects the obj with key <obj class name>.id"""
	key = f"{obj.__class__.__name__}.{obj.id}"
	FileStorage.__objects[key] = obj

    def save(self):
	"""serializes __objects to the JSON file (path: __file_path)"""
	to_dict = {}
	for key, obj in FileStorage.__objects.items():
	    to_dict[key] = obj.to_dict()
	with open(FileStorage.__file_path, "w") as f:
	    json.dump(to_dict, f)

    def reload(self):
	"""deserializes the JSON file to __objects
	(only if the JSON file (__file_path) exists
	otherwise, do nothing. If the file doesn’t exist,
	no exception should be raised)
	"""
	try:
	    with open(FileStorage.__file_path, "r") as f:
		_dict = json.load(f)
	    new_dict = {}
	    for obj_name, obj_details in _dict.items():
		class_name = obj_name.split(".")[0]
		obj = eval(class_name)(**obj_details)
		new_dict[obj_name] = obj
		FileStorage.__objects = new_dict
	except FileNotFoundError:
	    pass

    def delete(self, obj):
	class_name = obj.__class__.__name__
	id = obj.id
	key = f"{class_name}.{id}"
		
	if key in FileStorage.__objects:
	    del FileStorage.__objects[key]
	    self.save()
	    return True
	return False		
