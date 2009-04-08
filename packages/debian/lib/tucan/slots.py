###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion crakotaku(at)yahoo.es
## Copyright (C) 2008-2009 Paco Salido beakman(at)riseup.net
## Copyright (C) 2008-2009 JM Cordero betic0(at)gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
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

WAIT_LIMIT = 300

class Slots:
	""""""
	def __init__(self, slots):
		""""""
		self.limit = False
		self.end_wait = 0
		self.max = slots
		self.slots = slots
		
	def get_slot(self):
		""""""
		if self.slots > 0:
			if time.time() > self.end_wait:
				self.limit = False
				self.slots -= 1
				return True
			
	def add_wait(self):
		""""""
		logger.warning("Wait 5 minutes.")
		self.limit = True
		self.end_wait = time.time() + WAIT_LIMIT
			
	def return_slot(self):
		""""""
		if self.slots < self.max:
			self.slots += 1
			return True
