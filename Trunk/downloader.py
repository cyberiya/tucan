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

import threading
import time

class Downloader(threading.Thread):
	"""Clase Downloader, hereda de threading.Thread
           --------------------------------------------
           * init :: inicializa la clase con los argumentos por defecto
           * run :: metodo run de la clase Downloader, detiene la ejecucion 
                    durante 'time' segundos, pasado ese tiempo se reanuda la 
                    ejecucion y el stop_flag se pone a  """
	def __init__(self, url, end, time=None, cookie=None):
		""" Inicia la funcion """
		threading.Thread.__init__(self)
		self.url = url
		self.end = end
		self.wait = time
		self.stop_flag = False
		self.status = "stoped"
		
	def run(self):
		""""""
		if self.wait:
			self.status = "waiting"
			time.sleep(self.wait)
		self.status = 0
		while not self.stop_flag:
			self.status += 1
		self.status = "stoped"
		self.end(self.url)

if __name__ == "__main__":
    d = Downloader()
