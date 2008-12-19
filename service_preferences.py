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

import cons

class AnonymousPreferences(gtk.VBox):
	""""""
	def __init__(self, name):
		""""""
		gtk.VBox.__init__(self)
		label = gtk.Label(name)
		self.pack_start(label)

class AccountPreferences(gtk.VBox):
	""""""
	def __init__(self, name):
		""""""
		gtk.VBox.__init__(self)
		label = gtk.Label(name)
		self.pack_start(label, False, False, 10)
		
		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_ACCOUNT))
		frame.set_border_width(10)
		self.pack_start(frame)
		scroll = gtk.ScrolledWindow()
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		frame.add(scroll)
		store = gtk.ListStore(gtk.gdk.Pixbuf, str, str, bool)
		self.treeview = gtk.TreeView(store)
		scroll.add(self.treeview)
		
		self.treeview.set_rules_hint(True)
		self.treeview.set_headers_visible(False)		

		tree_icon = gtk.TreeViewColumn('Active') 
		icon_cell = gtk.CellRendererPixbuf()
		icon_cell.set_property("width", 50)
		tree_icon.pack_start(icon_cell, True)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.treeview.append_column(tree_icon)
		
		tree_name = gtk.TreeViewColumn('User Name') 
		name_cell = gtk.CellRendererText()
		name_cell.set_property("width", 120)
		name_cell.set_property("editable", True)
		name_cell.connect("edited", self.change, 1)
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 1)
		self.treeview.append_column(tree_name)

		tree_pass = gtk.TreeViewColumn('Password') 
		pass_cell = gtk.CellRendererText()
		pass_cell.set_property("width", 120)
		pass_cell.set_property("editable", True)
		pass_cell.connect("edited", self.change, 2)
		tree_pass.pack_start(pass_cell, True)
		tree_pass.add_attribute(pass_cell, 'text', 2)
		self.treeview.append_column(tree_pass)

		tree_enable = gtk.TreeViewColumn('Enable')
		enable_cell = gtk.CellRendererToggle()
		enable_cell.connect("toggled", self.toggled)
		tree_enable.pack_start(enable_cell, False)
		tree_enable.add_attribute(enable_cell, 'active', 3)
		self.treeview.append_column(tree_enable)

		self.active_service_icon = self.treeview.render_icon(gtk.STOCK_YES, gtk.ICON_SIZE_LARGE_TOOLBAR)
		self.unactive_service_icon = self.treeview.render_icon(gtk.STOCK_NO, gtk.ICON_SIZE_LARGE_TOOLBAR)
		
		for name, password in [("mierda", "puta"),("hostia", "cojones")]:
			store.append([self.unactive_service_icon, name, password, True])

		frame = gtk.Frame()
		frame.set_border_width(10)
		frame.set_shadow_type(gtk.SHADOW_NONE)
		self.pack_start(frame, False, False)
		bbox = gtk.HButtonBox()
		bbox.set_layout(gtk.BUTTONBOX_EDGE)
		frame.add(bbox)
		button = gtk.Button(None, gtk.STOCK_ADD)
		button.connect("clicked", self.add)
		bbox.pack_start(button)
		button = gtk.Button(None, gtk.STOCK_REMOVE)
		button.connect("clicked", self.remove)
		bbox.pack_start(button)
		aspect = gtk.AspectFrame()
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		bbox.pack_start(aspect)
		button = gtk.Button(None, gtk.STOCK_REFRESH)
		button.connect("clicked", self.check)
		bbox.pack_start(button)
		
	def add(self, button):
		""""""
		model = self.treeview.get_model()
		iter = model.append([self.unactive_service_icon, "None", "None", False])
		self.treeview.set_cursor(model.get_path(iter), self.treeview.get_column(1), True)

	def remove(self, button):
		""""""
		model, iter = self.treeview.get_selection().get_selected()
		if iter:
			model.remove(iter)

	def check(self, button):
		""""""
		model, iter = self.treeview.get_selection().get_selected()
		if iter:
			print "download cookie", model.get_value(iter, 1), model.get_value(iter, 2)

	def toggled(self, button, path):
		""""""
		model = self.treeview.get_model()
		if button.get_active():
			active = False
		else:
			active = True
		button.set_active(active)
		model.set_value(model.get_iter(path), 3, active)

	def change(self, cellrenderertext, path, new_text, column):
		""""""
		model = self.treeview.get_model()
		model.set_value(model.get_iter(path), column, new_text)

class ServicePreferences(gtk.Dialog):
	""""""
	def __init__(self, name, icon):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon(icon)
		self.set_title(name)
		self.set_size_request(600, 400)
		
		hbox = gtk.HBox()
		self.vbox.pack_start(hbox, True, True, 5)
		frame = gtk.Frame()
		hbox.pack_start(frame, False, False, 10)
		
		store = gtk.TreeStore(str, int)
		treeview = gtk.TreeView(store)
		treeview.get_selection().connect("changed", self.select)
		frame.add(treeview)
		
		treeview.set_headers_visible(False)
		
		tree_name = gtk.TreeViewColumn('Name')
		name_cell = gtk.CellRendererText()
		name_cell.set_property("width", 100)
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 0)
		treeview.append_column(tree_name)
		
		self.notebook = gtk.Notebook()
		hbox.pack_start(self.notebook, True, True, 10)
		self.notebook.set_show_tabs(False)
		
		cont = 0
		for item in ["Downloads", "Uploads"]:
			iter = store.append(None, [item, -1])
			for subitem in ["Anonymous", "User", "Premium"]:
				page = gtk.VBox()
				if subitem == "Anonymous":
					page = AnonymousPreferences(subitem + " " + item)
				else:
					page = AccountPreferences(subitem + " " + item)
				self.notebook.append_page(page, None)
				subiter = store.append(iter, [subitem, cont])
				treeview.expand_to_path(store.get_path(subiter))
				if cont == 0:
					treeview.set_cursor_on_cell(store.get_path(subiter))
				cont += 1

		#action area
		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		ok_button = gtk.Button(None, gtk.STOCK_OK)
		self.action_area.pack_start(cancel_button)
		self.action_area.pack_start(ok_button)
		cancel_button.connect("clicked", self.close)
		ok_button.connect("clicked", self.close)
		
		self.connect("response", self.close)
		self.show_all()
		self.run()
		
	def select(self, selection):
		""""""
		model, iter = selection.get_selected()
		if iter:
			child_iter = model.iter_children(iter)
			if child_iter:
				selection.select_iter(child_iter)
			else:
				self.notebook.set_current_page(model.get_value(iter, 1))

	def close(self, widget=None, other=None):
		""""""
		self.destroy()
	
if __name__ == "__main__":
	x = ServicePreferences("rapidshare.com", gtk.gdk.pixbuf_new_from_file(cons.ICON_MISSING))