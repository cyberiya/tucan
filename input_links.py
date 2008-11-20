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

class InputLinks(gtk.Dialog):
	""""""
	def __init__(self, sort, check, add):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon_from_file(cons.ICON_DOWNLOAD)
		self.set_title("Input Links")
		self.set_size_request(600,500)
		
		self.sort_links = sort
		self.check_links = check
		self.add = add
		
		#textview
		frame = gtk.Frame("Paste links here:")
		self.vbox.pack_start(frame)
		frame.set_border_width(10)
		hbox = gtk.HBox()
		frame.add(hbox)
		scroll = gtk.ScrolledWindow()
		hbox.pack_start(scroll, True, True, 10)
		scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		buffer = gtk.TextBuffer()		
		self.textview = gtk.TextView(buffer)
		scroll.add(self.textview)
		self.textview.set_wrap_mode(gtk.WRAP_CHAR)
		
		#check button
		button_box = gtk.HButtonBox()
		hbox.pack_start(button_box, False, False, 10)
		vbox = gtk.VBox()
		check_image = gtk.image_new_from_file(cons.ICON_CHECK)
		vbox.pack_start(check_image)
		check_label = gtk.Label("Check Links")
		vbox.pack_start(check_label)
		check_button = gtk.Button()
		check_button.add(vbox)
		button_box.pack_start(check_button)
		check_button.connect("clicked", self.check)
		
		#treeview
		self.store = gtk.TreeStore(gtk.gdk.Pixbuf, str, str, str, bool)
		frame = gtk.Frame()
		self.vbox.pack_start(frame)
		frame.set_border_width(10)
		scroll = gtk.ScrolledWindow()
		frame.add(scroll)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.treeview = gtk.TreeView(self.store)		
		scroll.add(self.treeview)
		
		self.treeview.set_rules_hint(True)
		self.treeview.set_headers_visible(False)
		self.treeview.expand_all()
		
		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, True)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.treeview.append_column(tree_icon)
				  
		tree_name = gtk.TreeViewColumn('Name') 
		name_cell = gtk.CellRendererText()
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 1)
		self.treeview.append_column(tree_name)
		
		#action area
		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		add_button = gtk.Button(None, gtk.STOCK_ADD)
		self.action_area.pack_start(cancel_button)
		self.action_area.pack_start(add_button)
		cancel_button.connect("clicked", self.close)
		add_button.connect("clicked", self.add_links)
		
		self.connect("response", self.close)
		self.show_all()
		self.run()
		
	def add_links(self, button):
		""""""
		tmp = {}
		for column in self.store:
			if not column[1] == cons.TYPE_UNSUPPORTED:
				tmp[column[1]] = []
				for value in column.iterchildren():
					tmp[column[1]].append((value[1], value[2], value[3], value[4]))
		if not tmp == {}:
			self.add(tmp)
		self.close()
	
	def check(self, button):
		""""""
		self.store.clear()
		buffer = self.textview.get_buffer()
		start, end = buffer.get_bounds()
		link_list = [link.strip() for link in buffer.get_text(start, end).split("\n")]
		buffer.set_text("")
		
		service_icon = self.treeview.render_icon(gtk.STOCK_INFO, gtk.ICON_SIZE_MENU)
		unsupported_icon = self.treeview.render_icon(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_MENU)
		active_icon = self.treeview.render_icon(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
		unactive_icon = self.treeview.render_icon(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)
		
		for service, links in self.sort_links(link_list).items():
			if not links == []:
				if service == cons.TYPE_UNSUPPORTED:
					service_iter = self.store.append(None, [unsupported_icon, service, None, None, None])
					for link in links:
						self.store.append(service_iter, [unactive_icon, link, None, None, None])
				else:
					service_iter = self.store.append(None, [service_icon, service, None, None, None])
					for link in links:
						active, file_name, size = self.check_links(link)
						icon = unactive_icon
						if active:
							icon = active_icon
						self.store.append(service_iter, [icon, link, file_name, size, active])
		self.treeview.expand_all()
		
	def close(self, widget=None, other=None):
		""""""
		self.destroy()

if __name__ == "__main__":
	def add(text):
		print text
	def parse(text):
		return {}
	def dummy_check(link):
		return True, link.split("/").pop(), "100MB"
	g = InputLinks(parse, parse, add)
	gtk.main()