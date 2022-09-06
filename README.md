# 0x00.AirBnB clone - The console
![AirBnB Image](https://camo.githubusercontent.com/29aee5323f56eeaf0ca03669b3181f360af907609dc764ab1c5006815a03f4ff/68747470733a2f2f692e696d6775722e636f6d2f4a4f68615a356d2e706e67)

### Introduction
The goal of this project is to deploy a simple copy of the [AirBnB](https://www.airbnb.com/) website on the server.
The project will cover some of the fundamental conceots of the higher level programming @ALX, we won't be implementing all the features for now.
Check @[alx-higher_level_programming](https://github.com/Keshtech2002/alx-higher_level_programming) for the concepts.

The project consists of the following parts:
1. Bulding the console to create a data model and manage data objects. Also store and persist them to a JSON file, essentially constituting a storage engine.
2. The static frontend using HTML/CSS and a web template for the objects.
3. MySQL database to replace the file storage engine and map the data models to tables in the database by using an ORM.
4. Creating a templating web framework by building a flask based python server that serve the static frontend with objects from the database or file storage engine.
5. Creating a RESTful API using flask for manipulating objects from the frontend.
6. Making the website dynamic by using JS and load objects using the REST API.

Each task is linked and will help you to:
- put in place a parent class (called BaseModel) to take care of the initialization, serialization and deserialization of your future instances
- create a simple flow of serialization/deserialization: Instance <-> Dictionary <-> JSON string <-> file
- create all classes used for AirBnB (User, State, City, Place…) that inherit from BaseModel
- create the first abstracted storage engine of the project: File storage.
- create all unittests to validate all our classes and storage engine

### Concepts
- Unittest - and please work all together on tests cases
- Python packages concept page
- Serialization/Deserialization
- \*args, \*\*kwargs
- datetime

### What’s a command interpreter?
Do you remember the Shell? It’s exactly the same but limited to a specific use-case. In our case, we want to be able to manage the objects of our project:
- Create a new object (ex: a new User or a new Place)
- Retrieve an object from a file, a database etc…
- Do operations on objects (count, compute stats, etc…)
- Update attributes of an object
- Destroy an object
The command interpreter leads to the console
BOB
### The console
The console is written in python using the [cmd](https://docs.python.org/3/library/cmd.html) module. It operates in interactive and non-interactive modes.
The console works like this in interactive mode:
```
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) 
(hbnb) 
(hbnb) quit
$
```
But also in non-interactive mode:
```
$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topiOOBc>):
========================================
EOF  help  quit
(hbnb) 
$OOB
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
$
```

### Some few commands

| command | Example |
| ------- | ------- |
| Run console | ```./console.py``` or ```python3 console.py``` |
| Quit the console | ```(hbnb) quit``` |
| Display the help for a command | ```(hbnb) help <command>``` |
| Create an object (prints its id) | ```(hbnb) create <class>``` |
| Show an object | ```(hbnb) show <class> <id>``` or ```(hbnb) <class>.show(<id>)``` |
| Destroy an object | ```(hbnb) destroy <class> <id>``` or ```(hbnb) <class>.destroy(<id>)``` |
| Show all objects, or all instances of a class | ```(hbnb) all``` or ```(hbnb) all <class>``` |
| Update an attribute of an object | ```(hbnb) update <class> <id> <attribute name> "<attribute value>"``` or ```(hbnb) <class>.update(<id>, <attribute name>, "<attribute value>")``` |


- All tests should also pass in non-interactive mode: ```$ echo "python3 -m unittest discover tests" | bash```
