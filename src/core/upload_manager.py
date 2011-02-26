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

MAX_UPLOADS = 1

class UploadManager:
	""""""
	def __init__(self, queue):
		""""""
		self.queue = queue

		self.timer = None
		self.schedules = 0
		self.scheduling = False

		self.threads = {}

	def get_active_threads(self):
		""""""
		cont = 0
		for id, th in self.threads.items():
			if th.isAlive():
				cont += 1
			else:
				self.threads.remove(id)
		return cont

	def add(self, file_list):
		""""""
		self.queue.add_package(file_list)
		self.scheduler()

	def start(self, id, item=None):
		""""""
		if not item:
			item = self.queue.get_item(id)
		if self.get_active_threads() < MAX_UPLOADS:
			#logging message
			th = threading.Thread()
			th.start()
			self.thread_list[id] = th

	def stop(self, id, item=None):
		""""""
		if not item:
			item = self.queue.get_item(id)
		if id in self.threads:
			self.threads[id].stop_flag = True
			#logging message

	def schedule(self):
		""""""
		items = [item for item in self.queue.items if isinstance(item, Link)]
		for item in items:
			if item.get_pending():
				self.start(item.id, item)
				break

	def keep_scheduling(self):
		""""""
		for item in self.queue.get_children():
			if item.status == cons.STATUS_PEND or item.get_active():
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
				self.schedule()
				if self.timer:
					self.timer.cancel()
				self.timer = threading.Timer(5, self.scheduler)
				self.timer.start()
			else:
				print "all complete"
				#events.trigger_all_complete()
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
