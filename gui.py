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

import pygtk
pygtk.require('2.0')
import gtk

from tray_icon import TrayIcon
from service_manager import ServiceManager
from input_links import InputLinks

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
		menu_quit = gtk.STOCK_QUIT, self.quit
		menu_help = gtk.STOCK_HELP, self.quit
		menu_about = gtk.STOCK_ABOUT, self.quit
		menu_preferences = gtk.STOCK_PREFERENCES, self.quit
		menu_import = "Import", self.quit
		
		#menubar
		file_menu = "File", [menu_import, None, menu_quit]
		edit_menu = "Options", [menu_preferences]
		help_menu = "Help", [menu_help, menu_about]
		self.vbox.pack_start(MenuBar([file_menu, edit_menu, help_menu]), False)

		#toolbar
		download = "Add Downloads", gtk.image_new_from_file(cons.ICON_DOWNLOAD), self.add_callback
		upload = "Add Uploads", gtk.image_new_from_file(cons.ICON_UPLOAD), self.quit
		clear = "Clear Complete", gtk.image_new_from_file(cons.ICON_CLEAR), self.quit
		up = "Move Up", gtk.image_new_from_file(cons.ICON_UP), self.quit
		down = "Move Down", gtk.image_new_from_file(cons.ICON_DOWN), self.quit
		start = "Start Selected", gtk.image_new_from_file(cons.ICON_START), self.quit
		stop = "Stop Selected", gtk.image_new_from_file(cons.ICON_STOP), self.quit
		self.vbox.pack_start(Toolbar([download, upload, clear, None, up, down, None, start, stop]), False)
		
		#treestores
		self.downloads = gtk.TreeStore(str)
		self.uploads = gtk.TreeStore(str)
		
		#pane
		pane = gtk.VPaned()
		self.vbox.pack_start(pane)
		pane.pack1(Tree(self.downloads, "No Downloads Active."), False)
		pane.pack2(Tree(self.uploads, "No Uploads Active."), False)
		
		self.connect("delete_event", self.hide_on_delete)
		self.show_all()
		
		#trayicon
		tray_menu = [menu_preferences, menu_about, None, menu_quit]
		self.tray_icon = TrayIcon(self.show, self.hide, tray_menu)
		
	def add_callback(self, button):
		""""""
		i = InputLinks(self.filter_service, self.dummy_check, self.dummy_add)
		
	def dummy_add(self, links):
		""""""
		print links
		
	def dummy_check(self, link):
		""""""
		return True, link.split("/").pop(), "100MB"

	def quit(self, dialog=None, response=None):
		""""""
		gtk.main_quit()
		
class Tree(gtk.VBox):
	""""""
	def __init__(self, model, text):
		""""""
		gtk.VBox.__init__(self)
		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.treeview = gtk.TreeView(model)
		self.treeview.set_rules_hint(True)
		scroll.add(self.treeview)
		self.pack_start(scroll)
		self.status_bar = gtk.Statusbar()
		self.status_bar.set_has_resize_grip(False)
		self.pack_start(self.status_bar, False)
		
		self.status_bar.push(self.status_bar.get_context_id(""), "\t" + text)
		
class Toolbar(gtk.Toolbar):
	""""""
	def __init__(self, list):
		"""list = [(tool_name, image, callback),]"""
		gtk.Toolbar.__init__(self)
		self.set_style(gtk.TOOLBAR_BOTH)
		for button in list:
			if button == None:
				item = gtk.SeparatorToolItem()
			else:
				item = gtk.ToolButton(button[1], button[0])
				item.connect("clicked", button[2])
			self.insert(item, -1)

class MenuBar(gtk.MenuBar):
	""""""
	def __init__(self, list):
		"""list = [(menu_name=str, [(item_image=stock_item, callback), None=separator])]"""
		gtk.MenuBar.__init__(self)
		for menu in list:
			item = gtk.MenuItem(menu[0])
			self.append(item)
			submenu = gtk.Menu()
			for sub in menu[1]:
				if sub == None:
					subitem = gtk.SeparatorMenuItem()
				else:
					subitem = gtk.ImageMenuItem(sub[0])
					subitem.connect("activate", sub[1])
				submenu.append(subitem)
			item.set_submenu(submenu)
	
if __name__ == "__main__":
	g = Gui()
	gtk.main()