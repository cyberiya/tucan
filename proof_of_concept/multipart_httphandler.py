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

import os
import socket
import sys
import stat
import mimetypes
import mimetools
import httplib
import urllib
import urllib2

CHUNK_SIZE = 4096
CRLF = '\r\n'

#class MultipartHTTPHandler(urllib2.HTTPCookieProcessor):
class MultipartHTTPHandler(urllib2.HTTPHandler):
	"""Based on urllib2_file-0.2 Fabien SEISEN"""
	
	handler_order = urllib2.HTTPHandler.handler_order - 10

	def get_content_type(self, filename):
		""""""
		return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

	def send_data(self, v_vars, v_files, boundary, sock=None):
		"""if sock is None, juste return the estimate size"""
		length = 0
		for key, value in v_vars:
			buffer = []
			buffer.append("--%s" % boundary)
			buffer.append('Content-Disposition: form-data; name="%s"' % key)
			buffer.append("")
			buffer.append("%s" % value)
			buffer = CRLF.join(buffer)
			length += len(buffer)

			if sock:
				sock.send(buffer)
			
		for key, fd in v_files:
			
			file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
			length += file_size

			name = os.path.basename(fd.name)
			
			buffer = []
			buffer.append("--%s" % boundary)
			buffer.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, name))
			buffer.append("Content-Type: %s" % self.get_content_type(name))
			buffer.append("")
			buffer.append("")
			buffer = CRLF.join(buffer)
			length += len(buffer)
			
			if sock:
				sock.send(buffer)
				size = 0
				while True:
					chunk = fd.read(CHUNK_SIZE)
					size += len(chunk)
					print int((float(size)/file_size)*100)
					if not chunk: break
					sock.send(chunk)
				fd.close()

		buffer = []
		buffer.append("")
		buffer.append("--%s--" % boundary)
		buffer.append("")
		buffer = CRLF.join(buffer)
		length += len(buffer)

		if sock:
			sock.send(buffer)

		return length

	def http_open(self, req):
		""""""
		return self.do_open(httplib.HTTPConnection, req)

	def do_open(self, http_class, req):
		""""""
		data = req.get_data()
		v_files=[]
		v_vars=[]
		for key, value in data.items():
			if hasattr(value, 'read'):
				v_files.append((key, value))
			else:
				v_vars.append((key, value))
		host = req.get_host()
		# parse host:port
		h = http_class(host) 
		if req.has_data():
			h.putrequest('POST', req.get_selector())
			if not 'Content-type' in req.headers:
				if len(v_files) > 0:
					boundary = mimetools.choose_boundary()
					length = self.send_data(v_vars, v_files, boundary)
					#h.putheader('Connection', 'keep-alive')
					#h.putheader('Keep-Alive', '300')
					h.putheader('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
					h.putheader('Content-length', str(length))
		else:
			h.putrequest('GET', req.get_selector())
		scheme, sel = urllib.splittype(req.get_selector())
		sel_host, sel_path = urllib.splithost(sel)
		h.putheader('Host', sel_host or host)
		for name, value in self.parent.addheaders:
			name = name.capitalize()
			if name not in req.headers:
				h.putheader(name, value)
		for key, value in req.headers.items():
			h.putheader(key, value)
		# convert a socket error to a URLError.
		try:
			h.endheaders()
		except socket.error, err:
			raise urllib2.URLError(err)

		if req.has_data():
			if len(v_files) > 0:
				l = self.send_data(v_vars, v_files, boundary, h)
		return h.get_response()
#		code, msg, hdrs = h.getreply()
#		fp = h.getfile()
#		if code == 200:
#			resp = urllib.addinfourl(fp, hdrs, req.get_full_url())
#			resp.code = code
#			resp.msg = msg
#			return resp
#		else:
#			return self.parent.error('http', req, fp, code, msg, hdrs)
