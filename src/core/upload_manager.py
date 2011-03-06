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
import threading
import logging
logger = logging.getLogger(__name__)

import cons

MAX_UPLOADS = 2

class UploadMockup(threading.Thread):
	""""""
	def __init__(self, item):
		""""""
		threading.Thread.__init__(self)
		self.item = item
		self.stop_flag = False

	def run(self):
		"""Parsing and Poster work"""
		speed = 1000000
		old_speed = 0
		while not self.stop_flag and self.item.current_size < self.item.total_size:
			time.sleep(0.5)
			self.item.update(speed, speed-old_speed)
			old_speed = speed
		if self.stop_flag:
			self.item.set_status(cons.STATUS_STOP)
		else:
			self.item.set_status(cons.STATUS_CORRECT)

	def stop(self):
		"""Set a flag so that it stops"""
		self.stop_flag = True

class UploadManager:
	""""""
	def __init__(self, queue):
		""""""
		self.queue = queue

		self.timer = None
		self.schedules = 0
		self.scheduling = False

		self.threads = {}

	def limit_not_reached(self):
		""""""
		cont = 0
		for id, th in self.threads.items():
			if th.isAlive():
				cont += 1
			else:
				del self.threads[id]
		return cont < MAX_UPLOADS

	def add_package(self, file_list):
		""""""
		id = self.queue.add_package(file_list)
		self.scheduler()
		return id
		
	def for_all_children(self, func, id, force):
		""""""
		children = self.queue.get_children(id)
		if children:
			for child in children:
				func(child.id, child, force)
			return True

	def start(self, id, item=None, force=True):
		""""""
		#item is only passed inside upload_manager
		if not item:
			item = self.queue.get_item(id)
		if item.status != cons.STATUS_CORRECT:
			if self.limit_not_reached() or force:
				#Start Links when not active
				if not self.for_all_children(self.start, id, force) and not item.get_active():
					logger.info("Started: %s" % item.get_name())
					item.set_status(cons.STATUS_ACTIVE)
					th = UploadMockup(item)
					th.start()
					self.threads[id] = th
			elif not force:
				if not self.for_all_children(self.start, id, force) and not item.get_active():
					logger.info("Pending: %s" % item.get_name())
					item.set_status(cons.STATUS_PEND)

	def stop(self, id, item=None, force=True):
		""""""
		#item is only passed inside upload_manager
		if not item:
			item = self.queue.get_item(id)
		if item.status != cons.STATUS_CORRECT:
			#Stop active Links if force 
			if not self.for_all_children(self.stop, id, force) and force or not item.get_active():
				item.set_status(cons.STATUS_STOP)
				logger.info("Stoped: %s" % item.get_name())
				if id in self.threads:
					self.threads[id].stop()

	def scheduled_start(self):
		""""""
		if self.limit_not_reached():
			items = [item for item in self.queue.items if item.type == cons.ITEM_TYPE_LINK]
			for item in items:
				if item.get_pending():
					self.start(item.id, item)
					if not self.limit_not_reached():
						break

	def keep_scheduling(self):
		""""""
		for item in self.queue.get_children():
			if item.get_pending() or item.get_active():
				return True

	def scheduler(self):
		""""""
		if not self.scheduling:
			self.scheduling = True
			if self.keep_scheduling():
				if self.schedules < 11:
					self.schedules += 1
				else:
					self.schedules = 0
					logger.debug("scheduled.")
				self.scheduled_start()
				if self.timer:
					self.timer.cancel()
				#self.timer = threading.Timer(5, self.scheduler)
				self.timer = threading.Timer(0.5, self.scheduler)
				self.timer.start()
			else:
				#print "all-complete"
				events.trigger_all_complete()
			self.scheduling = False

	def quit(self):
		""""""
		if self.timer:
			self.scheduling = True
			while self.timer.isAlive():
				self.timer.cancel()
				self.timer.join(0.5)
		for id, th in self.threads.items():
			while th.isAlive():
				th.stop_flag = True
				th.join(0.5)
