###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion Crakotak(at)yahoo.es
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

import cookielib

class Accounts:
	""""""
	def __init__(self, config, section):
		""""""
		self.config = config
		self.section = section
		self.active = False
		for account in self.config.get_accounts(self.section).values():
			if account[2]:
				self.active = True
		
	def get_cookie(self):
		""""""
		for account in self.config.get_accounts(self.section).values():
			if account[2]:
				cookie = cookielib.CookieJar()
				cookie._cookies = account[0]
				return cookie
			