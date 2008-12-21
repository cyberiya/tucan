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

import os
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
		self.set_title("Tucan Manager - Version: " + cons.TUCAN_VERSION + cons.REVISION)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_size_request(900, 500)
		#self.maximize()
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
		download = "Add Downloads", gtk.image_new_from_file(cons.ICON_DOWNLOAD), self.add_links
		upload = "Add Uploads", gtk.image_new_from_file(cons.ICON_UPLOAD), self.quit
		clear = "Clear Complete", gtk.image_new_from_file(cons.ICON_CLEAR), self.clear_complete
		up = "Move Up", gtk.image_new_from_file(cons.ICON_UP), self.move_up
		down = "Move Down", gtk.image_new_from_file(cons.ICON_DOWN), self.move_down
		start = "Start Selected", gtk.image_new_from_file(cons.ICON_START), self.start
		stop = "Stop Selected", gtk.image_new_from_file(cons.ICON_STOP), self.stop
		self.vbox.pack_start(Toolbar([download, upload, None, clear, None, up, down, None, start, stop]), False)
		
		delete = gtk.STOCK_REMOVE, self.delete
		start = gtk.STOCK_MEDIA_PLAY, self.start
		stop = gtk.STOCK_MEDIA_STOP, self.stop
		
		#trees
		self.downloads = Tree([delete], self.download_manager.get_files)
		#self.uploads = Tree()
		self.uploads = gtk.VBox()
		
		#pane
		self.pane = gtk.VPaned()
		self.vbox.pack_start(self.pane)
		self.pane.pack1(self.downloads, True)
		self.pane.pack2(self.uploads, True)
		self.pane.set_position(self.get_size()[1])
		
		self.connect("key-press-event", self.delete_key)
		self.connect("delete_event", self.hide_on_delete)
		self.show_all()
		
		#trayicon
		tray_menu = [menu_preferences, menu_about, None, menu_quit]
		self.tray_icon = TrayIcon(self.show, self.hide, tray_menu)
		self.downloads.status_bar.connect("text-pushed", self.tray_icon.change_tooltip)
		
	def delete_key(self, window, event):
		"""pressed del key"""
		if event.keyval == 65535:
			self.delete()

	def not_implemented(self, widget):
		""""""
		w = Message(cons.SEVERITY_WARNING, "Not Implemented!", "The functionality you are trying to use is not implemented yet.")
	
	def resize_pane(self, checkbox):
		""""""
		if checkbox.get_active():
			self.pane.set_position(self.get_size()[1])
		else:
			self.pane.set_position(-1)
		
	def help(self, widget):
		""""""
		webbrowser.open("http://cusl3-tucan.forja.rediris.es/")
		
	def add_links(self, button):
		""""""
		i = InputLinks(self.filter_service, self.link_check, self.create_packages, self.manage_packages)
		
	def manage_packages(self, packages, packages_info):
		""""""
		tmp_packages = []
		if not len(packages_info) > 0:
			packages_info = [(cons.DEFAULT_PATH, name, None) for name, package_files in packages]
		#create directories and password files
		for info in packages_info:
			package_path = info[0] + info[1].replace(" ", "_") + "/"
			if not os.path.exists(package_path):
				os.mkdir(package_path)
			if info[2]:
				f = open(package_path + "password.txt", "w")
				f.write(info[2] + "\n")
				f.close()
		#add packages to gui and manager
		for package_name, package_downloads in packages:
			info = packages_info[packages.index((package_name, package_downloads))]
			package_name = info[1].replace(" ", "_")
			package_path = info[0] + info[1] + "/"
			self.downloads.add_package(package_name, package_path, package_downloads)
			for download in package_downloads:
				tmp = []
				for service in download[2]:
					plugin_name, plugin = self.get_plugin(service)
					tmp.append((download[0][download[2].index(service)], plugin))
				self.download_manager.add(package_path, download[1], tmp, download[3], download[4])
			
	def start(self, button):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		if len(paths) > 0:
			if len(paths[0]) > 1:
				print "start", self.download_manager.start(model.get_value(model.get_iter(paths[0]), 3))
			else:
				print "start package"
				for item in self.downloads.package_files(model.get_iter(paths[0])):
					self.download_manager.start(item)

	def stop(self, button):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		if len(paths) > 0:
			if len(paths[0]) > 1:
				print "stop", self.download_manager.stop(model.get_value(model.get_iter(paths[0]), 3))
			else:
				print "stop package"
				for item in self.downloads.package_files(model.get_iter(paths[0])):
					self.download_manager.stop(item)

	def clear_complete(self, button):
		"""Implementado solo para descargas"""
		files = self.downloads.clear()
		if len(files) > 0:
			self.download_manager.clear(files)
	
	def move_up(self, button):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		if len(paths) > 0:
			if not len(paths[0]) > 1:
				print "move up", self.downloads.move_up(model.get_iter(paths[0]))

	def move_down(self, button):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		if len(paths) > 0:
			if not len(paths[0]) > 1:
				print "move down", self.downloads.move_down(model.get_iter(paths[0]))

	def delete(self, button=None):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		status = [cons.STATUS_STOP, cons.STATUS_PEND, cons.STATUS_ERROR]
		if len(paths) > 0:
			if len(paths[0]) > 2:
				print "remove link"
				name, link = self.downloads.delete_link(status, model.get_iter(paths[0]))
				if link:
					print self.download_manager.delete_link(name, link)
			elif len(paths[0]) > 1:
				print "remove file"
				name = self.downloads.delete_file(status, model.get_iter(paths[0]))
				if name:
					print self.download_manager.clear([name])
			else:
				print "remove package"
				files = self.downloads.delete_package(status, model.get_iter(paths[0]))
				if len(files) > 0:
					print self.download_manager.clear(files)

	def quit(self, dialog=None, response=None):
		""""""
		self.hide()
		self.stop_all()
		gtk.main_quit()
	
if __name__ == "__main__":
	g = Gui()
	gobject.threads_init()
	gtk.main()