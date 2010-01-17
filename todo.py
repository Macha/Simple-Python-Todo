#!/usr/bin/env python

from todolist import *
import os
import sys


json_folder = os.path.expanduser("~") + "/.todopy/"


class Todo:
	"""
	Allows a user to edit their todo list.
	"""

	def run(self):
		"""
		Runs the function with the same name as sys.argv[1]
		"""
		try:
			func = getattr(self, sys.argv[1])
		# Command not found
		except AttributeError:
			print "The command", sys.argv[1], "doesn't exist"
		# No action defined, show help
		except IndexError:
			self.help()
		else:
			if callable(func):
				try:
					func()
				except IndexError:
					print "Missing argument for command '" + sys.argv[1] + "' check help"
				except NoSuchListError:
					print "That list does not exist. Please try another list," \
						+ " or create the list using create <list>"

	def install(self):
		"""
		Sets up the data files for storing the todo list.
		"""
		os.mkdir(json_folder)
		create("todo", False)

		print
		print "Simple Python Todo Installed"
		print

	def create(self, print_output=True):
		"""
		Creates a new list.
		"""
		list_name = sys.argv[2]
		json_file = open(self.getListFilename(list_name), "w")
		json_file.write("[]")
		json_file.close()

		if print_output:
			print
			print "Created:", list_name
			print

	def delete(self):
		"""
		Deletes a list.
		"""
		
		list_name = sys.argv[2]
		os.remove(self.getListFilename(list_name))

		print
		print list_name, "removed"
		print

	def add(self):
		"""
		Adds an item to the todo list.
		"""
		text = ' '.join(sys.argv[2:])
		self.addto("todo", text)

	def addto(self, list_name="", text=""):
		"""
		Adds an item to the specified list.
		"""
		if list_name == "":
			list_name = sys.argv[2]
			text = ' '.join(sys.argv[3:])

		todo_list = TodoList(self.getListFilename(list_name))
		todo_list.add(text)
		todo_list.save()	

		print
		print "Added to:", list_name
		print "Added:", text
		print

	def done(self):
		"""
		Removes an item from the todo list by ID
		"""
		item_id = int(sys.argv[2])
		self.donein("todo", item_id)

	def donein(self, list_name="todo", item_id=-1):
		"""
		Removes an item from a certain list.
		"""
		if item_id < 0:
			list_name = sys.argv[2]
			item_id = int(sys.argv[3])


		todo_list = TodoList(self.getListFilename(list_name))
		removed_text = todo_list.remove(item_id)
		todo_list.save()

		print
		print "Removed from:", list_name
		print "Removed:", removed_text
		print
		
	def list(self, list_name="todo"):
		"""
		Prints out a todo list. If a list name is specified, prints that list,
		otherwise prints out the default, "todo" list.
		"""
		if len(sys.argv) > 2:
			list_name = sys.argv[2]

		print
		print TodoList(self.getListFilename(list_name))
		print

	def getListFilename(self, list_name):
		"""
		Gets the Filename for a list.
		"""
		filename = json_folder + list_name.lower() + ".json"
		return filename

	def help(self):
		"""
		Prints out help information
		"""
		print
		print "Usage (simple):"
		print "\t add <message> \t- Adds a message to the todo list"
		print "\t list \t\t- Lists all current todo items"
		print "\t done <ID> \t- Removes a finished todo item with the specified ID"
		print "\t install \t- Sets up the data files needed to run the script"
		print
		print "Usage (multiple lists):"
		print "\t addto <list> <message> \t - Adds a message to a certain list"
		print "\t list <list> \t\t\t - Prints out a certain list."
		print "\t donein <list> <ID> \t - Marks a message done in a certain list"
		print "\t create <list> \t\t\t - Creates a list with the name <list>"
		print "\t delete <list> \t\t\t - Deletes the list with the name <list>"
		print

Todo().run()
