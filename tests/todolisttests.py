#!/usr/bin/env python

import json
import os
import unittest
import sys
sys.path.append(os.pardir)
import todolist

class TodoListTests(unittest.TestCase):

	def setUp(self):
		self.testdata = open("./testdata.json", "r")
		self.testdata_text = self.testdata.read()
		self.testdata.close()

	def tearDown(self):
		try:
			os.remove("./todo.json")
		except OSError:
			# File not created, no need to delete.
			pass

	def create_data_file(self):
		datafile = open("./todo.json", "w")
		datafile.write(self.testdata_text)
		datafile.close()

	def create_todolist_and_safe_list(self):
		self.create_data_file()
		self.todolist = todolist.TodoList("./todo.json")
		self.list = json.loads(self.testdata_text)

	def get_data_file_as_string(self):
		self.testdata = open("./todo.json", "r")
		string = self.testdata.read()
		self.testdata.close()
		return string

	def test_load(self):
		self.create_todolist_and_safe_list()
		for item in self.list:
			self.assert_(item in self.todolist)

	def test_save(self):	
		self.create_todolist_and_safe_list()
		self.todolist.save()
		newfile_text = self.get_data_file_as_string()
		self.assertEquals(newfile_text, self.testdata_text)


	def test_contains(self):
		self.create_todolist_and_safe_list()
		self.assert_({"text": "Sometext", "id": 2} in self.todolist)

	def test_add(self):
		self.create_todolist_and_safe_list()
		self.todolist.add("Some item")
		self.todolist.add("Some other item")

		self.assert_({'id':7, 'text': "Some item"} in self.todolist)
		self.assert_({'id':8, 'text': "Some other item"} in self.todolist)

	def test_remove(self):
		self.create_todolist_and_safe_list()
		self.todolist.remove(2)
		self.assert_({"text": "Sometext", "id": 2} not in self.todolist)

	def test_loop(self):
		self.create_todolist_and_safe_list()
		test_list = []
		for item in self.todolist:
			test_list.append(item)

		self.assertEquals(test_list, self.list)

	def test_string(self):
		self.create_todolist_and_safe_list()
		self.assertEquals(str(self.todolist), '1\tAdd multiple lists, and removal functionality to GUI\n2\tSometext\n3\tSome text\n4\tTesting\n5\tAnother Item\n6\tFor the note list')

	def test_len(self):
		self.create_todolist_and_safe_list()
		self.assertEquals(len(self.todolist), 6)

	def test_get_by_id(self):
		self.create_todolist_and_safe_list()
		self.assertEquals({"text": "Sometext", "id": 2}, self.todolist[2])

	def test_get_by_id_out_of_bounds(self):
		self.create_todolist_and_safe_list()
		self.assertRaises(IndexError, self.todolist.__getitem__, 27)

	def test_list_does_not_exist(self):
		self.assertRaises(todolist.NoSuchListError, todolist.TodoList, "fakey")

suite = unittest.TestLoader().loadTestsFromTestCase(TodoListTests)
unittest.TextTestRunner(verbosity=2).run(suite)
