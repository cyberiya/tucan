###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion crak@tucaneando.com
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

import threading
import time
import curses
import logging
logger = logging.getLogger(__name__)

from no_ui import NoUi

STATUS_LINES = 1
DOWNLOAD_LINES = 10
LOG_LINES = 8

class LogStream:
	""""""
	def __init__(self):
		""""""
		self.length = LOG_LINES-2
		self.new_buffer = []
		self.old_buffer = []

	def write(self, message):
		""""""
		self.new_buffer.append(str(message))
		
	def flush(self):
		""""""
		pass
		
	def readlines(self):
		""""""
		if len(self.new_buffer) > 0:
			cont = 1
			for line in self.new_buffer:
				tmp = self.new_buffer[0]
				del self.new_buffer[0]
				self.old_buffer.append(tmp)
				if cont >= self.length:
					break
			return self.old_buffer[-self.length:]

class Cli(NoUi):
	""""""		
	def __init__(self, *kwargs):
		""""""		
		#set logger
		self.stream = LogStream()
		handler = logging.StreamHandler(self.stream)
		handler.setLevel(logging.INFO)
		handler.setFormatter(logging.Formatter('%(levelname)-7s %(message)s'))
		logging.getLogger("").addHandler(handler)
				
		NoUi.__init__(self, *kwargs)
		self.quit_question = False

	def run(self, screen):
		""""""
		#set default screen
		self.screen = screen
		try:
			self.screen.nodelay(1)
			#curses.curs_set(0)
			self.screen.leaveok(1)

			self.status_win = self.screen.derwin(STATUS_LINES, 80, 0, 0)
			self.download_win = self.screen.derwin(DOWNLOAD_LINES, 80, 2, 0)
			self.log_win = self.screen.derwin(LOG_LINES, 80, 16, 0)
		except curses.error, e:
			logger.warning(e)
			
		#load links file
		th = threading.Thread(group=None, target=self.load_file, name=None)
		th.start()
		
		while True:
		#while len(self.download_manager.active_downloads + self.download_manager.pending_downloads) > 0:
		#	self.download_manager.update()
		#	print "Active:", [download.name for download in self.download_manager.active_downloads]
			#self.update_status()
			self.parse_input()
			self.update_log()
			curses.doupdate()
			time.sleep(0.5)
		self.quit()
		
	def parse_input(self):
		""""""
		try:
			input = self.screen.getkey()
		except curses.error:
			if not self.quit_question:
				self.update_status()
		else:
			if self.quit_question:
				if input.lower() == "y":
					self.quit()
				else:
					self.quit_question = False
					self.update_status()
			else:
				if input.lower() == "q":
					self.quit_question = True
					self.question()
				else:
					self.update_status()
					
	def update_log(self):
		""""""
		lines = self.stream.readlines()
		if lines:
			self.log_win.erase()
			for i in range(len(lines)):
				self.log_win.addstr(i, 0, lines[i])
			self.log_win.noutrefresh()

	def update_status(self):
		""""""				
		self.status_win.erase()
		self.status_win.addstr(0, 0, "Downstream: %s KB/s \tTotal %s \tActive %s \tComplete %s" % (0,0,0,0), curses.A_BOLD)
		self.status_win.noutrefresh()

	def question(self):
		""""""
		self.status_win.erase()
		self.status_win.addstr(0, 0, "Are you sure you want to quit? [y/N]", curses.A_STANDOUT)
		self.status_win.noutrefresh()
		