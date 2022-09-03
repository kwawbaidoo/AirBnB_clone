#!/usr/bin/env python3
"""Console.py -> Command Line with cmd Module
"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models import storage

class HBNBCommand(cmd.Cmd):
	"""
	Class that uses cmd module to implement a built in interpreter
	"""
	prompt = "(hbnb) "
	
	model_list = ["BaseModel", "User", "City", "State", "Place", "Amenity", "Review"]

	def precmd(self, args):
		"""
		This function runs before the onecmd and 
		It is overridden to account for our dots notation for all 
		commands
		"""
		if "." in args:
			result = args.replace(".", " ").replace(",", " ").replace("(", " ") \
					.replace(")", " ")
			result = result.split(" ")
			result[0] , result[1] = result[1], result[0]
			result = " ".join(result)
		return super().precmd(result)
		

	@classmethod
	def handle_errors(cls, args, **kwargs):
		"""
		Handles Errors in our command line inputs
		"""

		if "all" in kwargs.values():
			if not args:
				return False
		if not args:
			print("** class name missing **")
			return True
		else:
			args = args.split(" ")
		n = len(args)
		if args[0] not in HBNBCommand.model_list:
			print("** class doesn't exist **")
			return True

		if 'command' not in kwargs:
			return False

		for argument in kwargs.values():
			if argument in ["show", "destroy"]:
				if n < 2:
					print("** instance id missing **")
					return True
			if argument == "update":
				if n < 2:
					print("** instance id missing **")
					return True
				elif n < 3:
					print("** attribute name missing **")
					return True
				elif n < 4:
					print("** value missing **")
					return True

		return False


	def do_quit(self, args):
                """
                This command quits the interpreter
                """
                return True

	def do_EOF(self, args):
		"""
		Quits the interpreter: press (cntr+D) to run EOF
		"""
		return True

	def emptyline(self):
		"""
		Overridden to prevent it from repeating the last nonempty 
		command entered
		"""
		return False

	def onecmd(self, args):
		"""
		This function picks out the function from the command line 
		args in order to execute
		Has been overridden to account for quit and EOF separately
		Has been overridden to account for other functions
		"""

		if args == "quit":
			return self.do_quit(args)
		elif args == "EOF":
			return self.do_EOF(args)
		else:
			cmd.Cmd.onecmd(self, args)
	
	
	def do_create(self, args):
		"""
		Creates a new instance of BaseModel, saves it (to the JSON file)
		and prints the id.
		$ create <model>
		
		Errors ->
		If the class name is missing, print ** class name missing ** 
		$ create
		If the class name doesn’t exist, print ** class doesn't exist ** 
		$ create MyModel
		"""
		
		error = HBNBCommand.handle_errors(args)
		if error:
			return

		obj = eval(args)()	
		obj.save()
		print(obj.id)


	def do_show(self, args):
		"""
		Prints the string representation of an instance based on the class 
		name and id
		$ show <model> <id>
		
		Errors ->
		If the class name is missing, print ** class name missing **
		$ show
		If the class name doesn’t exist, print ** class doesn't exist **
		$ show MyModel
		If the id is missing, print ** instance id missing **
		$ show BaseModel
		If the instance of the class name doesn’t exist for the id,
		print ** no instance found *
		$ show BaseModel 121212
		"""		

		error = HBNBCommand.handle_errors(args, command = "show")
		if error:
			return
		args = args.split(" ")
		objects = storage.all()
		key = ".".join(args)
		obj = objects.get(key)
		if obj:
			print(obj)
		else:
			print("** no instance found **")


	def do_destroy(self, args):
		"""
		Deletes an instance based on the class name and id 
		(save the change into the JSON file)
		$ destroy <model> <id>

		Error->
		If the class name is missing, print ** class name missing **
		$ destroy
		If the class name doesn’t exist, print ** class doesn't exist **
		$ destroy MyModel
		If the id is missing, print ** instance id missing **
		$ destroy BaseModel
		If the instance of the class name doesn’t exist for the id,
		print ** no instance found **
		$ destroy BaseModel 121212
		"""

		error = HBNBCommand.handle_errors(args, command = "destroy")
		if error:
			return
		args = args.split(" ")
		key == ".".join(args)
		
		objects = storage.all()
		
		if key in objects and storage.delete(objects[key]):
			pass
		else:
			print("** no instance found **")


	def do_all(self, args):
		"""
		Prints all string representation of all instances 
		based or not on the class name
		$ all <model>
		$ all
		
		Errors->
		The printed result must be a list of strings
		If the class name doesn’t exist, print ** class doesn't exist **
		$ all MyModel
		"""

		error = HBNBCommand.handle_errors(args, command = "all")
		if error:
			return
		args = args.split(" ")
		objects = storage.all()
		if args[0] == "":
			for obj in objects.values():
				print(obj)
		else:
			for key in objects:
				k = key.split(".")
				if k[0] == args[0]:
					print(objects[key])
			

	def do_update(self, args):
		"""
		Updates an instance based on the class name and id by adding or 
		updating attribute (save the change into the JSON file)
		$ update <model> <id> <attribute name> "<attribute value>"
		Only one attribute can be updated at the time
		You can assume the attribute name is valid (exists for this model)
		The attribute value must be casted to the attribute type

		Error->
		If the class name is missing, print ** class name missing **
		$ update
		If the class name doesn’t exist, print ** class doesn't exist **
		$ update MyModel
		If the id is missing, print ** instance id missing **
		$ update BaseModel
		If the instance of the class name doesn’t exist for the id,
		print ** no instance found **
		$ update BaseModel 121212
		If the attribute name is missing, print ** attribute name missing **
		$ update BaseModel existing-id
		If the value for the attribute name doesn’t exist, print ** value missing **
		$ update BaseModel existing-id first_name
		All other arguments should not be used
		$ update BaseModel 1234-1234-1234 email "aibnb@mail.com" first_name "Betty" =
		$ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
		id, created_at and updated_at cant’ be updated
		"""

		error = HBNBCommand.handle_errors(args, command = "update")
		
		if error:
			return

		args = args.split(" ")
		class_name = args[0]
		id = args[1]
		attr_name = args[2]
		attr_value = args[3]
		if "\"" in attr_value:
			attr_value = attr_value[1:-1]

		if attr_value.isdigit():
			attr_value = int(attr_value)

		objects = storage.all()
		key = f"{class_name}.{id}"

		for k in objects:
			if k == key:
				obj = objects[k]
				setattr(obj, attr_name, attr_value)
				obj.save()
				return
		print("** instance id not found **")


	def do_count(self, args):
		"""
		Gives the count of a particular model or instance
		$ count <model>
		
		Error->
		"""
		if HBNBCommand.handle_errors(args, command = "count"):
			return
		count = 0
		args = args.split(" ")
		obj = storage.all()
		
		key = args[0]
		for item in obj:
			if key in item:
				count += 1
		print(count)



if __name__ == "__main__":
	HBNBCommand().cmdloop()
