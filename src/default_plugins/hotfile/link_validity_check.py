import logging
from core.url_open import URLOpen
logger = logging.getLogger(__name__)

def link_validity_check(url):
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
		size   = int(link_name_size_status_list[1]) / 1024
		status = int(link_name_size_status_list[2])
		unit = "KB"
	except Exception, e:
		logger.exception("%s :%s" % (url, e))
		
	if status != 1:
		""" print ("Link is down! {0} {1}|".format(type(status), status)) """
		return None, -1, None
	else:
		return name, size, unit
