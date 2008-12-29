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

import os
import Image
import ImageFile
import ImageOps

IMAGE_PATH = "tmp.tif"
TEXT_PATH = "tmp.txt"

class Tesseract:
	""""""
	def __init__(self, data, filter=None):
		""""""
		p = ImageFile.Parser()
		p.feed(data)
		image = p.close()
		image = image.resize((180,60), Image.BICUBIC)
		if filter:
			image = image.point(self.filter_pixel)
		image = ImageOps.grayscale(image)
		image.save(IMAGE_PATH)
	
	def get_captcha(self, num_chars):
		""""""
		if os.system("tesseract "+ IMAGE_PATH + " tmp") == 0:
			f = file(TEXT_PATH, "r")
			captcha = f.readline().strip()
			if len(captcha) == num_chars:
				return captcha
				
	def filter_pixel(self, pixel):
		""""""
		if pixel > 50:
			return 255
		else:
			return 1

if __name__ == "__main__":
	f = file("tmp.jpg", "r")
	t = Tesseract(f.read())
	print t.get_captcha(3)