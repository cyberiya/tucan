###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
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
import sys
import time
import threading
import __builtin__
import gettext
import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from tree import Tree

import cons
from input_files import InputFiles
import threading
from rapidshare import UploadParser

MIN_WIDTH = 250
MIN_HEIGHT = 200

class Gui(gtk.Window):
	""""""
	def __init__(self):
		""""""
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_title("%s - Version: %s" % (cons.TUCAN_NAME, cons.TUCAN_VERSION))
		self.set_size_request(MIN_WIDTH, MIN_HEIGHT)

		self.resize(900, 500)
		self.set_position(gtk.WIN_POS_CENTER)

		self.vbox = gtk.VBox()
		self.add(self.vbox)

		#trees
#		self.downloads = Tree()
		self.downloads = gtk.VBox()
		self.uploads = Tree()
#		self.uploads = gtk.VBox()
		self.add_button = gtk.Button("Add upload")
		self.add_button.connect("clicked", self.input_files, None)

		#pane
		self.pane = gtk.VPaned()
		self.vbox.pack_start(self.pane)
		self.pane.pack2(self.downloads, True)
		self.pane.pack1(self.uploads, True)
		self.vbox.pack_end(self.add_button, True)
		self.pane.set_position(self.get_size()[1])
		
		self.connect("delete_event", self.quit)
		self.show_all()
		
		self.upload = None
		

	def add_upload(self):
		self.upload = UploadParser("/home/elie/cli.png", "mierda", self.uploads.update)
		
	def input_files(self,one,two):
		InputFiles(self,self.uploads)

	def quit(self,one,two):
		""""""
		self.close()

	def close(self):
		""""""
		self.destroy()
		gtk.main_quit()

		
if __name__ == "__main__":
	gobject.threads_init()
	gui = Gui()
	th = threading.Thread(target=gui.add_upload)
	th.start()
	gtk.main()
