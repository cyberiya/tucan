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

[('method', 'post'), ('action', '/formdownload.php'), ('target', '_top')]
[('name', 'txtNumber'), ('type', 'text'), ('id', 'txtNumber'), ('value', ''), ('maxlength', '3'), ('size', '5'), ('class', 'inpcode')]
[('name', 'btnLogin'), ('type', 'image'), ('id', 'btnLogin'), ('src', '/images/premium-banners//download_button.png'), ('value', 'Download')]




if __name__ == "__main__":
	f = open("tmp.jpg", "w")
	f.write(urllib2.urlopen(urllib2.Request("http://www.gigasize.com/randomImage.php")).read())
	f.close()
	print urllib2.urlopen(urllib2.Request("http://www.gigasize.com/get.php/3196987695/p3x03sp.avi")).read()