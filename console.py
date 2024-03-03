#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User


def parse(arg: str):
    """Splits lines by spaces"""
    args = split(arg)
    return args, len(args)


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """
    prompt = '(hbnb) '
    __classes = {"BaseModel", "User"}

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Called when an empty line is entered"""
        pass

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argl, lenC = parse(arg)
        if lenC == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            instance = eval(argl[0])()
            print(instance.id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argl, lenC = parse(arg)
        if lenC == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif lenC < 2:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            match_id = False
            for obj in all_objs.keys():
                inst_name, id_inst = obj.split(".")
                if (inst_name == argl[0] and id_inst == argl[1]):
                    obj_show = all_objs[obj]
                    print(obj_show)
                    match_id = True
            if (not match_id):
                print("** no instance found **")

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argl, lenC = parse(arg)
        if lenC == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif lenC < 2:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            match_id = False
            for obj in all_objs.keys():
                inst_name, id_inst = obj.split(".")
                if (inst_name == argl[0] and id_inst == argl[1]):
                    del all_objs[obj]
                    match_id = True
                    storage.save()
                    break
            if (not match_id):
                print("** no instance found **")

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argl, lenC = parse(arg)
        all_objs = storage.all()
        if lenC == 0:
            str_obj = [str(value) for value in all_objs.values()]
            print(str_obj)
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            str_obj = [str(value) for value in all_objs.values()
                       if argl[0] == value.__class__.__name__]
            print(str_obj)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl, lenC = parse(arg)
        if lenC == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif lenC < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(argl[0], argl[1])
            if key not in objects:
                print("** no instance found **")
            elif len(argl) < 3:
                print("** attribute name missing **")
            elif len(argl) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                attr_name = argl[2]
                attr_value = argl[3]
                try:
                    attr_value = eval(attr_value)
                except Exception:
                    pass
                setattr(obj, attr_name, attr_value)
                obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
