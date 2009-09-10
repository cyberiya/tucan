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

import time
import logging
logger = logging.getLogger(__name__)

from no_ui import NoUi

class Cli(NoUi):
	""""""
	def __init__(self, conf, links_file=None):
		""""""
		NoUi.__init__(self, conf, links_file)
		
	def run(self):
		""""""
		while len(self.download_manager.active_downloads + self.download_manager.pending_downloads) > 0:
			self.download_manager.update()
			print "Active:", [download.name for download in self.download_manager.active_downloads]
			time.sleep(1)
		self.quit()
