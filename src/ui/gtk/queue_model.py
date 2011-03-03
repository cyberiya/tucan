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

from core.queue import Queue, Package, File, Link

import core.cons as cons


class Cache:
	""""""
	def __init__(self):
		""""""
		self.id_cache = {}
		self.path_cache = {}
		
	def get_id(self, path):
		""""""
		if path in self.id_cache:
			return self.id_cache[path]

	def get_path(self, id):
		""""""
		if id in self.path_cache:
			return self.path_cache[id]
	
	def set(self, id, path):
		""""""
		self.id_cache[path] = id
		self.path_cache[id] = path
		
	def clear(self):
		""""""
		del self.id_cache
		del self.path_cache
		self.id_cache = {}
		self.path_cache = {}
		
class QueueModel(gtk.GenericTreeModel, Queue):
	""""""
	def __init__(self, icons):
		""""""
		gtk.GenericTreeModel.__init__(self)
		Queue.__init__(self)
		self.column_types = (gtk.gdk.Pixbuf, str, int, int, int, int)
		self.cache = Cache()
		self.icons = icons

	def propagate_cb(self, id, parent=None, status=None):
		""""""
		Queue.propagate_cb(self, id, parent, status)
		self.update_row(id)

	def update_row(self, id):
		""""""
		path = self.on_get_path(id)
		self.row_changed(path, self.get_iter(path))
		
	def set_value(self, id, key, value):
		""""""
		self.update_row(id)
		Queue.set_value(self, id, key, value)

	def add_package(self, file_list, name=None):
		""""""
		id = Queue.add_package(self, file_list, name=None)
		path = self.on_get_path(id)
		self.row_inserted(path, self.get_iter(path))
		for item in self.get_children(id):
			path = self.on_get_path(item.id)
			self.row_inserted(path, self.get_iter(path))
			for subitem in self.get_children(item.id):
				path = self.on_get_path(subitem.id)
				self.row_inserted(path, self.get_iter(path))
		return id

	def delete(self, id):
		""""""
		path = self.on_get_path(id)
		self.row_deleted(path)
		Queue.delete(self, id)

	def move(self, id, direction):
		""""""
		item = self.get_item(id)
		path = self.on_get_path(item.parent_id)
		if path:
			iter = self.get_iter(path)
		else:
			iter = None
		prev = self.get_children(item.parent_id)
		self.cache.clear()
		Queue.move(self, id, direction)
		next = self.get_children(item.parent_id)
		self.rows_reordered(path, iter, [next.index(item) for item in prev])

	def on_get_flags(self):
		""""""
		return 0 #gtk.TREE_MODEL_ITERS_PERSIST

	def on_get_n_columns(self):
		""""""
		return len(self.column_types)

	def on_get_column_type(self, num):
		""""""
		if num < len(self.column_types):
			return self.column_types[num]

	def on_get_iter(self, path):
		""""""
		id = self.cache.get_id(path)
		if id:
			return id
		elif path:
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
								id = links[path[2]].id
								self.cache.set(id, path)
								return id
						else:
							self.cache.set(file.id, path)
							return file.id
				else:
					self.cache.set(package.id, path)
					return package.id

	def on_get_path(self, iter_id):
		""""""
		path = self.cache.get_path(iter_id)
		if path:
			return path
		elif iter_id:
			package_cont = -1
			file_cont = -1
			link_cont = -1
			for item in self.items:
				if item.type == cons.ITEM_TYPE_PACKAGE:
					package_cont += 1
					if item.id == iter_id:
						self.cache.set(iter_id, (package_cont, ))
						return (package_cont, )
					else:
						file_cont = -1
						link_cont = -1
				elif item.type == cons.ITEM_TYPE_FILE:
					file_cont += 1
					if item.id == iter_id:
						self.cache.set(iter_id, (package_cont, file_cont))
						return (package_cont, file_cont)
					else:
						link_cont = -1
				elif item.type == cons.ITEM_TYPE_LINK:
					link_cont += 1
					if item.id == iter_id:
						self.cache.set(iter_id, (package_cont, file_cont, link_cont))
						return (package_cont, file_cont, link_cont)

	def on_get_value(self, iter_id, column):
		""""""
		item = self.get_item(iter_id)
		if column is 0:
			return self.icons.get_icon(item.type, item.status)
		if column is 1:
			return str(item)
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
