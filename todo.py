#!/usr/bin/python

import json
import os
import sys


json_folder = os.path.expanduser("~") + "/.todopy/"
json_location = json_folder + "todo.json"

class Todo:

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

	def install(self):
		"""
		Sets up the data files for storing the todo list.
		"""
		os.mkdir(json_folder)
		json_file = open(json_location, "w")
		json_file.write("[]")
		json_file.close()

		print "TodoPy Installed"

	def add(self):
		"""
		Adds an item to the todo list.
		"""
		text = ' '.join(sys.argv[2:])
		todo_list = TodoList()
		todo_list.add(text)
		todo_list.save()

		print
		print "Added:", text
		print

	def remove(self):
		"""
		Removes an item from the todo list by ID
		"""
		id = int(sys.argv[2])
		todo_list = TodoList()
		removed_text = todo_list.remove(id)
		todo_list.save()
		

		print
		print "Removed", removed_text
		print

	def list(self):
		"""
		Prints out the todo list
		"""
		print TodoList()

	def help(self):
		"""
		Prints out help information
		"""
		print
		print "Usage:"
		print "\t add <message> \t- Adds a message to the todo list"
		print "\t list \t\t- Lists all current todo items"
		print "\t remove <ID> \t- Removes the todo item with the specified ID"
		print "\t install \t- Sets up the data files needed to run the script"
		print

class TodoList:
	
	def __init__(self):
		"""
		Sets up the list.
		"""
		self.load()

	def add(self, text):
		"""
		Adds an item to the list
		"""
		try:
			last_id = self.list[-1]['id']
		except IndexError:
			# No items in list
			last_id = 1

		new_item = {'id': last_id + 1, 'text': text}
		self.list.append(new_item)

	def __str__(self):
		string = ""
		for item in self.list:
			string = string + str(item['id']) + "\t" + str(item['text']) + "\n"
		string = string[:-1] # Cut out final newline
		return string
			

	def remove(self, id):
		"""
		Removes an item from the list.
		"""
		for todo in self.list[:]:
			if todo['id'] == id:
				removed_text = self.list['id']
				self.list.remove(todo)
				return removed_text

		return "Nothing"

	def load(self):
		"""
		Loads the list data from file.
		"""
		json_file = open(json_location, "r")
		json_text = json_file.read()
		json_file.close()
		self.list = json.loads(json_text)

	def save(self):
		"""
		Writes the list data to file.
		"""
		json_file = open(json_location, "w")
		json_file.write(json.dumps(self.list))
		json_file.close()


Todo().run()
