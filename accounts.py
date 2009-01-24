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

class Accounts:
	""""""
	def __init__(self, config, section, cookie):
		""""""
		self.config = config
		self.active = False
		self.section = section
		self.cookie = cookie
		self.accounts = self.config.get_accounts(self.section)
		for account in self.accounts.values():
			if account[1]:
				self.active = True
		
	def get_cookie(self):
		""""""
		result = None
		for user, data in self.accounts.items():
			if data[1]:
				cookie = self.cookie.get_cookie(user, data[0])
				if cookie:
					result = cookie
				else:
					self.accounts[user] = (data[0], False)
					self.config.set_accounts(self.section, self.accounts)
					print self.accounts
		if result:
			return result
		else:
			self.active = False