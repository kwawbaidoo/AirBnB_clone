#!/usr/bin/python3
"""This module the defines the entry point
for the console command interpreter.
"""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBComand(cmd.Cmd):
    """
    Defines the HBNBCommand class for console implemantation
    Class that uses cmd module to implement a built in interpreter
    """
    prompt = "(hbnb) "

    class_model = (
        "BaseModel",
        "User",
        "City",
        "State",
        "Place",
        "Amenity",
        "Review"
        )

    str_dict = None

    @classmethod
    def striped(cls, arg):
        """Strips `arg` string of first and last character. """
        return arg[1:-1]

    def precmd(self, line):
        """
	This function runs before the onecmd and 
	It is overridden to account for our dots notation for all 
	commands
	"""
        if '.' in line:
            if '{' in line:
                dict_ = re.search("{([^}]*)}", line)
                if not dict_:
                    return cmd.Cmd().precmd(line)
                dict_ = dict_.group(0)
                HBNBComand.str_dict = eval(dict_)
                pass

            line_arg = line.replace('.', ' ').replace(', ', ' ')\
                .replace('(', ' ').replace(')', ' ')

            line_arg = line_arg.split()
            line_arg[0], line_arg[1] = line_arg[1], line_arg[0]
            if len(line_arg) > 2:
                if "\"" in line_arg[2]:
                    line_arg[2] = HBNBComand.striped(line_arg[2])
            line = ' '.join(line_arg)

        return cmd.Cmd().precmd(line)

    def do_quit(self, arg):
        """
        This command quits the interpreter
        """
        return True

    def do_EOF(self, arg):
        """
	Quits the interpreter: press (cntr+D) to run EOF
	"""
        return True

    def onecmd(self, line):
	"""
	This function picks out the function from the command line 
	args in order to execute
	Has been overridden to account for quit and EOF separately
	Has been overridden to account for other functions
	"""

	if args == "quit":
	    return self.do_quit(line)
	elif args == "EOF":
	    return self.do_EOF(line)
	else:
	    cmd.Cmd.onecmd(self, line)

    @classmethod
    def HBNBError(cls, line, command=None):
        """
	Handles Errors in our command line inputs
	"""
        args = line.split()
        if not args:
           print("** class name missing **")
            return True
        if args[0] not in HBNBComand.class_model:
            print("** class doesn't exist **")
            return True
        if len(args) < 2 and command not in ('create', 'all', 'count'):
            print("** instance id missing **")
            return True

        if command in ("show", "delete", "update"):
            obj = storage.all()
            key = f"{args[0]}.{args[1]}"
            _str = obj.get(key)
            if _str is None:
                print("** no instance found **")
                return True

        return False

    def do_create(self, line):
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
        args = line.split()
        if HBNBComand.HBNBError(line, "create"):
            return

        class_ = eval(args[0])
        obj_ = class_()
        print(obj_.__dict__["id"])
        storage.save()

    def do_show(self, line):
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
        args = line.split()
        if HBNBComand.HBNBError(line, "show"):
            return

        obj_dict = storage.all()
        key = f"{args[0]}.{args[1]}"
        _str = obj_dict.get(key)
        print(_str)

    def do_destroy(self, line):
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
        args = line.split()
        if HBNBComand.HBNBError(line,  "delete"):
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all()
        del (obj[key])
        storage.save()

    def do_all(self, line):
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
        args = line.split()
        _str = []
        obj = storage.all()

        if args:
            if HBNBComand.HBNBError(line, 'all'):
                return
            key = args[0]
            for item in obj:
                if key in item:
                    _str.append(str(obj.get(item)))

        else:
            for item in obj:
                _str.append(str(obj.get(item)))
        ", ".join(_str)
        print(_str)

    def do_update(self, line):
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
        args = line.split()

        if HBNBComand.HBNBError(line, "update"):
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        obj_dict = storage.all()
        key = f"{args[0]}.{args[1]}"
        item = obj_dict.get(key)

        if HBNBComand.str_dict:
            for key in HBNBComand.str_dict:
                value = HBNBComand.str_dict[key]
                setattr(item, key, value)
            HBNBComand.str_dict = None
        else:
            setattr(item, args[2], args[3])
        item.save()
        storage.save()

    def do_count(self, line):
        """
	Gives the count of a particular model or instance
	$ count <model>
	Error->
	"""
        if HBNBComand.HBNBError(line, "count"):
            return
        count = 0
        args = line.split()
        obj = storage.all()

        key = args[0]
        for item in obj:
            if key in item:
                count += 1
        print(count)
        storage.save()

    def emptyline(self):
        """
        Overridden to prevent it from repeating the last nonempty
	command entered
        Do nothing if empty line is passed
        """
        pass


if __name__ == "__main__":
    HBNBComand().cmdloop()
