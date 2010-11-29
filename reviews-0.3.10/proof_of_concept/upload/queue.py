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

import uuid
import time
import os.path
import logging
logger = logging.getLogger(__name__)

import cons

class Item:
	""""""
	def __init__(self, parent_id=None):
		""""""
		self.id = str(uuid.uuid1())
		self.parent_id = parent_id
		self.status = cons.STATUS_PEND
		self.current_size = 0
		self.total_size = 0
		self.current_speed = 0

	def get_progress(self):
		""""""
		return int((float(self.current_size)/self.total_size)*100)
		
	def get_active(self):
		""""""
		if self.status in [cons.STATUS_ACTIVE, cons.STATUS_WAIT]:
			return True

class Link(Item):
	""""""
	def __init__(self, parent_id, plugin):
		""""""
		Item.__init__(self, parent_id)
		self.url = None
		self.plugin = plugin

class File(Item):
	""""""
	def __init__(self, parent_id, path):
		""""""
		Item.__init__(self, parent_id)
		self.path = path
		self.name = os.path.basename(path)

class Package(Item):
	""""""
	def __init__(self, name, desc=""):
		""""""
		Item.__init__(self)
		self.name = name
		self.desc = desc #same for all the files

class Queue:
	""""""
	def __init__(self):
		""""""
		self.items = [] #main list [package]

	def add_package(self, file_list, name=None):
		""""""
		if not name:
			name ="package-%s" % time.strftime("%Y%m%d%H%M%S")
		package = Package(name)
		self.items.append(package)
		for path, size, links in file_list:
			file = File(package.id, path)
			self.items.append(file)
			for plugin in links:
				file.total_size += size
				link = Link(file.id, plugin)
				link.total_size = size
				self.items.append(link)
			package.total_size += file.total_size
		return package.id

	def delete(self, id):
		""""""
		item = self.get_item(id)
		if item and not item.get_active():
			if isinstance(item, Package):
				self.delete_package(item)
			elif isinstance(item, File):
				self.delete_file(item)
			elif isinstance(item, Link):
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
			self.get_item(file.parent_id).total_size -= file.total_size
			links = self.get_children(id)
			self.items.remove(file)
			for link in links:
				self.items.remove(link)
		else:
			self.delete(file.parent_id)

	def delete_link(self, link):
		""""""
		if len(self.get_children(link.parent_id)) > 1:
			file = self.get_item(link.parent_id)
			package = self.get_item(file.parent_id)
			file.total_size -= link.total_size
			package.total_size -= link.total_size
			self.items.remove(link)
		else:
			self.delete(link.parent_id)

	def swap(self, old, new, l):
		""""""
		d = abs(old - new)
		self.items[old:old+d],self.items[new:new+l] = self.items[new:new+d], self.items[old:old+l]

	def get_length(self, id):
		""""""
		l = 1
		for item in self.get_children(id):
			l += 1
			subitems = self.get_children(item.id)
			for subitem in subitems:
				l += 1
		return l

	def move_up(self, id):
		""""""
		item = self.get_item(id)
		if item:
			if isinstance(item, Package):
				self.move_up_package(item)
			elif isinstance(item, File):
				self.move_up_file(item)
			elif isinstance(item, Link):
				self.move_up_link(item)

	def move_up_package(self, item):
		""""""
		ind = self.items.index(item)
		packages = self.get_children()
		tmp = packages.index(item)-1
		if tmp >= 0 and tmp < len(packages):
			if isinstance(packages[tmp], Package):
				ind2 = self.items.index(packages[tmp])
				self.swap(ind, ind2, self.get_length(item.id))

	def move_up_file(self, item):
		""""""
		ind = self.items.index(item)
		files = self.get_children(item.parent_id)
		tmp = files.index(item)-1
		if tmp >= 0 and tmp < len(files):
			if isinstance(files[tmp], File):
				ind2 = self.items.index(files[tmp])
				self.swap(ind, ind2, self.get_length(item.id))

	def move_up_link(self, item):
		""""""
		ind = self.items.index(item)
		if ind-1 >= 0:
			if isinstance(self.items[ind-1], Link):
				self.swap(ind, ind-1, 1)

	def move_down(self, id):
		""""""
		item = self.get_item(id)
		if item:
			if isinstance(item, Package):
				self.move_down_package(item)
			elif isinstance(item, File):
				self.move_down_file(item)
			elif isinstance(item, Link):
				self.move_down_link(item)

	def move_down_package(self, item):
		""""""
		ind = self.items.index(item)
		packages = self.get_children()
		tmp = packages.index(item)+1
		if tmp >= 0 and tmp < len(packages):
			if isinstance(packages[tmp], Package):
				ind2 = self.items.index(packages[tmp])
				self.swap(ind, ind2, self.get_length(item.id))

	def move_down_file(self, item):
		""""""
		ind = self.items.index(item)
		files = self.get_children(item.parent_id)
		tmp = files.index(item)+1
		if tmp >= 0 and tmp < len(files):
			if isinstance(files[tmp], File):
				ind2 = self.items.index(files[tmp])
				self.swap(ind, ind2, self.get_length(item.id))

	def move_down_link(self, item):
		""""""
		ind = self.items.index(item)
		if ind+1 < len(self.items):
			if isinstance(self.items[ind+1], Link):
				self.swap(ind, ind+1, 1)

	def get_value(self, id, key):
		""""""
		item = self.queue.get_item(id)
		if item:
			return getattr(item, key)

	def set_value(self, id, key, value):
		""""""
		item = self.get_item(id)
		if item:
			setattr(item, key, value)

	def get_item(self, id):
		""""""
		for item in self.items:
			if item.id == id:
				return item

	def get_children(self, id=None):
		""""""
		return [item for item in self.items if item.parent_id == id]
