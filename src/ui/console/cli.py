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

import threading
import time
import curses
import logging
logger = logging.getLogger(__name__)

from no_ui import NoUi
from core.log_stream import LogStream

import core.cons as cons
import core.misc as misc

STATUS_LINES = 1
DOWNLOAD_LINES = 60
LOG_LINES = 50
WIDTH = 100

LINES_PER_DOWNLOAD = 3

class UIContext:
	Downloads = 0
	AddLinks  = 1
	Log       = 2
	Wizard    = 3

class Cli(NoUi):
	""""""
	def __init__(self, *kwargs):
		""""""
		#Setup logger to log events to this class
		self.stream = LogStream()
		handler = logging.StreamHandler(self.stream)
		handler.setLevel(logging.INFO)
		handler.setFormatter(logging.Formatter('%(levelname)-7s %(message)s'))
		logging.getLogger("").addHandler(handler)

		NoUi.__init__(self, *kwargs)

		#Set context tab
		self.context = UIContext.Downloads
		self.running = True
		self.quit_question = False
		self.win_height = 0
		self.win_chars = 0
		self.total_speed = 0
		self.th = None
		self.statistics_th = None


	def update_statistics(self):
		avg_counter = 0
		avg_speed   = 0
		while self.running:
			total_speed  = 0
			avg_counter += 1
			downloads = self.download_manager.complete_downloads + self.download_manager.active_downloads
			for download in downloads:
				total_speed += download.speed
			
			avg_speed += total_speed
			if avg_counter == 10:
				avg_counter = 0
				avg_speed = avg_speed / 5
				self.total_speed = int(avg_speed)
			self.download_manager.update()
			time.sleep(.1)


	def run(self, screen):
		""""""
		self.screen = screen
		self.screen.nodelay(1)
		try:
			curses.curs_set(0)
		except:
			logger.warning("Could not hide the cursor")

		#set default screen
		self.status_pad = curses.newpad(STATUS_LINES, WIDTH)
		self.main_pad   = curses.newpad(DOWNLOAD_LINES, WIDTH)
		self.log_pad    = curses.newpad(LOG_LINES, WIDTH)

		#load links file
		self.th = threading.Thread(group=None, target=self.load_links, name=None)
		self.th.start()

		#start statistics thread
		self.statistics_th = threading.Thread(group=None, target=self.update_statistics, name=None)
		self.statistics_th.start()

		current_context = UIContext.Downloads
		while self.running:
			self.win_height, self.win_chars = self.screen.getmaxyx()
			self.parse_input()

			self.update_status()

			# if the current view has changed clear the screen
			if self.context != current_context:
				self.clear_screen(self.context)
				current_context = self.context

			try:
				if self.context == UIContext.Downloads:
					self.update_main()
				elif self.context == UIContext.Log:
					self.update_log()

			except curses.error, e:
				logger.warning(e)

			curses.doupdate()
			time.sleep(0.5)

	def clear_screen(self, except_context):
		""""""
		if except_context != UIContext.Log:
			self.log_pad.clear()
			self.log_pad.refresh(0, 0, 2, 0, self.win_height-2, self.win_chars-1)
		if except_context != UIContext.Downloads:
			self.main_pad.clear()
			self.main_pad.refresh(0, 0, 2, 0, self.win_height-2, self.win_chars-1)

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
					self.set_status("Shutting down, please wait...")
					self.quit()
				else:
					self.quit_question = False
					self.update_status()
			else:
				if input.lower() == "q":
					self.quit_question = True
					self.set_status("Are you sure you want to quit? [y/N]")

				elif input.lower() =="l":
					self.context = UIContext.Log

				elif input.lower() =="d":
					self.context = UIContext.Downloads


	def update_main(self):
		""""""
		if self.win_height > 5:
			cont = 0
			self.main_pad.erase()
			downloads = self.download_manager.complete_downloads + self.download_manager.active_downloads
			while len(downloads)*LINES_PER_DOWNLOAD > DOWNLOAD_LINES:
				del downloads[0]
			for download in downloads:
				service = "[]"
				for link in download.links:
					if link.active:
						service = "[%s %s]" %(link.plugin_type, link.service)
				percent = "%i%s" % (int(download.progress), "%")
				speed = "%s KB/s" % download.speed
				size = "%i%s / %i%s" % (download.actual_size, download.actual_size_unit, download.total_size, download.total_size_unit)
				time = str(misc.calculate_time(download.time))
				self.main_pad.addnstr(cont, 1, download.name, WIDTH)
				self.main_pad.addnstr(cont+1, 5, "%s %s \t%s \t%s \t%s" % (percent, service, size, speed, time), WIDTH)
				cont += LINES_PER_DOWNLOAD
			#2 blank lines at top
			cont +=2
			remain = self.win_height-cont
			start = 0
			while remain <= 5:
					remain += LINES_PER_DOWNLOAD
					start += LINES_PER_DOWNLOAD
			#pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol
			self.main_pad.noutrefresh(start, 0, 2, 0, cont-start, self.win_chars-1)
			return remain

	def update_log(self):
		""""""
		lines = self.stream.readnlines(self.win_height-1)
		if lines:
			self.log_pad.erase()
			for i in range(len(lines)):
				self.log_pad.addnstr(i, 0, lines[i], WIDTH, curses.A_DIM)
			self.log_pad.noutrefresh(0, 0, 2, 0, self.win_height-1, self.win_chars-1)

	def update_status(self):
		""""""
		active = len(self.download_manager.active_downloads)
		complete = len(self.download_manager.complete_downloads)
		total = len(self.download_manager.pending_downloads + self.download_manager.active_downloads + self.download_manager.complete_downloads)
		self.set_status("Downstream: %s KB/s \tTotal %s \tActive %s \tComplete %s" % (self.total_speed, total, active, complete), curses.A_BOLD)

	def set_status(self, message, attr=curses.A_STANDOUT):
		""""""
		self.status_pad.erase()
		self.status_pad.addnstr(0, 0, message, WIDTH, attr)
		self.status_pad.noutrefresh(0, 0, 0, 0, 0, self.win_chars-1)
		if attr == curses.A_STANDOUT:
			curses.doupdate()

	def quit(self):
		""""""
		self.stop()
		while self.th.isAlive():
			self.th.join(0.5)
		self.running = False
		NoUi.quit(self)
