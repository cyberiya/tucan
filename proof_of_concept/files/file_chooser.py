###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion crakotaku(at)yahoo.es
## Copyright (C) 2008-2009 Paco Salido beakman(at)riseup.net
## Copyright (C) 2008-2009 JM Cordero betic0(at)gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import os

import pygtk
pygtk.require('2.0')
import gtk

import cons

class FileChooser(gtk.FileChooserDialog):
	""""""
	def __init__(self, parent, func, default_path=None):
		""""""
		gtk.FileChooserDialog.__init__(self, _("Select a Folder"), parent, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
		if default_path:
			self.set_filename(default_path)
		
		self.action_area.set_layout(gtk.BUTTONBOX_EDGE)
		hidden_button = gtk.CheckButton(_("Show hidden files."))
		hidden_button.set_active(self.get_show_hidden())
		self.action_area.pack_start(hidden_button)
		hidden_button.connect("clicked", self.show_hidden)
		
		button = gtk.Button(None, gtk.STOCK_OK)
		button.connect("clicked", self.on_choose_folder, func)
		self.action_area.pack_start(button)
		self.set_position(gtk.WIN_POS_CENTER)
		
		self.connect("response", self.close)
		
		self.show_all()
		self.run()

	def show_hidden(self, button):
		""""""
		self.set_show_hidden(button.get_active())

	def on_choose_folder(self, button, func):
		""""""
		func(os.path.join(self.get_filename(), ""))
		self.close()
		
	def close(self, widget=None, response=None):
		""""""
		self.destroy()
