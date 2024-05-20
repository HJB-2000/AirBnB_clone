#!/usr/bin/python3

import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """
    Parse the argument string.

    Args:
        arg (str): The argument string.

    Returns:
        list: A list of parsed arguments.
    """
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """
        Do nothing on empty input.
        """
        pass

    def default(self, arg):
        """
        Handle default command.

        Args:
            arg (str): The argument string.

        Returns:
            bool: True if the command is handled successfully, False otherwise.
        """
        commands = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            parts = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", parts[1])
            if match is not None:
                command_parts = [parts[1][:match.span()[0]],
                                 match.group()[1:-1]]
                if command_parts[0] in commands.keys():
                    call = "{} {}".format(parts[0], command_parts[1])
                    return commands[command_parts[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """
        Quit command to exit the program.
        """
        return True

    def do_EOF(self, arg):
        """
        EOF signal to exit the program.
        """
        print("")
        return True

    def do_create(self, arg):
        """
        Create a new class instance and print its id.

        Usage: create <class>
        """
        parts = parse(arg)
        if len(parts) == 0:
            print("** class name missing **")
        elif parts[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(parts[0])().id)
            storage.save()

    def do_show(self, arg):
        """
        Display the string representation of a class instance of a given id.

        Usage: show <class> <id>
        """
        parts = parse(arg)
        object_dict = storage.all()
        if len(parts) == 0:
            print("** class name missing **")
        elif parts[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(parts) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(parts[0], parts[1]) not in object_dict:
            print("** no instance found **")
        else:
            print(object_dict["{}.{}".format(parts[0], parts[1])])

    def do_destroy(self, arg):
        """
        Delete a class instance of a given id.

        Usage: destroy <class> <id>
        """
        parts = parse(arg)
        object_dict = storage.all()
        if len(parts) == 0:
            print("** class name missing **")
        elif parts[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(parts) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(parts[0], parts[1]) not in object_dict.keys():
            print("** no instance found **")
        else:
            del object_dict["{}.{}".format(parts[0], parts[1])]
            storage.save()

    def do_all(self, arg):
        """
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.

        Usage: all [<class>]
        """
        parts = parse(arg)
        if len(parts) > 0 and parts[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(parts) > 0 and parts[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(parts) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """
        Retrieve the number of instances of a given class.

        Usage: count instances of <class> or use <class>.count()
            to get the total count.
        """
        parts = parse(arg)
        i = 0
        for obj in storage.all().values():
            if parts[0] == obj.__class__.__name__:
                i += 1
        print(i)

    def do_update(self, arg):
        """
        Update a class instance identified by <id> by adding or updating
        an attribute specified by <attribute_name> with <attribute_value>,
        or by updating attributes using a dictionary.

        Usage: update <class> <id> <attribute_name> <attribute_value> or
            <class>.update(<id>, <attribute_name>, <attribute_value>) or
            <class>.update(<id>, <dictionary>)
        """
        parts = parse(arg)
        object_dict = storage.all()

        if len(parts) == 0:
            print("** class name missing **")
            return False
        if parts[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(parts) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(parts[0], parts[1]) not in object_dict.keys():
            print("** no instance found **")
            return False
        if len(parts) == 2:
            print("** attribute name missing **")
            return False
        if len(parts) == 3:
            try:
                type(eval(parts[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(parts) == 4:
            obj = object_dict["{}.{}".format(parts[0], parts[1])]
            if parts[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[parts[2]])
                obj.__dict__[parts[2]] = valtype(parts[3])
            else:
                obj.__dict__[parts[2]] = parts[3]
        elif type(eval(parts[2])) == dict:
            obj = object_dict["{}.{}".format(parts[0], parts[1])]
            for key, value in eval(parts[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in
                        {str, int, float}):
                    valtype = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = valtype(value)
                else:
                    obj.__dict__[key] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
