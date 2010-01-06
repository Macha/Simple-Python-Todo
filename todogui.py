#!/usr/bin/env python
from todolist import *
import glob
import os
import sys

import pygtk
pygtk.require('2.0')
import gtk


json_folder = os.path.expanduser("~") + "/.todopy/"

class TodoGUI:

	lists = {}

	def __init__(self):
		"""
		Creates the GUI display.
		"""
		
		# Initialise default list.
		# TODO: Support multiple lists
		self.todolist = TodoList(json_folder + "todo.json")

		for infile in glob.glob( os.path.join(json_folder, '*.json') ):
			listname = infile.replace(json_folder, "").replace(".json", "")
			self.lists[listname] = TodoList(infile)
			print "Found:", infile.replace(json_folder, "").replace(".json", "")

		for k, v in self.lists.iteritems():
			print 
			print k
			print "------------"
			print v
			print


		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("Simple Python Todo")
	
		send_button = gtk.Button(None, gtk.STOCK_ADD)
		send_button.connect("clicked", self.add_item)

		vbox = gtk.VBox(False, 10)
		vbox.set_border_width(10)

		hbox_note_area = gtk.HBox(False, 0)
		hbox_send_area = gtk.HBox(False, 0)

		# Set up the text view for showing the notes
		sw_display = gtk.ScrolledWindow()
		sw_display.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		self.store = self.create_model()
		self.display_view = gtk.TreeView(self.store)
		self.display_view.set_size_request(280, 200)
		self.display_view.set_rules_hint(True)	
		self.create_columns(self.display_view)
		sw_display.add(self.display_view)
		
		hbox_note_area.pack_start(sw_display)

		# Set up the text view for adding new notes
		sw_add = gtk.ScrolledWindow()
		sw_add.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		self.textview_add = createTextView(230, 80)
		self.textview_add.connect("key_press_event", self.key_pressed)
		sw_add.add(self.textview_add)
		
		hbox_send_area.pack_start(sw_add)
		hbox_send_area.pack_start(send_button)


		# Organise the boxes
		vbox.pack_start(hbox_note_area)
		hbox_note_area.show()
		vbox.pack_start(hbox_send_area)
		hbox_send_area.show()
		self.window.add(vbox)

		self.window.connect("delete_event", self.delete_event)
		self.window.show_all()

	def main(self):
		"""
		Starts the Todo GUI
		"""
		gtk.main()

	def create_model(self):
		"""
		Sets up the store for the TreeView
		"""
		store = gtk.ListStore(int, str)

		for todo in self.todolist:
			store.append([todo['id'], todo['text']])

		return store

	def create_columns(self, tree_view):
		"""
		Sets up the columns for the TreeView
		"""
		
		renderer_text = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Text", renderer_text, text=1)
		column.set_sort_column_id(1)
		tree_view.append_column(column)

	def delete_event(self, widget, event, Data=None):
		"""
		Saves the list and closes the app.
		"""
		self.todolist.save()
		gtk.main_quit()
		return False

	def key_pressed(self, widget, event, Data=None):
		"""
		Checks if enter was pressed, and if so, adds a new item
		"""
		if event.keyval == gtk.gdk.keyval_from_name('Return') or \
		event.keyval == gtk.gdk.keyval_from_name('KP_Enter'):
			self.add_item()
			return True		
	
	def add_item(self, widget=None, Data=None):
		"""
		Adds an item to the todo list.
		"""
		note = getAllTextViewText(self.textview_add) + "\n"
		newid = self.todolist.add(note)
		self.textview_add.get_buffer().set_text("")
		self.store.append([newid, note])

def createTextView(width=200, height=200, editable=True, wrap=True):
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

def getAllTextViewText(textview):
	"""
	Gets all the text from a text view.
	"""
	textbuffer = textview.get_buffer()
	startiter, enditer = textbuffer.get_bounds()
	text = startiter.get_slice(enditer)
	return text

TodoGUI().main()
