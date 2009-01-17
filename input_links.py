###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion Crakotak(at)yahoo.es
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

import HTMLParser
import threading

import pygtk
pygtk.require('2.0')
import gtk

from message import Wait
from advanced_packages import AdvancedPackages

import cons

class ClipParser(HTMLParser.HTMLParser):
	""""""
	def __init__(self):
		""""""
		HTMLParser.HTMLParser.__init__(self)
		self.url = []
	
	def handle_starttag(self, tag, attrs):
		""""""
		if tag == "a":
			if attrs[0][0] == "href":
				self.url.append(attrs[0][1])

class InputLinks(gtk.Dialog):
	""""""
	def __init__(self, path, sort, check, create, manage, show_advanced_packages):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon_from_file(cons.ICON_DOWNLOAD)
		self.set_title(_("Input Links"))
		self.set_size_request(600,500)
		
		self.cancel_check = False
		
		self.clipboard = gtk.clipboard_get()
		self.clipboard.request_targets(self.get_clipboard)

		self.default_path = path
		self.sort_links = sort
		self.check_links = check
		self.create_packages = create
		self.packages = manage
		
		#textview
		frame = gtk.Frame(_("Paste links here:"))
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
		check_label = gtk.Label(_("Check Links"))
		vbox.pack_start(check_label)
		check_button = gtk.Button()
		check_button.add(vbox)
		button_box.pack_start(check_button)
		check_button.connect("clicked", self.check)
		
		#treeview
		frame = gtk.Frame()
		self.vbox.pack_start(frame)
		frame.set_border_width(10)
		scroll = gtk.ScrolledWindow()
		frame.add(scroll)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.treeview = gtk.TreeView(gtk.TreeStore(gtk.gdk.Pixbuf, str, str, int, str, str, bool, bool))
		scroll.add(self.treeview)
		
		self.treeview.set_rules_hint(True)
		self.treeview.set_headers_visible(False)
		
		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, True)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.treeview.append_column(tree_icon)
				  
		tree_name = gtk.TreeViewColumn('Name') 
		name_cell = gtk.CellRendererText()
		name_cell.set_property("editable", True)
		name_cell.connect("edited", self.change_name)
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 2)
		self.treeview.append_column(tree_name)
		
		tree_add = gtk.TreeViewColumn('Add')
		add_cell = gtk.CellRendererToggle()
		add_cell.connect("toggled", self.toggled)
		tree_add.pack_start(add_cell, True)
		tree_add.add_attribute(add_cell, 'active', 6)
		tree_add.add_attribute(add_cell, 'visible', 7)
		self.treeview.append_column(tree_add)
		
		#advanced checkbutton
		self.advanced_button = gtk.CheckButton(_("Show advanced Package configuration."))
		self.advanced_button.set_active(show_advanced_packages)
		self.vbox.pack_start(self.advanced_button, False)
		
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
		
	def change_name(self, cellrenderertext, path, new_text):
		""""""
		model = self.treeview.get_model()
		model.set_value(model.get_iter(path), 2, new_text)

	def get_clipboard(self, clipboard, selection_data, data):
		""""""
		target_html = "text/html"
		if target_html  in list(selection_data):
			selection = self.clipboard.wait_for_contents(target_html)
			if selection:
				for line in str(selection.data.decode("utf16")).split("\n"):
					try:
						parser = ClipParser()
						parser.feed(line)
						parser.close()
						if len(parser.url) > 0:
							self.textview.get_buffer().insert_at_cursor("\n".join(parser.url) + "\n")
					except HTMLParser.HTMLParseError:
						pass
	def toggled(self, button, path):
		""""""
		model = self.treeview.get_model()
		active = True
		if button.get_active():
			active = False
		button.set_active(active)
		model.set_value(model.get_iter(path), 6, active)
		
	def add_links(self, button):
		""""""
		tmp = {}
		store = self.treeview.get_model()
		for column in store:
			if column[2] != cons.TYPE_UNSUPPORTED:
				tmp[column[2]] = []
				for value in column.iterchildren():
					if value[1] != value[2]:
						if value[6]:
							print value[1], value[2], value[3], value[4], value[5]
							tmp[column[2]].append((value[1], value[2], value[3], value[4], value[5]))
		if tmp != {}:
			self.hide()
			packages = self.create_packages(tmp)
			packages_info = None
			if self.advanced_button.get_active():
				w = AdvancedPackages(self.default_path, packages)
				packages_info = w.packages
				if packages_info:
					self.packages(packages, packages_info)
					self.close()
				else:
					self.show()
			else:
				self.packages(packages, [])
				self.close()
		else:
			self.close()
	
	def check(self, button):
		""""""
		w = Wait(_("Checking links, please wait."), self)
		w.connect("key-press-event", self.cancel)
		th = threading.Thread(group=None, target=self.check_all, name=None, args=(w,))
		th.start()
		
	def check_all(self, wait):
		""""""
		gtk.gdk.threads_enter()
		store = self.treeview.get_model()
		store.clear()
		buffer = self.textview.get_buffer()
		start, end = buffer.get_bounds()
		link_list = [link.strip() for link in buffer.get_text(start, end).split("\n")]
		
		service_icon = self.treeview.render_icon(gtk.STOCK_INFO, gtk.ICON_SIZE_MENU)
		unsupported_icon = self.treeview.render_icon(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_MENU)
		active_icon = self.treeview.render_icon(gtk.STOCK_APPLY, gtk.ICON_SIZE_MENU)
		unchecked_icon = self.treeview.render_icon(gtk.STOCK_DIALOG_WARNING, gtk.ICON_SIZE_MENU)
		unactive_icon = self.treeview.render_icon(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)
		gtk.gdk.threads_leave()
		
		for service, links in self.sort_links(link_list).items():
			if links != []:
				if service == cons.TYPE_UNSUPPORTED:
					gtk.gdk.threads_enter()
					service_iter = store.append(None, [unsupported_icon, service, service, 0, None, None, False, False])
					gtk.gdk.threads_leave()
					for link in links:
						gtk.gdk.threads_enter()
						store.append(service_iter, [unchecked_icon, link, link, 0, None, None, False, False])
						gtk.gdk.threads_leave()
				else:
					gtk.gdk.threads_enter()
					service_iter = store.append(None, [service_icon, service, service, 0, None, None, False, False])
					gtk.gdk.threads_leave()
					for link in links:
						if self.cancel_check:
							self.cancel_check = False
							wait.destroy()
							raise Exception("Check Links cancelled")
						check, plugin_type = self.check_links(service) 
						file_name, size, size_unit = check(link)
						if file_name:
							if size > 0:
								icon = active_icon
								marked = True
							else:
								icon = unchecked_icon
								marked = False
						else:
							icon = unactive_icon
							marked = False
							file_name = link
						print file_name, size, size_unit
						gtk.gdk.threads_enter()
						store.append(service_iter, [icon, link, file_name, size, size_unit, plugin_type, marked, marked])
						self.treeview.expand_row(store.get_path(service_iter), True)
						gtk.gdk.threads_leave()
		gtk.gdk.threads_enter()
		buffer.set_text("")
		wait.destroy()
		gtk.gdk.threads_leave()
	
	def cancel(self, window, event):
		"""Esc key"""
		if event.keyval == 65307:
			window.progress.set_text(_("Check Canceled!"))
			self.cancel_check = True
	
	def close(self, widget=None, other=None):
		""""""
		self.destroy()
	
if __name__ == "__main__":
	x = InputLinks(None, None, None)
	gtk.main()