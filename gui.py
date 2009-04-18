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
import sys
import time
import threading
import webbrowser
import __builtin__
import gettext
import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from about import About
from message import Message
from tray_icon import TrayIcon
from preferences import Preferences
from log_view import LogView

from menu_bar import MenuBar
from toolbar import Toolbar

import config
from sessions import Sessions
from file_chooser import FileChooser

from tree import Tree
from input_links import InputLinks

from service_manager import ServiceManager

from service_update import ServiceUpdate

import cons
	
class Gui(gtk.Window, ServiceManager):
	""""""
	def __init__(self, conf):
		""""""		
		#i18n
		gettext.bindtextdomain(cons.NAME_LOCALES, cons.PATH_LOCALES)
		gettext.textdomain(cons.NAME_LOCALES)
		__builtin__._ = gettext.gettext

		#configuration
		self.configuration = conf

		#show preferences if not configured
		if not self.configuration.configured:
			Preferences(self.configuration, True)
		self.preferences_shown =  False
		
		#l10n
		lang = gettext.translation(cons.NAME_LOCALES, cons.PATH_LOCALES, languages=[self.configuration.get(config.SECTION_MAIN, config.OPTION_LANGUAGE)])
		lang.install()

		ServiceManager.__init__(self, self.configuration)
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		
		self.set_icon_from_file(cons.ICON_TUCAN)
		self.set_title("%s - Version: %s" % (cons.TUCAN_NAME, cons.TUCAN_VERSION))
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_size_request(900, 500)
		self.vbox = gtk.VBox()
		self.add(self.vbox)
		
		#menu items
		menu_load_session = _("Load Session"), lambda x: FileChooser(self, self.load_session, cons.CONFIG_PATH, True)
		menu_save_session = _("Save Session"), lambda x: FileChooser(self, self.save_session, cons.CONFIG_PATH, save=True)
		menu_quit = gtk.STOCK_QUIT, self.quit
		menu_help = gtk.STOCK_HELP, self.help
		menu_about = gtk.STOCK_ABOUT, About
		menu_preferences = gtk.STOCK_PREFERENCES, self.preferences
		menu_log = _("Show Logs"), LogView
		show_uploads = gtk.CheckMenuItem(_("Show Uploads")), self.resize_pane, self.configuration.getboolean(config.SECTION_ADVANCED, config.OPTION_SHOW_UPLOADS)
		
		#menubar
		file_menu = _("File"), [menu_load_session, menu_save_session, None, menu_quit]
		view_menu = _("View"), [show_uploads, menu_log, None, menu_preferences]
		help_menu = _("Help"), [menu_help, menu_about]
		self.vbox.pack_start(MenuBar([file_menu, view_menu, help_menu]), False)

		#toolbar
		download = _("Add Downloads"), gtk.image_new_from_file(cons.ICON_DOWNLOAD), self.add_links
		upload = _("Add Uploads"), gtk.image_new_from_file(cons.ICON_UPLOAD), self.not_implemented #self.quit
		clear = _("Clear Complete"), gtk.image_new_from_file(cons.ICON_CLEAR), self.clear_complete
		up = _("Move Up"), gtk.image_new_from_file(cons.ICON_UP), self.move_up
		down = _("Move Down"), gtk.image_new_from_file(cons.ICON_DOWN), self.move_down
		start = _("Start Selected"), gtk.image_new_from_file(cons.ICON_START), self.start
		stop = _("Stop Selected"), gtk.image_new_from_file(cons.ICON_STOP), self.stop
		self.vbox.pack_start(Toolbar([download, upload, None, clear, None, up, down, None, start, stop]), False)
		
		copy = gtk.STOCK_COPY, self.copy_clipboard
		delete = gtk.STOCK_REMOVE, self.delete
		start = gtk.STOCK_MEDIA_PLAY, self.start
		stop = gtk.STOCK_MEDIA_STOP, self.stop
		
		#trees
		self.downloads = Tree([copy, None, delete], self.download_manager)
		#self.uploads = Tree()
		self.uploads = gtk.VBox()
		
		#sessions
		self.session = Sessions()
		if self.configuration.getboolean(config.SECTION_ADVANCED, config.OPTION_SAVE_SESSION):
			self.load_default_session()
		else:
			if os.path.exists(cons.SESSION_FILE):
				title = _("Tucan Manager - Restore previous session.")
				message = _("Your last session closed unexpectedly.\nTucan will try to restore it now.")
				m = Message(None, cons.SEVERITY_WARNING, title, message, both=True)
				if m.accepted:
					self.load_default_session()
		
		#pane
		self.pane = gtk.VPaned()
		self.vbox.pack_start(self.pane)
		self.pane.pack1(self.downloads, True)
		self.pane.pack2(self.uploads, True)
		self.pane.set_position(self.get_size()[1])
		
		self.connect("key-press-event", self.delete_key)
		
		if self.configuration.getboolean(config.SECTION_ADVANCED, config.OPTION_TRAY_CLOSE):
			self.connect("delete_event", self.hide_on_delete)
		else:
			self.connect("delete_event", self.quit)
		
		self.show_all()
				
		#trayicon
		tray_menu = [menu_preferences, menu_about, None, menu_quit]
		self.tray_icon = TrayIcon(self.show, self.hide, tray_menu)
		self.connect("hide", self.tray_icon.activate)
		self.downloads.status_bar.connect("text-pushed", self.tray_icon.change_tooltip)
		
		#Autocheck services
		th = threading.Thread(group=None, target=self.check_updates, name=None)
		th.start()

		#ugly polling
		gobject.timeout_add(120000, self.save_default_session)
		
	def check_updates(self):
		""""""
		s = ServiceUpdate(self.configuration)
		if len(s.get_updates()) > 0:
			gobject.idle_add(self.update_manager)
			
	def update_manager(self):
		""""""
		if not self.preferences_shown:
			self.preferences_shown = True
			Preferences(self.configuration, True, True)
			self.preferences_shown =  False
		return False
		
	def delete_key(self, window, event):
		"""pressed del key"""
		if event.keyval == 65535:
			self.delete()
			
	def preferences(self, button=None):
		""""""
		if not self.preferences_shown:
			self.preferences_shown = True
			Preferences(self.configuration)
			self.preferences_shown =  False

	def not_implemented(self, widget):
		""""""
		w = Message(self, cons.SEVERITY_WARNING, "Not Implemented!", "The functionality you are trying to use is not implemented yet.")
	
	def resize_pane(self, checkbox):
		""""""
		if checkbox.get_active():
			self.pane.set_position(-1)
		else:
			self.pane.set_position(self.get_size()[1])
		
	def help(self, widget):
		""""""
		webbrowser.open(cons.DOC)
		
	def add_links(self, button):
		""""""
		default_path = self.configuration.get(config.SECTION_MAIN, config.OPTION_DOWNLOADS_FOLDER)
		show_advanced_packages = self.configuration.getboolean(config.SECTION_ADVANCED, config.OPTION_ADVANCED_PACKAGES)
		InputLinks(default_path, self.filter_service, self.get_check_links, self.create_packages, self.manage_packages, show_advanced_packages)
		
	def copy_clipboard(self, button):
		""""""
		model, iter = self.downloads.treeview.get_selection().get_selected()
		if iter:
			link_list = self.downloads.get_links(iter)
			clipboard = gtk.Clipboard()
			clipboard.clear()
			clipboard.set_text("\n".join(link_list))

	def load_session(self, path):
		""""""
		packages, info = self.session.load_session(path)
		if packages != None:
			self.manage_packages(packages, info)
			logger.debug("Session loaded: %s" % info)
		
	def save_session(self, path):
		""""""
		packages, info = self.downloads.get_packages()
		self.session.save_session(path, packages, info)
		logger.debug("Session saved: %s" % info)
		
	def load_default_session(self):
		""""""
		self.load_session(cons.SESSION_FILE)
			
	def save_default_session(self):
		""""""
		self.save_session(cons.SESSION_FILE)
		return True
		
	def manage_packages(self, packages, packages_info):
		""""""
		tmp_packages = []
		if not len(packages_info) > 0:
			default_path = self.configuration.get(config.SECTION_MAIN, config.OPTION_DOWNLOADS_FOLDER)
			packages_info = [(default_path, name, None) for name, package_files in packages]
		#create directories and password files
		for info in packages_info:
			package_path = os.path.join(info[0], info[1].replace(" ", "_"), "")
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
			package_path = os.path.join(info[0], package_name, "")
			self.downloads.add_package(package_name, package_path, package_downloads, info[2])
			for download in package_downloads:
				tmp = []
				for service in download[2]:
					plugin, plugin_type = self.get_download_plugin(service)
					tmp.append((download[0][download[2].index(service)], plugin, plugin_type, service))
				self.download_manager.add(package_path, download[1], tmp, download[3], download[4])
			
	def start(self, button):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		if len(paths) > 0:
			if len(paths[0]) > 1:
				logger.warning("Start file: %s" % self.download_manager.start(model.get_value(model.get_iter(paths[0]), 3)))
			else:
				logger.warning("Start package.")
				for item in self.downloads.package_files(model.get_iter(paths[0])):
					self.download_manager.start(item)

	def stop(self, button):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		if len(paths) > 0:
			if len(paths[0]) > 1:
				logger.warning("Stop file: %s" % self.download_manager.stop(model.get_value(model.get_iter(paths[0]), 3)))
			else:
				logger.warning("Stop package.")
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
				logger.warning("Move up: %s" % self.downloads.move_up(model.get_iter(paths[0])))

	def move_down(self, button):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		if len(paths) > 0:
			if not len(paths[0]) > 1:
				logger.warning("Move down: %s" % self.downloads.move_down(model.get_iter(paths[0])))

	def delete(self, button=None):
		"""Implementado solo para descargas"""
		model, paths = self.downloads.treeview.get_selection().get_selected_rows()
		status = [cons.STATUS_STOP, cons.STATUS_PEND, cons.STATUS_ERROR]
		if len(paths) > 0:
			if len(paths[0]) > 2:
				name, link = self.downloads.delete_link(status, model.get_iter(paths[0]))
				if link:
					logger.warning("Remove %s: %s" % (link, self.download_manager.delete_link(name, link)))
			elif len(paths[0]) > 1:
				name = self.downloads.delete_file(status, model.get_iter(paths[0]))
				if name:
					logger.warning("Remove %s: %s" % (name, self.download_manager.clear([name])))
			else:
				files = self.downloads.delete_package(status, model.get_iter(paths[0]))
				if len(files) > 0:
					logger.warning("Remove package: %s" % self.download_manager.clear(files))

	def quit(self, dialog=None, response=None):
		""""""
		if len(self.download_manager.active_downloads) > 0:
			message = "Tucan still has active downloads.\n Are you sure you want to quit?"
			m = Message(self, cons.SEVERITY_WARNING, "Tucan Manager - Active Downloads.", message, True, True)
			if m.accepted:
				self.close()
			else:
				#This way GTK won't destroy the window.
				return True
		else:
			self.close()

	def close(self):
		""""""
		if self.configuration.getboolean(config.SECTION_ADVANCED, config.OPTION_SAVE_SESSION):
			self.save_default_session()
		else:
			try:
				os.remove(cons.SESSION_FILE)
			except Exception, e:
				logger.info(e)
		self.hide()
		self.tray_icon.set_visible(False)
		self.stop_all()
		gtk.main_quit()
	
if __name__ == "__main__":
	g = Gui()
	gobject.threads_init()
	gtk.main()