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


	def swap(self, id, up=True):
		""""""
		item = self.get_item(id)
		if item:
			l = 0 #Number of items to move
			items = self.get_children(id)
			if items:
				l += 1
				for item in items:
					l += 1
					subitems = self.get_children(item.id)
					for subitem in subitems:
						l += 1
			else:
				l = 1 #Item is a link
			
			item = self.get_item(id)
			
			#Get all the items that are the same kind of the item to be moved
			if isinstance(item, Link):
				tmp = [it for it in enumerate(self.items) if isinstance(it[1], Link)]
			if isinstance(item, File):
				tmp = [it for it in enumerate(self.items) if isinstance(it[1], File)]
			if isinstance(item, Package):
				tmp = [it for it in enumerate(self.items) if isinstance(it[1], Package)]

			old = self.items.index(item) #Old index of the item
			new = None #New index of the item
			
			#Find the index of the item suitable for the swap
			if up:
				tmp = [ind[0] for ind in tmp if ind[1].parent_id == item.parent_id and ind[0] < old]
				if tmp:
					new = max(tmp)
			else:
				tmp = [ind[0] for ind in tmp if ind[1].parent_id == item.parent_id and ind[0] > old]
				if tmp:
					new = min(tmp)
			if new:
				#A swap is possible ?
				if (up and new < old) or (not up and old < new):
					d = old - new
					i = old
					j = new
				
					#Swap the two slices
					self.items[i:i+d],self.items[j:j+l] = self.items[j:j+d],self.items[i:i+l]

	def move_up(self, id):
		""""""
		self.swap(id, True)


	def move_down(self, id):
		""""""
		self.swap(id, False)

	def get_value(self, id, key):
		""""""
		pass

	def set_value(self, id, key, value):
		""""""
		pass

	def get_item(self, id):
		""""""
		for item in self.items:
			if item.id == id:
				return item

	def get_children(self, id=None):
		""""""
		children = []
		for item in self.items:
			if item.parent_id == id:
				children.append(item)
		return children
		
	def update_link(self, id, delete=False, status=None):
		""""""
		pass
	def update_file(self, id):
		""""""
		pass
	def update_package(self, id):
		""""""
		pass

