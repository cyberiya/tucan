###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
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
import urllib2
import cookielib
import time
import random

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

HEADER = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20081114 Firefox/3.0.4", "Referer" : "http://rapidshare.com/", "Origin" : "http://rapidshare.com/"}

class UploadParser():
	""""""
	def __init__(self, file_name, description):
		""""""
		up_done_action = None
		file_id = None
		url = None

		opener = register_openers()
		cookie = cookielib.CookieJar()
		opener.add_handler(urllib2.HTTPCookieProcessor(cookie))

		result = opener.open(urllib2.Request("http://api.rapidshare.com/cgi-bin/rsapi.cgi?sub=nextuploadserver_v1&cbf=RSAPIDispatcher&cbid=1",None,HEADER))
#		print result.readlines()[0]
		server = result.readlines()[0].split('"')[1].split('"')[0]
		print server
		uploadid = str(int(time.time()))[-5:] + str(int(round(random.random()*1000000)))
#		action = "http://rs%sl3.rapidshare.com/cgi-bin/uploadprogress.cgi?uploadid=%s&r=%s&cbf=RSAPIDispatcher&cbid=2" % (server,uploadid,str(int(time.time()))[-5:])
#		
#		print action
#		
#		result = opener.open(urllib2.Request(action,None, HEADER))
#		print result.readlines()
		
		up_done_action = "http://rs%sl3.rapidshare.com/cgi-bin/upload.cgi?rsuploadid=%s" % (server,uploadid)
		form = {"rsapi_v1" : "1", "realfolder" : "0" , "filecontent": open(file_name, "rb")}
		print up_done_action
		print form
		datagen, headers = multipart_encode(form,None,self.progress)
		headers = dict(headers.items() + HEADER.items())
		print headers
		result = opener.open(urllib2.Request(up_done_action, datagen, headers))
		
#		print result.readlines()
		for line in result:
			if 'File1.1=' in line:
				url = line.split('File1.1=')[1].split("\\")[0]
				print url
		
#		action = "http://rs%sl3.rapidshare.com/cgi-bin/uploadprogress.cgi?uploadid=%s&r=%s&cbf=RSAPIDispatcher&cbid=3" % (server,uploadid,str(int(time.time()))[-5:])
#		
#		result = opener.open(urllib2.Request(action,None, HEADER))
#		print result.readlines()
#		action = "http://rs%sl3.rapidshare.com/cgi-bin/uploadprogress.cgi?uploadid=%s&r=%s&cbf=RSAPIDispatcher&cbid=4" % (server,uploadid,str(int(time.time()))[-5:])
#		
#		result = opener.open(urllib2.Request(action,None, HEADER))
#		print result.readlines()
		
#		for line in result:
#			if 'name="url"' in line:
#				url = line.split('value="')[1].split('"')[0]
#				print url
				
	def progress(self,se,current,total):
		print "%d : %d" % (current,total)

if __name__ == "__main__":
	c = UploadParser("/home/elie/upload.png", "mierda")
