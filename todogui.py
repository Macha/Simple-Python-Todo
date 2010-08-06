#!/usr/bin/env python
from todolist import *
import glob
import os
import sys

import pygtk
pygtk.require('2.0')
import gtk
import pango


json_folder = os.path.expanduser('~') + '/.todopy/'

class TodoGUI:

	lists = {}

	def __init__(self):
		"""
		Creates the GUI display.
		"""
		
		# Initialise default list.
		# TODO: Support multiple lists
		self.todolist = TodoList(json_folder + 'todo.json')

		# Start of multiple lists support. Currently unused
		for infile in glob.glob( os.path.join(json_folder, '*.json') ):
			listname = infile.replace(json_folder, '').replace('.json', '')
			self.lists[listname] = TodoList(infile)
			print 'Found:', infile.replace(json_folder, '').replace('.json', '')

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title('Simple Python Todo')
	
		send_button = gtk.Button(None, gtk.STOCK_ADD)
		send_button.connect('clicked', self.send_button_clicked)

		vbox = gtk.VBox(False, 10)
		vbox.set_border_width(10)

		hbox_note_area = gtk.HBox(False, 0)
		hbox_send_area = gtk.HBox(False, 0)

		self.current_list = ListPanel(self.todolist)
		sw_display = self.current_list.sw
		hbox_note_area.pack_start(sw_display)

		# Set up the text view for adding new notes
		sw_add = gtk.ScrolledWindow()
		sw_add.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		self.textview_add = self.create_text_view(230, 80)
		self.textview_add.connect('key_press_event', self.textbox_key_pressed)
		sw_add.add(self.textview_add)
		
		hbox_send_area.pack_start(sw_add)
		hbox_send_area.pack_start(send_button)


		# Organise the boxes
		vbox.pack_start(hbox_note_area)
		hbox_note_area.show()
		vbox.pack_start(hbox_send_area)
		hbox_send_area.show()
		self.window.add(vbox)

		self.window.connect('delete_event', self.delete_event)
		self.window.show_all()

	def main(self):
		"""
		Starts the Todo GUI
		"""
		gtk.main()



	def delete_event(self, widget, event, Data=None):
		"""
		Saves the list and closes the app.
		"""
		self.todolist.save()
		gtk.main_quit()
		return False

	def textbox_key_pressed(self, widget, event, Data=None):
		"""
		Checks if enter was pressed, and if so, adds a new item
		"""
		if event.keyval == gtk.gdk.keyval_from_name('Return') or \
		event.keyval == gtk.gdk.keyval_from_name('KP_Enter'):
			self.add_item_to_list(self.current_list)
			return True		

	def send_button_clicked(self, widget, event, Data=None):
		"""
		Adds a new item when the send button is clicked.
		"""
		self.add_item_to_list(self.current_list)
		return True

	def add_item_to_list(self, todolist):
		"""
		Copies the text from the entry box to a todolist.
		"""
		note = self.get_all_text_view_text(self.textview_add)
		todolist.add_item(note)
		self.textview_add.get_buffer().set_text('')

	def create_text_view(self, width=200, height=200, editable=True, wrap=True):
		"""
		Creates a text view with certain settings.
		"""
		textview = gtk.TextView()
		textview.set_size_request(width, height)

		if wrap is True:
			textview.set_wrap_mode(gtk.WRAP_WORD)

		textview.set_editable(editable)
		# Don't show cursor in uneditable text views.
		textview.set_cursor_visible(editable)

		return textview

	def get_all_text_view_text(self, textview):
		"""
		Gets all the text from a text view.
		"""
		textbuffer = textview.get_buffer()
		startiter, enditer = textbuffer.get_bounds()
		text = startiter.get_slice(enditer)
		return text

class ListPanel:

	def __init__(self, todolist):
		"""
		Set up the tree view for showing a todo list.
		"""
		self.todolist = todolist
		self.selection_id = None;
		
		
		self.store = self.create_model(todolist)
		self.display_view = gtk.TreeView(self.store)
		self.display_view.set_size_request(280, 200)
		self.display_view.set_rules_hint(True)
		
		self.display_view.connect('key_press_event', self.key_pressed)

		selection = self.display_view.get_selection()
		selection.connect("changed", self.selection_changed)
		selection.set_mode(gtk.SELECTION_SINGLE)

		self.create_columns(self.display_view)
		
	
		self.sw = gtk.ScrolledWindow()
		self.sw.add(self.display_view)
		self.sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

	def create_model(self, todolist):
		"""
		Sets up the store for the TreeView
		"""
		store = gtk.ListStore(int, str)

		for todo in todolist:
			new_row = (todo.id, todo.text)
			print new_row
			store.append(new_row)

		return store
	
	def create_columns(self, tree_view):
		"""
		Sets up the columns for the TreeView
		"""
		
		renderer_text = gtk.CellRendererText()
		renderer_text.props.wrap_width = 280
		renderer_text.props.wrap_mode = pango.WRAP_WORD
		column = gtk.TreeViewColumn('Text', renderer_text, text=1)
		column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_sort_column_id(0)
		tree_view.append_column(column)
	
	def add_item(self, text):
		"""
		Adds an item to the todo list.
		"""
		new_todo = self.todolist.add(text)
		self.store.append((new_todo.id, text))

	def remove_item(self, item_id):
		"""
		Remove an item from the list, and the display.
		"""
		self.todolist.remove(item_id) 
		store = self.store
		store.foreach(self.find_item_to_remove, item_id)
		#titer = store.get_iter_root()
		#while True:
		#	if store.get_path(titer)[0] == item_id:
		#		store.remove(titer)
		#		break
		#	else:
		#		titer = store.iter_next(titer)
		#		if titer is None:
		#			break

	def find_item_to_remove(self, model, path, iter, user_data):
		"""
		Finds and removes the correct item from the ListStore.
		"""
		if path[0] == user_data:
			model.remove(iter)
			return True

	def key_pressed(self, widget, event, Data=None):
		"""
		Deletes the item from the list if the delete key is pressed.
		""" 
		if event.keyval == gtk.gdk.keyval_from_name('Delete') and self.selection_id is not None:
			self.remove_item(self.selection_id)
			self.selection_id = None;
			return True

	def selection_changed(self, selection):
		"""
		Sets the currently selected items ID
		"""
		store, titer = selection.get_selected()
		if titer is not None:
			print store.get_path(titer)
			for item in store:
				print item[0], item[1]
			self.selection_id = store.get_value(titer, 0)

TodoGUI().main()
