###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion Crakotaku(at)yahoo.es
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

import sys
import os
import tempfile

import ImageFile
import Image
import TiffImagePlugin

import cons

IMAGE_SUFFIX = ".tif"
TEXT_SUFFIX = ".txt"

class Tesseract:
	""""""
	def __init__(self, data, filter=None):
		""""""
		if "win" in sys.platform:
			if PATH not in sys.path:
				sys.path.insert(0, cons.PATH)
			self.image_name = os.path.join(cons.CONFIG_PATH, "tmp.tif")
			self.text_name = os.path.join(cons.CONFIG_PATH, "tmp")
			self.tesseract = os.path.join(cons.PATH, "tesseract", "tesseract.exe")
		else:
			self.text = tempfile.NamedTemporaryFile(suffix=TEXT_SUFFIX)
			self.image = tempfile.NamedTemporaryFile(suffix=IMAGE_SUFFIX)
			self.image_name = self.image.name
			self.text_name = self.text.name.rsplit(TEXT_SUFFIX, 1)[0]
			self.tesseract = "tesseract"
		p = ImageFile.Parser()
		p.feed(data)
		if filter:
			image = filter(p.close())
		else:
			image = p.close()
		image.save(self.image_name)
	
	def get_captcha(self):
		""""""
		captcha = ""
		if "win" in sys.platform:
			if os.system(self.tesseract + " " + self.image_name + " " + self.text_name) == 0:
				f = file(self.text_name + TEXT_SUFFIX, "r")
				captcha = f.readline().strip()
				f.close()
		else:
			if os.system(self.tesseract + " " + self.image_name + " " + self.text_name) == 0:
				captcha = self.text.file.readline().strip()
			self.text.file.close()
			self.image.file.close()
		return captcha

if __name__ == "__main__":
	f = file("tmp.png", "r")
	t = Tesseract(f.read())
	print t.get_captcha()