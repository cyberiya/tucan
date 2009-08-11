#! /usr/bin/env python
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

import __builtin__
import os.path
import sys
import logging

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from gui import Gui

import url_open
import config
import cons

class Tucan:
	""""""
	def __init__(self):
		""""""
		#exception hook
		self.old_exception_hook = sys.excepthook
		sys.excepthook = self.exception_hook

		#configuration
		self.configuration = config.Config()
		sys.path.append(cons.PLUGIN_PATH)

		#globals
		__builtin__.max_downloads = self.configuration.getint(config.SECTION_MAIN, config.OPTION_MAX_DOWNLOADS)
		__builtin__.max_download_speed = self.configuration.getint(config.SECTION_MAIN, config.OPTION_MAX_DOWNLOAD_SPEED)

		#logging
		if os.path.exists(cons.LOG_FILE):
			if os.path.exists("%s.old" % cons.LOG_FILE):
				os.remove("%s.old" % cons.LOG_FILE)
			os.rename(cons.LOG_FILE, "%s.old" % cons.LOG_FILE)
		logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s %(levelname)s: %(message)s', filename=cons.LOG_FILE, filemode='w')
		self.logger = logging.getLogger(self.__class__.__name__)

		self.logger.info(cons.TUCAN_VERSION)
		self.logger.debug("OS: %s" % sys.platform)
		self.logger.debug("Main path: %s" % cons.PATH)
		self.logger.debug("Configuration path: %s" % cons.CONFIG_PATH)

		#proxy settings
		proxy_url, proxy_port = self.configuration.get_proxy()
		url_open.set_proxy(proxy_url, proxy_port)

		#global custom exit
		__builtin__.tucan_exit = self.exit

	def exception_hook(self, type, value, trace):
		""""""
		file_name = trace.tb_frame.f_code.co_filename
		line_no = trace.tb_lineno
		exception = type.__name__
		self.logger.critical("File %s line %i - %s: %s" % (file_name, line_no, exception, value))
		print self.old_exception_hook(type, value, trace)
		self.exit(-1)

	def exit(self, arg=0):
		""""""
		self.logger.debug("Exit: %s" % arg)
		sys.exit(arg)

if __name__ == "__main__":
	gobject.threads_init()
	t = Tucan()
	Gui(t.configuration)
	gtk.main()
