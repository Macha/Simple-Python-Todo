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
		
		self.textview_display = createTextView(280, 200, False)
		sw_display.add(self.textview_display)
		self.textview_display.get_buffer().set_text(self.todolist.idLessString())
		
		self.textview_display.show()
		
		hbox_note_area.pack_start(sw_display)
		sw_display.show()

		# Set up the text view for adding new notes
		sw_add = gtk.ScrolledWindow()
		sw_add.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		self.textview_add = createTextView(230, 80)
		self.textview_add.connect("key_press_event", self.key_pressed)
		sw_add.add(self.textview_add)
		self.textview_add.show()
		
		hbox_send_area.pack_start(sw_add)
		sw_add.show()

		hbox_send_area.pack_start(send_button)
		send_button.show()


		# Organise the boxes
		vbox.pack_start(hbox_note_area)
		hbox_note_area.show()
		vbox.pack_start(hbox_send_area)
		hbox_send_area.show()
		self.window.add(vbox)
		vbox.show()

		self.window.connect("delete_event", self.delete_event)
		self.window.show()

	def main(self):
		"""
		Starts the Todo GUI
		"""
		gtk.main()

	def delete_event(self, widget, event, Data=None):
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
		self.todolist.add(note)
		self.textview_add.get_buffer().set_text("")
		displaybuffer = self.textview_display.get_buffer()
		displaybuffer.insert(displaybuffer.get_end_iter(), note)

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
