###############################################################################
##	Tucan Project

##	Copyright (C) 2008 Fran Lupion Crakotak(at)yahoo.es
##	Copyright (C) 2008 Paco Salido beakman(at)riseup.net
##	Copyright (C) 2008 JM Cordero betic0(at)gmail.com

##	This program is free software; you can redistribute it and/or modify
##	it under the terms of the GNU General Public License as published by
##	the Free Software Foundation; either version 2 of the License, or
##	(at your option) any later version.

##	This program is distributed in the hope that it will be useful,
##	but WITHOUT ANY WARRANTY; without even the implied warranty of
##	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##	GNU General Public License for more details.

##	You should have received a copy of the GNU General Public License
##	along with this program; if not, write to the Free Software
##	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import webbrowser
import time

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from about import About
from message import Message
from tray_icon import TrayIcon
from menu_bar import MenuBar
from toolbar import Toolbar
from tree import Tree
from input_links import InputLinks

from service_manager import ServiceManager

import cons

class Gui(gtk.Window, ServiceManager):
	""""""
	def __init__(self):
		""""""
		ServiceManager.__init__(self)
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_icon_from_file(cons.ICON_TUCAN)
		self.set_title("Tucan Manager - Version: " + cons.TUCAN_VERSION)
		self.maximize()
		self.vbox = gtk.VBox()
		self.add(self.vbox)
		
		#menu items
		menu_import = "Import", self.not_implemented
		menu_quit = gtk.STOCK_QUIT, self.quit
		menu_help = gtk.STOCK_HELP, self.help
		menu_about = gtk.STOCK_ABOUT, About
		menu_preferences = gtk.STOCK_PREFERENCES, self.not_implemented
		hide_uploads = gtk.CheckMenuItem("Hide Uploads"), self.resize_pane, True
		
		#menubar
		file_menu = "File", [menu_import, None, menu_quit]
		view_menu = "View", [hide_uploads, None, menu_preferences]
		help_menu = "Help", [menu_help, menu_about]
		self.vbox.pack_start(MenuBar([file_menu, view_menu, help_menu]), False)

		#toolbar
		download = "Add Downloads", gtk.image_new_from_file(cons.ICON_DOWNLOAD), self.add_callback
		upload = "Add Uploads", gtk.image_new_from_file(cons.ICON_UPLOAD), self.quit
		clear = "Clear Complete", gtk.image_new_from_file(cons.ICON_CLEAR), self.not_implemented
		up = "Move Up", gtk.image_new_from_file(cons.ICON_UP), self.not_implemented
		down = "Move Down", gtk.image_new_from_file(cons.ICON_DOWN), self.not_implemented
		start = "Start Selected", gtk.image_new_from_file(cons.ICON_START), self.start
		stop = "Stop Selected", gtk.image_new_from_file(cons.ICON_STOP), self.stop
		self.vbox.pack_start(Toolbar([download, upload, clear, None, up, down, None, start, stop]), False)
		
		#trees
		self.downloads = Tree(self.get_plugin, "No Downloads Active.")
		self.uploads = Tree(self.get_plugin, "No Uploads Active.")
		
		#pane
		self.pane = gtk.VPaned()
		self.vbox.pack_start(self.pane)
		self.pane.pack1(self.downloads, True)
		self.pane.pack2(self.uploads, True)
		self.pane.set_position(self.get_size()[1])

		self.connect("delete_event", self.hide_on_delete)
		self.show_all()
		
		#trayicon
		tray_menu = [menu_preferences, menu_about, None, menu_quit]
		self.tray_icon = TrayIcon(self.show, self.hide, tray_menu)
		
	def start(self, button):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		for path in paths:
			print self.downloads.start_item(model.get_iter(path))

	def stop(self, button):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		for path in paths:
			print self.downloads.stop_item(model.get_iter(path))
		
	def not_implemented(self, widget):
		""""""
		w = Message(cons.SEVERITY_WARNING, "Not Implemented!", "The Functionality you are trying to use is not implemented yet.")
	
	def resize_pane(self, checkbox):
		""""""
		if checkbox.get_active():
			self.pane.set_position(self.pane.get_property("max-position"))
		else:
			self.pane.set_position(-1)
		
	def help(self, widget):
		""""""
		webbrowser.open("http://cusl3-tucan.forja.rediris.es/")
		
	def add_callback(self, button):
		""""""
		i = InputLinks(self.filter_service, self.link_check, self.downloads.add_package)
		
	def link_check(self, link, service):
		"""return (active, file_name, int_size, size_unit, plugin)"""
		plugin_name, plugin = self.get_plugin(service)
		name, size, unit = plugin.check_link(link)
		if unit == cons.UNIT_KB:
			size = int(round(size/1024))
			unit = cons.UNIT_MB
		return name, size, unit, plugin_name

	def quit(self, dialog=None, response=None):
		""""""
		gtk.main_quit()
	
if __name__ == "__main__":
	g = Gui()
	gobject.threads_init()
	gtk.main()