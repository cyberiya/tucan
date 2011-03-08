###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
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

from base_types import Package, File, Link, STATUS_HIERARCHY

import cons

class Queue:
	""""""
	def __init__(self):
		""""""
		self.items = []

	def update_cb(self, id, parent=None, status=None):
		"""updates row and propagates status to parent"""
		if parent:
			self.propagate_status(parent, status)

	def sort_status(self, new_status, old_status):
		""""""
		status = STATUS_HIERARCHY
		return status[min(status.index(new_status), status.index(old_status))]

	def propagate_status(self, parent, status):
		""""""
		#check if the status change affects the parent
		if parent.status != status:
			#find the appropriate status in the brotherhood
			for item in self.get_children(parent.id):
				status = self.sort_status(item.status, status)
			#check again if the status change affects the parent
			if parent.status != status:
				parent.set_status(status)
				if parent.parent:
					self.propagate_status(parent.parent, status)

	def add_package(self, file_list, name=None):
		""""""
		if not name:
			name ="package-%s" % time.strftime("%Y%m%d%H%M%S")
		package = Package(self.update_cb, name)
		self.items.append(package)
		package_total_size = 0
		for path, size, links in file_list:
			file = File(self.update_cb, package, path)
			self.items.append(file)
			file_total_size = 0
			for plugin in links:
				file_total_size += size
				link = Link(self.update_cb, file, plugin)
				link.set_total_size(size)
				self.items.append(link)
			file.set_total_size(file_total_size)
			package_total_size += file.total_size
		package.set_total_size(package_total_size)
		return package

	def delete(self, item):
		""""""
		if item:
			if item.type == cons.ITEM_TYPE_PACKAGE:
				self.delete_package(item)
			elif item.type == cons.ITEM_TYPE_FILE:
				self.delete_file(item)
			elif item.type == cons.ITEM_TYPE_LINK:
				self.delete_link(item)

	def delete_package(self, package):
		""""""
		files = self.get_children(package.id)
		self.items.remove(package)
		for file in files:
			links = self.get_children(file.id)
			self.items.remove(file)
			for link in links:
				self.items.remove(link)

	def delete_file(self, file):
		""""""
		if len(self.get_children(file.parent_id)) > 1:
			links = self.get_children(file.id)
			self.items.remove(file)
			for link in links:
				self.items.remove(link)
			package = self.get_item(file.parent_id)
			package.current_size -= file.current_size
			package.set_total_size(package.total_size - file.total_size)
		else:
			self.delete(file.parent)

	def delete_link(self, link):
		""""""
		if len(self.get_children(link.parent_id)) > 1:
			self.items.remove(link)
			file = self.get_item(link.parent_id)
			package = self.get_item(file.parent_id)
			file.current_size -= link.current_size
			file.set_total_size(file.total_size - link.total_size)
			package.current_size -= link.current_size
			package.set_total_size(package.total_size - link.total_size)
		else:
			self.delete(link.parent)
			
	def move_up(self, item):
		""""""
		self.move(item, -1)

	def move_down(self, item):
		""""""
		self.move(item, 1)

	def move(self, item, direction=-1):
		"""direction : -1 if the item goes up, 1 if it goes down."""
		if item:
			ind = self.items.index(item)
			items = self.get_children(item.parent_id)
			tmp = items.index(item) + direction
			if tmp >= 0 and tmp < len(items):
				ind2 = self.items.index(items[tmp])
				for type in [cons.ITEM_TYPE_PACKAGE, cons.ITEM_TYPE_FILE, cons.ITEM_TYPE_LINK]:
					if item.type == type and items[tmp].type == type:
						self.swap(ind, ind2, self.get_length(item.id), self.get_length(items[tmp].id))
						break

	def swap(self, old, new, l1, l2):
		""""""
		if old > new:
			old,new,l1,l2 = new,old,l2,l1
		self.items[old:old+l2],self.items[old+l2:old+l2+l1] = self.items[new:new+l2], self.items[old:old+l1]


	def get_length(self, id):
		""""""
		l = 1
		for item in self.get_children(id):
			l += 1
			subitems = self.get_children(item.id)
			for subitem in subitems:
				l += 1
		return l

	def get_item(self, id):
		""""""
		if id:
			for item in self.items:
				if item.id == id:
					return item

	def get_children(self, id=None):
		""""""
		return [item for item in self.items if item.parent_id == id]

	def for_all_children(self, id, func, *args):
		""""""
		children = self.get_children(id)
		if children:
			for child in children:
				func(child.id, child, *args)
			return True
