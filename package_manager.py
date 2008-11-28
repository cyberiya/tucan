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

import re

import cons

LINKS = {'megaupload.com': [('http://www.megaupload.com/?d=N06UYST6', 'D.S03E02.0TV.cHoPPaHoLiK.part1.rar', 96, 'MB', 'AnonymousMegaupload'), ('http://www.megaupload.com/?d=HE4TMQPQ', 'D.S03E02.0TV.cHoPPaHoLiK.part2.rar', 96, 'MB', 'AnonymousMegaupload'), ('http://www.megaupload.com/?d=3TSDC4J3', 'D.S03E02.0TV.cHoPPaHoLiK.part3.rar', 96, 'MB', 'AnonymousMegaupload'), ('http://www.megaupload.com/?d=BP5RK0TM', 'D.S03E02.0TV.cHoPPaHoLiK.part4.rar', 96, 'MB', 'AnonymousMegaupload'), ('http://www.megaupload.com/?d=2XF7ELQ9', 'D.S03E02.0TV.cHoPPaHoLiK.part5.rar', 96, 'MB', 'AnonymousMegaupload'), ('http://www.megaupload.com/?d=15YBBMCG', 'D.S03E02.0TV.cHoPPaHoLiK.part6.rar', 68, 'MB', 'AnonymousMegaupload')], 'rapidshare.com': [('http://rapidshare.com/files/151319465/D.S03E02.0TV.cHoPPaHoLiK.part1.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part1.rar', 98, 'MB', 'PremiumRapidshare'), ('http://rapidshare.com/files/151319467/D.S03E02.0TV.cHoPPaHoLiK.part2.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part2.rar', 98, 'MB', 'PremiumRapidshare'), ('http://rapidshare.com/files/151319554/D.S03E02.0TV.cHoPPaHoLiK.part3.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part3.rar', 98, 'MB', 'PremiumRapidshare'), ('http://rapidshare.com/files/151319448/D.S03E02.0TV.cHoPPaHoLiK.part4.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part4.rar', 98, 'MB', 'PremiumRapidshare'), ('http://rapidshare.com/files/151319452/D.S03E02.0TV.cHoPPaHoLiK.part5.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part5.rar', 98, 'MB', 'PremiumRapidshare'), ('http://rapidshare.com/files/151319357/D.S03E02.0TV.cHoPPaHoLiK.part6.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part6.rar', 69, 'MB', 'PremiumRapidshare')]}
FILES = ['D.S02E02.0TV.cHoPPaHoLiK.part1.rar', 'Los Episodios Nacionales 01-10 parte2.zip', 'D.S03E02.0TV.cHoPPaHoLiK.part3.rar', 'Los Episodios Nacionales 01-11 parte2.zip', 'Los Episodios Nacionales 01-10 parte1.zip', 'D.S02E02.0TV.cHoPPaHoLiK.part2.rar',  'D.S03E02.0TV.cHoPPaHoLiK.part4.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part5.rar', 'D.S03E02.0TV.cHoPPaHoLiK.part6.rar']

class PackageManager:
	""""""
	def __init__(self):
		""""""
		pass
	
	def get_packages(self, files):
		""""""
		packages = {}
		while len(files) > 0:
			tmp_name = []
			first = files[0]
			others = files[1:]
			for file_name in others:
				chars = re.split("[0-9]+", file_name)
				nums = re.split("[^0-9]+", file_name)
				tmp = ""
				for i in chars:
					if tmp+i == first[0:len(tmp+i)]:
						tmp += i
						for j in nums:
							if tmp+j == first[0:len(tmp+j)]:
								tmp += j
				tmp_name.append(tmp)
			final_name = ""
			for name in tmp_name:
				if len(name) > len(final_name):
					final_name = name
			if len(final_name) > 0:
				packages[final_name] = [first]
				del files[files.index(first)]
				tmp_list = []
				for name in files:
					if final_name in name:
						tmp_list.append(name)
				packages[final_name] += tmp_list
				for i in tmp_list:
					del files[files.index(i)]
			else:
				alone_name = first
				alone_name = alone_name.split(".")
				alone_name.pop()
				alone_name = ".".join(alone_name)
				packages[alone_name] = [first]
				del files[files.index(first)]
		return packages

	def sort_files(self, dict):
		""""""
		files = []
		for service, links in dict.items():
			for link in links:
				if not link[1] in files:
					files.append(link[1])
		files.sort()
		return files

if __name__ == "__main__":
	l = PackageManager()
	print l.get_packages(list(FILES))
