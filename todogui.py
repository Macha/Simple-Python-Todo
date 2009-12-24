#!/usr/bin/env python
from todolist import *
import os
import sys

import pygtk
pygtk.require('2.0')
import gtk


json_folder = os.path.expanduser("~") + "/.todopy/"

class TodoGUI:
	def __init__(self):
		"""
		Creates the GUI display.
		"""
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("Simple Python Todo")
	
		send_button = gtk.Button(None, gtk.STOCK_ADD)

		vbox = gtk.VBox(False, 10)
		vbox.set_border_width(10)

		hbox_note_area = gtk.HBox(False, 0)
		hbox_send_area = gtk.HBox(False, 0)



		# Set up the text view for showing the notes
		sw_display = gtk.ScrolledWindow()
		sw_display.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		textview_display = createTextView(280, 200, False)
		sw_display.add(textview_display)
		textview_display.show()
		
		hbox_note_area.pack_start(sw_display)
		sw_display.show()

		# Set up the text view for adding new notes
		sw_add = gtk.ScrolledWindow()
		sw_add.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		textview_add = createTextView(230, 80)
		sw_add.add(textview_add)
		textview_add.show()
		
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
		gtk.main_quit()
		return False

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


TodoGUI().main()
