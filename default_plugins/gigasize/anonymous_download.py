###############################################################################
##	Tucan Project

##	Copyright (C) 2008 Fran Lupion Crakotak(at)yahoo.es
##	Copyright (C) 2008 Paco Salido beakman(at)riseup.net
##	Copyright (C) 2008 JM Cordero betic0(at)gmail.com

##	This program is free software; you can redistribute it and/or modify
##	it under the terms of the GNU General Public License as published by
##	the Free Software Foundation; either version 2 of the License, or
##	(at your option) any later version.

##	This program is distributed in the hope that it will be useful,
##	but WITHOUT ANY WARRANTY; without even the implied warranty of
##	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##	GNU General Public License for more details.

##	You should have received a copy of the GNU General Public License
##	along with this program; if not, write to the Free Software
##	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import cons

from download_plugin import DownloadPlugin
from slots import Slots

class AnonymousDownload(DownloadPlugin, Slots):
	""""""
	def __init__(self):
		""""""
		Slots.__init__(self, 1)
		DownloadPlugin.__init__(self)
		
	def add(self, path, link, file_name):
		""""""
		if self.get_slot():
			print path, link, file_name
		else:
			self.add_wait()
			
	def delete(self, file_name):
		""""""
		if self.stop(file_name):
			print self.return_slot()
