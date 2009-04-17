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

import urllib2
import logging
logger = logging.getLogger(__name__)

import cons

PROXY = None

def set_proxy(url, port=0):
	""""""
	if url:
		PROXY = {"http": "%s:%i" % (url, port)}
		logger.info("Using proxy: %s:%i" % (url, port))
	else:
		PROXY = None
		logger.info("Proxy Disabled.")

class URLOpen:
	""""""
	def __init__(self, cookie=None):
		""""""
		if PROXY:
			self.opener = urllib2.build_opener(urllib2.ProxyHandler(PROXY), urllib2.HTTPCookieProcessor(cookie))
		else:
			self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		
	def open(self, url, form=None):
		""""""
		try:
			if form:
				handler = self.opener.open(urllib2.Request(url, None, cons.USER_AGENT), form)
			else:
				handler = self.opener.open(urllib2.Request(url, None, cons.USER_AGENT))
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		else:
			return handler

if __name__ == "__main__":
	PROXY = {"http": "proxy.alu.uma.es:3128"}
	o = URLOpen()
	print o.open("http://www.google.es", None).read()
