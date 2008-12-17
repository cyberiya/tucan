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

import urllib
import urllib2
import cookielib

if __name__ == "__main__":
	urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar())))
	urllib2.urlopen(urllib2.Request("http://www.gigasize.com/get.php/3196987695/p3x03sp.avi"))
	f = open("tmp.jpg", "w")
	f.write(urllib2.urlopen(urllib2.Request("http://www.gigasize.com/randomImage.php")).read())
	f.close()
	captcha = str(raw_input()).strip()
	data = urllib.urlencode({"txtNumber": captcha, "btnLogin.x": "124", "btnLogin.y": "12", "btnLogin": "Download"})
	handle = urllib2.urlopen(urllib2.Request("http://www.gigasize.com/formdownload.php"), data)
	print handle.read()
	handle.close()