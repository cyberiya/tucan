###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion crak@tucaneando.com
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

import sys
import os
import locale
import subprocess
import logging

#project constants
TUCAN_NAME = "Tucan Manager"
TUCAN_VERSION = "0.3.8 alpha"
TUCAN_REV = ""
try:
	rev = subprocess.Popen("svnversion", stdout=subprocess.PIPE).stdout.read().strip()
except:
	pass
else:
	TUCAN_REV = "r%s" % rev

WEBPAGE = "http://www.tucaneando.com"
DOC = "http://doc.tucaneando.com"

#OS constants
OS_UNIX = False
OS_WINDOWS = False
OS_OSX = False
if sys.platform.startswith("win"):
	OS_WINDOWS = True
elif "darwin" in sys.platform:
	OS_OSX = True
else:
	OS_UNIX = True

#user agent
USER_AGENT = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20081114 Firefox/3.0.4"}

#status constants
STATUS_PEND = "pending"
STATUS_ACTIVE = "active"
STATUS_WAIT = "waiting"
STATUS_STOP = "stoped"
STATUS_CORRECT = "correct"
STATUS_ERROR = "error"

#message constants
SEVERITY_INFO = "info"
SEVERITY_WARNING = "warning"
SEVERITY_ERROR = "error"

#size unit constants
UNIT_KB = "KB"
UNIT_MB = "MB"
UNIT_GB = "GB"

#speed unit constant
UNIT_SPEED = "KB/s"

#time constants
MINUTE = 60
HOUR = 3600

#service type constans
TYPE_ANONYMOUS = "Anonymous"
TYPE_USER = "User"
TYPE_PREMIUM = "Premium"
TYPE_UNSUPPORTED = "unsupported"

#path constants
if OS_WINDOWS:
	PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
	DEFAULT_PATH = os.path.join(os.path.expanduser("~"), "").decode(locale.getdefaultlocale()[1])
	if PATH not in sys.path:
		sys.path.insert(0, PATH)
else:
	if OS_OSX:
		PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
	else:
		PATH = os.path.join(sys.path[0], "")
	DEFAULT_PATH = os.path.join(os.path.expanduser("~"), "")
CONFIG_PATH = os.path.join(DEFAULT_PATH, ".tucan" ,"")

#log constants
LOG_FILE = os.path.join(CONFIG_PATH, "tucan.log")
LOGGER = "Tucan logger"

#plugin constants
PLUGIN_PATH = os.path.join(CONFIG_PATH, "plugins")
DEFAULT_PLUGINS = os.path.join(PATH, "default_plugins", "")

#session constants
SESSION_FILE = os.path.join(CONFIG_PATH, "last.session")

#localization constants
NAME_LOCALES = "tucan"
PATH_LOCALES = os.path.join(PATH, "i18n")

#media constants
PATH_MEDIA = os.path.join(PATH, "media", "")
ICON_TUCAN = PATH_MEDIA + "tucan.svg"
ICON_DOWNLOAD = PATH_MEDIA + "document-save.svg"
ICON_UPLOAD = PATH_MEDIA + "system-software-update.svg"
ICON_CLEAR = PATH_MEDIA + "edit-delete.svg"
ICON_DOWN = PATH_MEDIA + "go-down.svg"
ICON_UP = PATH_MEDIA + "go-up.svg"
ICON_START = PATH_MEDIA + "media-playback-start.svg"
ICON_STOP = PATH_MEDIA + "media-playback-stop.svg"
ICON_CHECK = PATH_MEDIA + "software-update-available.svg"
ICON_PACKAGE = PATH_MEDIA + "package-x-generic.svg"
ICON_PREFERENCES = PATH_MEDIA + "preferences-system.svg"
ICON_PREFERENCES_MAIN = PATH_MEDIA + "preferences-desktop.svg"
ICON_PREFERENCES_SERVICES = PATH_MEDIA + "contact-new.svg"
ICON_PREFERENCES_ADVANCED = PATH_MEDIA + "applications-system.svg"
ICON_LANGUAGE = PATH_MEDIA + "preferences-desktop-locale.svg"
ICON_FOLDER = PATH_MEDIA + "user-home.svg"
ICON_NETWORK = PATH_MEDIA + "network-error.svg"
ICON_ADVANCED = PATH_MEDIA + "application-x-executable.svg"
ICON_MISSING = PATH_MEDIA + "image-missing.svg"
ICON_ACCOUNT = PATH_MEDIA + "system-users.svg"
ICON_UPDATE = PATH_MEDIA + "software-update-urgent.svg"
