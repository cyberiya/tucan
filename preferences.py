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

class Preferences(gtk.Dialog):
	""""""
	def __init__(self):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon_from_file(cons.ICON_PREFERENCES)
		self.set_title("Preferences")
		#self.set_resizable(False)
		self.set_size_request(500,500)
		
		self.path = "/home/crak/downloads/"
		
		self.notebook = gtk.Notebook()
		self.notebook.set_property("homogeneous", True)
		self.vbox.pack_start(self.notebook)
		self.new_page("General Configuration", cons.ICON_PREFERENCES_MAIN, self.init_main())
		self.new_page("Service Configuration", cons.ICON_PREFERENCES_SERVICES, self.init_services())
		self.new_page("Advanced Configuration", cons.ICON_PREFERENCES_ADVANCED, self.init_advanced())

		#action area
		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		save_button = gtk.Button(None, gtk.STOCK_SAVE)
		self.action_area.pack_start(cancel_button)
		self.action_area.pack_start(save_button)
		cancel_button.connect("clicked", self.close)
		save_button.connect("clicked", self.close)
		
		self.connect("response", self.close)
		self.show_all()
		self.run()
		
	def new_page(self, tab_name, tab_image, page):
		""""""
		vbox = gtk.VBox()
		vbox.pack_start(gtk.image_new_from_file(tab_image))
		vbox.pack_start(gtk.Label(tab_name))
		vbox.show_all()
		self.notebook.append_page(page, vbox)
		self.notebook.set_tab_label_packing(page, True, True, gtk.PACK_START)
		
	def init_main(self):
		""""""
		vbox = gtk.VBox()
		
		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_LANGUAGE))
		frame.set_border_width(5)
		vbox.pack_start(frame, False, False)
		hbox = gtk.HBox()
		vbox1 = gtk.VBox()
		frame.add(vbox1)
		hbox = gtk.HBox()
		vbox1.pack_start(hbox, False, False, 5)
		label = gtk.Label("Choose language: ")
		hbox.pack_start(label, False, False, 10)
		aspect = gtk.AspectFrame()
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		hbox.pack_start(aspect)
		combobox = gtk.combo_box_new_text()
		for lang in ["English", "French", "German", "Japanese", "Spanish"]:
			combobox.append_text(lang)
		combobox.set_active(0)
		hbox.pack_start(combobox, False, False, 10)

		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_NETWORK))
		frame.set_border_width(5)
		vbox.pack_start(frame, False, False)
		vbox1 = gtk.VBox()
		frame.add(vbox1)
		hbox = gtk.HBox()
		label = gtk.Label("Max simultaneous downloads: ")
		hbox.pack_start(label, False, False, 10)
		aspect = gtk.AspectFrame()
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		hbox.pack_start(aspect)
		spinbutton = gtk.SpinButton()
		spinbutton.set_range(1,10)
		spinbutton.set_increments(1,0)
		spinbutton.set_numeric(True)
		hbox.pack_start(spinbutton, False, False, 10)
		vbox1.pack_start(hbox, False, False, 2)
		hbox = gtk.HBox()
		label = gtk.Label("Max simultaneous uploads: ")
		hbox.pack_start(label, False, False, 10)
		aspect = gtk.AspectFrame()
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		hbox.pack_start(aspect)
		spinbutton = gtk.SpinButton()
		spinbutton.set_range(1,10)
		spinbutton.set_increments(1,0)
		spinbutton.set_numeric(True)
		hbox.pack_start(spinbutton, False, False, 10)
		vbox1.pack_start(hbox, False, False, 2)
		
		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_FOLDER))
		frame.set_border_width(5)
		vbox.pack_start(frame, False, False)
		vbox1 = gtk.VBox()
		frame.add(vbox1)
		hbox = gtk.HBox()
		vbox1.pack_start(hbox, False, False, 5)
		label = gtk.Label("Downloads Folder: " + self.path)
		hbox.pack_start(label, False, False, 10)
		bbox = gtk.HButtonBox()
		bbox.set_layout(gtk.BUTTONBOX_END)
		hbox.pack_start(bbox, True, True, 10)
		button = gtk.Button(None, gtk.STOCK_OPEN)
		button.connect("clicked", self.choose_path)
		bbox.pack_start(button)
		
		vbox.show_all()
		return vbox

	def choose_path(self, button):
		""""""
		self.filechooser = gtk.FileChooserDialog('Select a Folder', self, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
		choose_button = gtk.Button(None, gtk.STOCK_OK)
		self.filechooser.action_area.pack_start(choose_button)
		self.filechooser.connect("response", self.on_choose, False)
		choose_button.connect("clicked", self.on_choose, None, True)
		self.filechooser.set_position(gtk.WIN_POS_CENTER)
		self.filechooser.show_all()
		self.filechooser.run()
			
	def on_choose(self, widget, response, choosed):
		""""""
		if choosed:
			self.path = self.filechooser.get_uri().split("file://").pop()+"/"
		self.filechooser.destroy()
		del self.filechooser

	def init_services(self):
		""""""
		vbox = gtk.VBox()
		
		frame = gtk.Frame()
		frame.set_size_request(-1, 300)
		vbox.pack_start(frame)
		frame.set_border_width(10)
		scroll = gtk.ScrolledWindow()
		frame.add(scroll)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		store = gtk.ListStore(gtk.gdk.Pixbuf, str, bool)
		self.treeview = gtk.TreeView(store)
		scroll.add(self.treeview)
		
		self.treeview.set_rules_hint(True)
		self.treeview.set_headers_visible(False)
		
		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		icon_cell.set_property("width", 100)
		tree_icon.pack_start(icon_cell, True)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.treeview.append_column(tree_icon)
		
		tree_name = gtk.TreeViewColumn('Name')
		name_cell = gtk.CellRendererText()
		name_cell.set_property("width", 300)
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 1)
		self.treeview.append_column(tree_name)
		
		tree_enable = gtk.TreeViewColumn('Enable')
		enable_cell = gtk.CellRendererToggle()
		enable_cell.connect("toggled", self.toggled)
		tree_enable.pack_start(enable_cell, False)
		tree_enable.add_attribute(enable_cell, 'active', 2)
		self.treeview.append_column(tree_enable)
		
		#fill store
		icon = gtk.gdk.pixbuf_new_from_file(cons.ICON_MISSING)
		for service in ["megaupload.com", "rapidshare.com"]:
			store.append((icon, service, True))
		
		frame = gtk.Frame()
		frame.set_border_width(10)
		frame.set_shadow_type(gtk.SHADOW_NONE)
		vbox.pack_start(frame, False, False)
		bbox = gtk.HButtonBox()
		bbox.set_layout(gtk.BUTTONBOX_START)
		frame.add(bbox)
		button = gtk.Button(None, gtk.STOCK_ADD)
		button.connect("clicked", self.close)
		bbox.pack_start(button)
		button = gtk.Button(None, gtk.STOCK_REMOVE)
		button.connect("clicked", self.close)
		bbox.pack_start(button)
		
		return vbox

	def toggled(self, button, path):
		""""""
		model = self.treeview.get_model()
		active = True
		if button.get_active():
			active = False
		button.set_active(active)
		model.set_value(model.get_iter(path), 2, active)

	def init_advanced(self):
		""""""
		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_ADVANCED))
		frame.set_border_width(10)
		hbox = gtk.HBox()
		frame.add(hbox)
		vbox = gtk.VBox()
		hbox.pack_start(vbox, True, True, 10)
		check = gtk.CheckButton("Close to tray.")
		vbox.pack_start(check, False, False, 5)
		check = gtk.CheckButton("Default advanced packages.")
		vbox.pack_start(check, False, False, 5)
		
		return frame
		
	def close(self, widget=None, other=None):
		""""""
		self.destroy()
	
if __name__ == "__main__":
	x = Preferences()