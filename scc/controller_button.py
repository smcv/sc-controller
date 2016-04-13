#!/usr/bin/env python2
"""
SC-Controller - Controller Button

Wraps around actual button and provides code for setting actions
"""
from __future__ import unicode_literals
from scc.tools import _

from gi.repository import Gtk
from controller_widget import ControllerWidget
import logging

log = logging.getLogger("ControllerButton")

class ControllerButton(ControllerWidget):
	def __init__(self, app, name, widget):
		ControllerWidget.__init__(self, app, name, widget)
		
		vbox = Gtk.Box(Gtk.Orientation.HORIZONTAL)
		separator = Gtk.Separator(orientation = Gtk.Orientation.VERTICAL)
		vbox.pack_start(self.icon, False, False, 1)
		vbox.pack_start(separator, False, False, 1)
		vbox.pack_start(self.label, False, False, 1)
		self.widget.add(vbox)
		self.widget.show_all()
