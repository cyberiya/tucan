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
import logging
logger = logging.getLogger(__name__)

from core.download_plugin import DownloadPlugin
from core.recaptcha import Recaptcha
from core.url_open import URLOpen

BASE_URL = "http://hotfile.com"

def check_links(url):
	""""""
	if url is None:
		return None

	name   = None
	size   = -1
	unit   = None
	status = -1

	
	"""
	Split the string by '/':
	Hotfile urls are always of this form:
		http://hotfile.com/dl/ID/KEY/filename.html
	Thus we should get the (0 based) 4th & 5th entry in the returned list
	"""
	split_str = url.split('/')
	if len(split_str) is not 7:
		return None

	link_id  = split_str[4]
	link_key = split_str[5]
	del split_str
	check_link_url = ("http://api.hotfile.com/?action=checklinks&ids=" + link_id + 
					  "&keys=" + link_key + "&fields=name,size,status")
	""" print ("Check link url: {0}".format(check_link_url))  """

	try: 
		link_name_size_status = URLOpen().open(check_link_url).readline()
		link_name_size_status_list = link_name_size_status.split(',')
		name   = link_name_size_status_list[0]
		size   = int(link_name_size_status_list[1])
		status = int(link_name_size_status_list[2])
		unit = "B"
	except Exception, e:
		logger.exception("%s :%s" % (url, e))
		
	if status != 1:
		""" print ("Link is down! {0} {1}|".format(type(status), status)) """
		return None, -1, None
	else:
		return name, size, unit

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, content_range=None):
		""""""
		link = None
		retry = 3
		try:
			if "?" in url:
				url = url.split("?")[0]
			tmp_link, tmp_form, wait = self.parse_wait(url)
			if not tmp_link or not tmp_form:
				return self.set_limit_exceeded()
			elif not wait_func(wait):
				return
			else:
				opener = URLOpen(cookielib.CookieJar())
				it = opener.open(tmp_link, tmp_form)
				for line in it:
					if "function starthtimer(){" in line:
						it.next()
						try:
							tmp = int(it.next().split("+")[1].split(";")[0])
							return self.set_limit_exceeded(int(tmp/1000))
						except Exception, e:
							logger.exception("%s: %s" % (url, e))
							return
					elif "click_download" in line:
						link = line.split('href="')[1].split('"')[0]
						break
					elif "http://api.recaptcha.net/challenge" in line:
						recaptcha_link = line.split('src="')[1].split('"')[0]
						if not wait_func():
							return
						c = Recaptcha(BASE_URL, recaptcha_link)
						while not link and retry:
							challenge, response = c.solve_captcha()
							if response:
								if not wait_func():
									return
								form = urllib.urlencode([("action", "checkcaptcha"), ("recaptcha_challenge_field", challenge), ("recaptcha_response_field", response)])
								for line in opener.open(tmp_link, form):
									if "click_download" in line:
										link = line.split('href="')[1].split('"')[0]
										break
							retry -= 1
						break
				if link:
					return opener.open(link, None, content_range, True)
				else:
					#Hotfile bug
					return self.set_limit_exceeded()
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def parse_wait(self, url):
		""""""
		link = None
		form = None
		wait = 0
		found = False
		try:
			tmp_form = []
			opener = URLOpen()
			for line in opener.open(url):
				if "download_file" in line:
					found = True
				elif found:
					if "method=post " in line:
						link = "%s%s" % (BASE_URL, line.split('action="')[1].split('" ')[0])
					elif "name=action " in line:
						tmp_form.append(("action", line.split("value=")[1].split(">")[0]))
					elif "name=tm " in line:
						tmp_form.append(("tm", line.split("value=")[1].split(">")[0]))
					elif "name=tmhash " in line:
						tmp_form.append(("tmhash", line.split("value=")[1].split(">")[0]))
					elif "name=wait " in line:
						wait = int(line.split("value=")[1].split(">")[0])
						tmp_form.append(("wait", wait))
					elif "name=waithash " in line:
						tmp_form.append(("waithash", line.split("value=")[1].split(">")[0]))
					elif "name=upidhash " in line:
						tmp_form.append(("upidhash", line.split("value=")[1].split(">")[0]))
						found = False
			form = urllib.urlencode(tmp_form)
		except Exception, e:
			logger.exception("%s: %s" % (url, e))
		return link, form, wait

	def check_links(self, url):
		return check_links(url)

