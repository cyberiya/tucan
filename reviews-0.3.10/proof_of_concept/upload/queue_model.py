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

import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk

import cons
from queue import *

class QueueModel(gtk.GenericTreeModel):
	column_types = (gtk.gdk.Pixbuf, str, int, int, int, int)

	def __init__(self, queue):
		gtk.GenericTreeModel.__init__(self)
		self.queue = queue
		self.items = queue.items
		return
		
	def get_index(self, node):
		packages = self.queue.get_children()
		length = 0
		for i in range(0, node[0]):
			length += self.queue.get_length(packages[i].id)
		if len(node) > 1:
			length += 1
			files = self.queue.get_children(packages[node[0]].id)
			for i in range(0, node[1]):
				length += self.queue.get_length(files[i].id)
		if len(node) > 2:
			length += 1
			length += node[2]
		return length

	def get_column_names(self):
		return self.column_names[:]

	def on_get_flags(self):
		return 0

	def on_get_n_columns(self):
		return len(self.column_types)

	def on_get_column_type(self, n):
		return self.column_types[n]

	def on_get_iter(self, path):
		return path

	def on_get_path(self, node):
		return self.get_index(node)

	def on_get_value(self, node, column):
		if column is 0:
			return None
		if column is 1:
			if isinstance(self.items[self.get_index(node)], Link):
				return self.items[self.get_index(node)].plugin
			else:
				return self.items[self.get_index(node)].name
		elif column is 2:
			return self.items[self.get_index(node)].get_progress()
		elif column is 3:
			return self.items[self.get_index(node)].current_size
		elif column is 4:
			return self.items[self.get_index(node)].total_size
		elif column is 5:
			return self.items[self.get_index(node)].current_speed

	def on_iter_next(self, node):
		try:
			if node != None:
				item = self.items[self.get_index(node)]
				if node[-1] == len(self.queue.get_children(item.parent_id))-1: # last node at level
					return None
				return node[:-1] +(node[-1]+1,)
		except IndexError:
			return None

	def on_iter_children(self, node):
		if node == None: # top of tree
			return(0,)
		if len(node) >= 3: # no more levels
			return None
		return node +(0,)

	def on_iter_has_child(self, node):
		item = self.items[self.get_index(node)]
		return node == None or not isinstance(item, Link)

	def on_iter_n_children(self, node):
		if node:
			item = self.items[self.get_index(node)]
			return len(self.queue.get_children(item.id))
		return len(self.queue.get_children())

	def on_iter_nth_child(self, node, n):
		if node:
			return node +(0,)
		else:
			return (n,)

	def on_iter_parent(self, child):
		assert child != None
		if child:
			return child[:-1]
		else:
			return None


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
		SIZE2 = 25
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
		
		queue = Queue()
		queue.add_package(FILE_LIST)
		queue.add_package(FILE_LIST2)
		queue.add_package(FILE_LIST3)
		queue.items[0].current_size = 1245
 
 
		self.listmodel = QueueModel(queue)
 
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


if __name__ == "__main__":
	gtmexample = GenericTreeModelExample()
	gtk.main()
