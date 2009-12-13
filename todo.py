#!/usr/bin/python

import json
import sys

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

	def add(self):
		"""
		Adds an item to the todo list.
		"""
		json_file = open("./todo.json", "r")
		todo_list = json.loads(json_file.read())
		json_file.close()

		last_id = todo_list[-1]['id']

		new_item = {'id': last_id + 1, 'text': ' '.join(sys.argv[2:])}

		todo_list.append(new_item)

		json_file = open("./todo.json", "w")
		json_file.write(json.dumps(todo_list))
		json_file.close()

		print
		print "Added:", new_item['text']
		print

	def remove(self):
		"""
		Removes an item from the todo list by ID
		"""
		json_file = open("./todo.json", "r")
		todo_list = json.loads(json_file.read())
		json_file.close()

		for todo in todo_list[:]:
			if todo['id'] == int(sys.argv[2]):
				removed_text = todo['text']
				todo_list.remove(todo)

		json_file = open("./todo.json", "w")
		json_file.write(json.dumps(todo_list))
		json_file.close()

		print
		print "Removed", removed_text
		print

	def list(self):
		"""
		Prints out the todo list
		"""
		json_file = open("./todo.json", "r")
		json_text = json_file.read()
		json_file.close()
		todo_list = json.loads(json_text)
		
		print
		for todo in todo_list:
			print todo['id'], "\t", todo['text']
		print

	def help(self):
		"""
		Prints out help information
		"""
		print
		print "Usage:"
		print "\t add <message> \t- Adds a message to the todo list"
		print "\t list \t\t- Lists all current todo items"
		print "\t remove <ID> \t- Removes the todo item with the specified ID"
		print

Todo().run()
