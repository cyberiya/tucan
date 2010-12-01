###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
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

import os.path
import logging
logger = logging.getLogger(__name__)

import pygtk
pygtk.require('2.0')
import gtk

from core.cons import PATH

try:
	EXT = ".svg"
	PATH_MEDIA = os.path.join(PATH, "media", "scalable")
	gtk.gdk.pixbuf_new_from_file("%s/tucan%s" % (PATH_MEDIA, EXT))
except Exception, e:
	EXT = ".png"
	PATH_MEDIA = os.path.join(PATH, "media")
	logger.warning("Using PNG icons: %s" % e)

ICON_TUCAN = "%s/tucan%s" % (PATH_MEDIA, EXT)
ICON_DOWNLOAD = "%s/document-save%s" % (PATH_MEDIA, EXT)
ICON_UPLOAD = "%s/system-software-update%s" % (PATH_MEDIA, EXT)
ICON_CLEAR = "%s/edit-delete%s" % (PATH_MEDIA, EXT)
ICON_DOWN = "%s/go-down%s" % (PATH_MEDIA, EXT)
ICON_UP = "%s/go-up%s" % (PATH_MEDIA, EXT)
ICON_START = "%s/media-playback-start%s" % (PATH_MEDIA, EXT)
ICON_STOP = "%s/media-playback-stop%s" % (PATH_MEDIA, EXT)
ICON_CHECK = "%s/software-update-available%s" % (PATH_MEDIA, EXT)
ICON_PACKAGE = "%s/package-x-generic%s" % (PATH_MEDIA, EXT)
ICON_PREFERENCES = "%s/preferences-system%s" % (PATH_MEDIA, EXT)
ICON_PREFERENCES_MAIN = "%s/preferences-desktop%s" % (PATH_MEDIA, EXT)
ICON_PREFERENCES_SERVICES = "%s/contact-new%s" % (PATH_MEDIA, EXT)
ICON_PREFERENCES_ADVANCED = "%s/applications-system%s" % (PATH_MEDIA, EXT)
ICON_LANGUAGE = "%s/preferences-desktop-locale%s" % (PATH_MEDIA, EXT)
ICON_FOLDER = "%s/user-home%s" % (PATH_MEDIA, EXT)
ICON_NETWORK = "%s/network-error%s" % (PATH_MEDIA, EXT)
ICON_ADVANCED = "%s/application-x-executable%s" % (PATH_MEDIA, EXT)
ICON_MISSING = "%s/image-missing%s" % (PATH_MEDIA, EXT)
ICON_ACCOUNT = "%s/system-users%s" % (PATH_MEDIA, EXT)
ICON_UPDATE = "%s/software-update-urgent%s" % (PATH_MEDIA, EXT)
ICON_SEND = "%s/mail-reply-sender%s" % (PATH_MEDIA, EXT)
