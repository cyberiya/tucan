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
from core.log_stream import LogStream

STATUS_LINES = 1
DOWNLOAD_LINES = 10
LOG_LINES = 8

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
		self.win_chars = 1

	def run(self, screen):
		""""""
		self.screen = screen
		self.screen.nodelay(1)
		y, self.win_chars = self.screen.getmaxyx()
		try:
			curses.curs_set(0)

		except:
			logger.warning("Could not hide the cursor")

		#set default screen
		self.status_win = self.screen.derwin(STATUS_LINES, self.win_chars, 0, 0)
		self.download_win = self.screen.derwin(DOWNLOAD_LINES, self.win_chars, 2, 0)
		self.log_win = self.screen.derwin(LOG_LINES, self.win_chars, 15, 0)

		#load links file
		th = threading.Thread(group=None, target=self.load_file, name=None)
		th.start()
		
		while True:
		#while len(self.download_manager.active_downloads + self.download_manager.pending_downloads) > 0:
		#	self.download_manager.update()
		#	print "Active:", [download.name for download in self.download_manager.active_downloads]
			#self.update_status()
			y, self.win_chars = self.screen.getmaxyx()
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
		lines = self.stream.readlines(LOG_LINES-2)
		if lines:
			self.log_win.erase()
			for i in range(len(lines)):
				self.log_win.addnstr(i, 0, lines[i], self.win_chars)
			self.log_win.noutrefresh()

	def update_status(self):
		""""""				
		self.status_win.erase()
		self.status_win.addnstr(0, 0, "Downstream: %s KB/s \tTotal %s \tActive %s \tComplete %s" % (0,0,0,0), self.win_chars, curses.A_BOLD)
		self.status_win.noutrefresh()

	def question(self):
		""""""
		self.status_win.erase()
		self.status_win.addnstr(0, 0, "Are you sure you want to quit? [y/N]", self.win_chars, curses.A_STANDOUT)
		self.status_win.noutrefresh()
		