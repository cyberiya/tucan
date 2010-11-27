###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
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

import time
import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from queue import Queue, Package, File, Link

import cons

class QueueModel(gtk.GenericTreeModel, Queue):
	""""""
	def __init__(self):
		""""""
		gtk.GenericTreeModel.__init__(self)
		Queue.__init__(self)
		self.column_types = (gtk.gdk.Pixbuf, str, int, int, int, int)
		
	def set_value(self, id, key, value):
		""""""
		path = self.on_get_path(id)
		self.row_changed(path, self.get_iter(path))
		Queue.set_value(self, id, key, value)

	def on_get_flags(self):
		""""""
		return gtk.TREE_MODEL_ITERS_PERSIST

	def on_get_n_columns(self):
		""""""
		return len(self.column_types)

	def on_get_column_type(self, num):
		""""""
		if num < len(self.column_types):
			return self.column_types[num]

	def on_get_iter(self, path):
		""""""
		print path
		if path:
			packages = self.get_children()
			if path[0] < len(packages):
				package = packages[path[0]]
				if len(path) > 1:
					files = self.get_children(package.id)
					if path[1] < len(files):
						file = files[path[1]]
						if len(path) > 2:
							links = self.get_children(file.id)
							if path[2] < len(links):
								return links[path[2]].id
						else:
							return file.id
				else:
					return package.id

	def on_get_path(self, iter_id):
		""""""
		if iter_id:
			package_cont = -1
			file_cont = -1
			link_cont = -1
			for item in self.items:
				if isinstance(item, Package):
					package_cont += 1
					if item.id == iter_id:
						return (package_cont, )
					else:
						file_cont = -1
						link_cont = -1
				elif isinstance(item, File):
					file_cont += 1
					if item.id == iter_id:
						return (package_cont, file_cont)
					else:
						link_cont = -1
				elif isinstance(item, Link):
					link_cont += 1
					if item.id == iter_id:
						return (package_cont, file_cont, link_cont)

	def on_get_value(self, iter_id, column):
		""""""
		item = self.get_item(iter_id)
		if column is 0:
			return None
		if column is 1:
			if isinstance(item, Link):
				return item.plugin
			else:
				return item.name
		elif column is 2:
			return item.get_progress()
		elif column is 3:
			return item.current_size
		elif column is 4:
			return item.total_size
		elif column is 5:
			return item.current_speed

	def on_iter_next(self, iter_id):
		""""""
		item = self.get_item(iter_id)
		if item:
			items = self.get_children(item.parent_id)
			ind = items.index(item)
			if ind+1 < len(items):
				return items[ind+1].id

	def on_iter_children(self, iter_id):
		""""""
		items = self.get_children(iter_id)
		if items:
			return items[0].id

	def on_iter_has_child(self, iter_id):
		""""""
		items = self.get_children(iter_id)
		if items:
			return True

	def on_iter_n_children(self, iter_id):
		""""""
		items = self.get_children(iter_id)
		if items:
			return len(items)
		else:
			return 0

	def on_iter_nth_child(self, iter_id, n):
		""""""
		assert n >= 0
		items = self.get_children(iter_id)
		if n < len(items):
			return items[n].id

	def on_iter_parent(self, iter_id):
		""""""
		item = self.get_item(iter_id)
		if item:
			return item.parent_id

class GenericTreeModelExample:
	def delete_event(self, widget, event, data=None):
		gtk.main_quit()
 
	def __init__(self):
		# Create a new window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
 
		self.window.set_size_request(600, 400)
 
		self.window.connect("delete_event", self.delete_event)
		
		
		PATH1 = '/home/user/file.part1.rar'
		PATH2 = '/home/user/file.part2.rar'
		SIZE = 1024
		SIZE2 = 2048
		LINK1 = 'megaupload.anonymous_upload'
		LINK2 = 'rapidshare.anonymous_upload'

		FILE_LIST = [
		(PATH1, SIZE, [LINK1, LINK2]), 
		(PATH2, SIZE, [LINK1, LINK2])]
		
		FILE_LIST2 = [
		(PATH1, SIZE2, [LINK1, LINK2, LINK1]), 
		(PATH2, SIZE2, [LINK1, LINK2]), 
		(PATH2, SIZE2, [LINK1, LINK2])]
		
		FILE_LIST3 = [
		(PATH2, SIZE, [LINK1, LINK2, LINK1])]

		self.listmodel = QueueModel()
		self.listmodel.add_package(FILE_LIST)
		self.listmodel.add_package(FILE_LIST2)
		self.listmodel.add_package(FILE_LIST3)
 
		# create the TreeView
		self.treeview = gtk.TreeView()
		

		# create the TreeViewColumns to display the data
		column_names = ['Icon','Name','Progress','Current size','Total size','Speed']
		self.tvcolumn = [None] * len(column_names)

		for n in range(0, len(column_names)):
			if column_names[n] == 'Progress':
				cell = gtk.CellRendererProgress()
				self.tvcolumn[n] = gtk.TreeViewColumn(column_names[n], cell, value=n)
			elif column_names[n] == 'Icon':
				cell = gtk.CellRendererPixbuf()
				self.tvcolumn[n] = gtk.TreeViewColumn(column_names[n], cell, pixbuf=n)
			else:
				cell = gtk.CellRendererText()
				self.tvcolumn[n] = gtk.TreeViewColumn(column_names[n], cell, text=n)
			if column_names[n] == 'Progress':
				self.tvcolumn[n].set_min_width(150)
			self.treeview.append_column(self.tvcolumn[n])

		self.scrolledwindow = gtk.ScrolledWindow()
		self.scrolledwindow.add(self.treeview)
		self.window.add(self.scrolledwindow)
		self.treeview.set_model(self.listmodel)
		self.window.show_all()
		
	def update(self):
		""""""
		for item in self.listmodel.items:
			self.listmodel.set_value(item.id, "current_size", item.current_size+10)
		if item.current_size != item.total_size:
			return True

if __name__ == "__main__":
	g = GenericTreeModelExample()
	gobject.timeout_add(1000, g.update)
	gtk.main()
