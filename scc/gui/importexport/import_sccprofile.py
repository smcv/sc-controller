#!/usr/bin/env python2
from __future__ import unicode_literals
from scc.tools import _

from gi.repository import Gtk, Gio
from scc.tools import get_profiles_path, find_profile, find_menu
from scc.special_actions import ShellCommandAction
from scc.profile import Profile
from scc.gui.parser import GuiActionParser

import sys, os, json, tarfile, tempfile, logging
log = logging.getLogger("IE.ImportSSCC")

class ImportSccprofile(object):
	def __init__(self):
		self._profile = None
	
	
	def on_btImportSccprofile_clicked(self, *a):
		# Create filters
		f1 = Gtk.FileFilter()
		f1.set_name("SC-Controller Profile or Archive")
		f1.add_pattern("*.sccprofile")
		f1.add_pattern("*.sccprofile.tar.gz")
		
		# Create dialog
		d = Gtk.FileChooserNative.new(_("Import Profile..."),
				self.window, Gtk.FileChooserAction.OPEN)
		d.add_filter(f1)
		if d.run() == Gtk.ResponseType.ACCEPT:
			if d.get_filename().endswith(".tar.gz"):
				if self.import_scc_tar(d.get_filename()):
					self.window.destroy()
			else:
				if self.import_scc(d.get_filename()):
					self.window.destroy()
	
	
	def error(self, text):
		"""
		Displays error page (reused from VDF import).
		"""
		tbError =			self.builder.get_object("tbError")
		grImportFailed =	self.builder.get_object("grImportFailed")
		
		tbError.set_text(text)
		self.next_page(grImportFailed)
	
	
	def import_scc(self, filename):
		"""
		Imports simple, single-file scc-profile.
		Just loads it, checks for shell() actions and asks user to enter name.
		"""
		# Load profile
		self._profile = Profile(GuiActionParser())
		try:
			self._profile.load(filename)
		except Exception, e:
			# Profile cannot be parsed. Display error message and let user to quit
			# Error message reuses page from VDF import, because they are
			# basically the same
			log.error(e)
			self.error(str(e))
			return False
		
		# Check for shell commands
		grShellCommands =	self.builder.get_object("grShellCommands")
		tvShellCommands =	self.builder.get_object("tvShellCommands")
		model = tvShellCommands.get_model()
		model.clear()
		for a in self._profile.get_actions():
			if isinstance(a, ShellCommandAction):
				model.append((False, a.command))
		# If there is shell command present, jump to warning page
		if len(model) > 0:
			self.next_page(grShellCommands)
			btNext = self.enable_next(True)
			btNext.set_label(_("Continue"))
			btNext.set_sensitive(False)
	
	
	def on_crShellCommandChecked_toggled(self, cr, path):
		tvShellCommands =	self.builder.get_object("tvShellCommands")
		btNext =			self.builder.get_object("btNext")
		model = tvShellCommands.get_model()
		model[path][0] = not model[path][0]
		btNext.set_sensitive(True)
		for row in model:
			if not row[0]:
				btNext.set_sensitive(False)
				return