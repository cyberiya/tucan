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

import urllib
import cookielib
import hashlib

class PremiumCookie:
	""""""
	def __init__(self):
		self.md5pw=''

	def get_cookie(self, user, password, url=None):
		""""""
		# create a cache of the MD5 hashed password
		if len(self.md5pw) == 0:
			self.md5pw = hashlib.md5(password).hexdigest()

		return '&username='+user+'&passwordmd5='+self.md5pw

if __name__ == "__main__":
	account_hasher = PremiumCookie()
	print account_hasher.get_cookie("caffein","kingkong1944")
