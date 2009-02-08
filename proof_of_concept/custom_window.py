import math

import pygtk
pygtk.require('2.0')
import gtk

FEATHER = ["255 82 2 1",
" 	c None",
".	c #FFFFFF",
"                                                                                                                               ...................                                                                                                             ",
"                                                                                                                               ...................                                                                                                             ",
"                                                                                                                              ....................                                                                                                             ",
"                                                                   ..........................                  .....................................................                                                                                           ",
"                                                                  ............................                .......................................................                                                                                          ",
"                                                                  ............................                ........................................................                                                                                         ",
"                                             ................................................................................................................................                                                                                  ",
"                                            .................................................................................................................................                                                                                  ",
"                                            ..................................................................................................................................                                                                                 ",
"                                  ...................................................................................................................................................    .......                                                               ",
"                                 .....................................................................................................................................................  .........                                                              ",
"                                .................................................................................................................................................................. .....                                                       ",
"                               ..........................................................................................................................................................................                                                      ",
"                              ...........................................................................................................................................................................                                                      ",
"               .       ......................................................................................................................................................................................                                                  ",
"              ...     ........................................................................................................................................................................................                                                 ",
"              ....    .........................................................................................................................................................................................                                                ",
"         .......................................................................................................................................................................................................       ....                                    ",
"         ........................................................................................................................................................................................................     ......                                   ",
"        ..........................................................................................................................................................................................................   ........                                  ",
"      ...........................................................................................................................................................................................................................                              ",
"      ............................................................................................................................................................................................................................                             ",
"    ...............................................................................................................................................................................................................................                            ",
"   .................................................................................................................................................................................................................................                           ",
"   ..................................................................................................................................................................................................................................                          ",
"......................................................................................................................................................................................................................................                         ",
".......................................................................................................................................................................................................................................                        ",
"........................................................................................................................................................................................................................................                       ",
"   ............................................................................................................................................................................................................................................................",
"   ............................................................................................................................................................................................................................................................",
"   ............................................................................................................................................................................................................................................................",
"   ............................................................................................................................................................................................................................................................",
"   ............................................................................................................................................................................................................................................................",
"   ............................................................................................................................................................................................................................................................",
"   ............................................................................................................................................................................................................................................................",
"    ...........................................................................................................................................................................................................................................................",
"     ..........................................................................................................................................................................................................................................................",
"      .........................................................................................................................................................................................................................................................",
"       ........................................................................................................................................................................................................................................................",
"        .......................................................................................................................................................................................................................................................",
"         ......................................................................................................................................................................................................................................................",
"          .. ............................................................................................................................................................................................................................................  ....",
"              .........................................................................................................................................................................................................................................        ",
"              .........................................................................................................................................................................................................................................        ",
"              ..........................................................................................................................................................................................................................                       ",
"              .........................................................................................................................................................................................................................                        ",
"               .......................................................................................................................................................................................................................                         ",
"                .....................................................................................................................................................................................................................                          ",
"                 ...................................................................................................................................................................................................................                           ",
"                 ..................................................................................................................................................................................................................                            ",
"                 .................................................................................................................................................................................................................                             ",
"                 ................................................................................................................................................................................................................                              ",
"                  ...............................................................................................................................................................................................................                              ",
"                    .............................................................................................................................................................................................................                              ",
"                    .............................................................................................................................................................................................................                              ",
"                      .........................................................................................................................................................................................................                                ",
"                      .........................................................................................................................................................................................................                                ",
"                       ........................................................................................................................................................................................................                                ",
"                         ......................................................................................................................................................................................................                                ",
"                         ......................................................................................................................................................................................................                                ",
"                          ....................................................................................................................................................................................................                                 ",
"                                    .....................................................................................................................................................................................                                      ",
"                                    .....................................................................................................................................................................................                                      ",
"                                      ...................................................................................................................................................................................                                      ",
"                                       ..................................................................................................................................................................................                                      ",
"                                       ..................................................................................................................................................................................                                      ",
"                                            ...........................................................................................................................................................................                                        ",
"                                            ..........................................................................................................................................................................                                         ",
"                                             .........................................................................................................................................................................                                         ",
"                                                                  ...............................................................................................................................................                                              ",
"                                                                  ...............................................................................................................................................                                              ",
"                                                                   ............................. ...............................................................................................................                                               ",
"                                                                                                   .........................................................................................................                                                   ",
"                                                                                                   ........................................................................................................                                                    ",
"                                                                                                                ...............  ......................................................................                                                        ",
"                                                                                                                 ..............  .....................................................................                                                         ",
"                                                                                                                 .............    ...................................................................                                                          ",
"                                                                                                                 .........       ............................  ............................                                                                    ",
"                                                                                                                 ........        ............................   ...........................                                                                    ",
"                                                                                                                  ......          ..........................    ..........................                                                                     ",
"                                                                                                                                                                     ......                                                                                    ",
"                                                                                                                                                                     .....                                                                                     "]

class FeatherWindow(gtk.Window):
	def __init__(self, parent):
		gtk.Window.__init__(self, gtk.WINDOW_POPUP)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_transient_for(parent)

		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#4b78b9"))
		vbox = gtk.VBox()
		self.add(vbox)
		vbox.pack_start(gtk.Label(""), False)
		vbox.pack_start(gtk.Label("AnonymousRapidshare"), False)
		vbox.pack_start(gtk.Label("[21:02]"), False)
		self.connect('size-allocate', self._on_size_allocate)

	def _on_size_allocate(self, window, allocation):
		pixmap, bitmap = gtk.gdk.pixmap_create_from_xpm_d(self.get_root_window(), None, FEATHER)
		width, height = pixmap.get_size()
		self.set_size_request(width, height)
		window.shape_combine_mask(bitmap, 0, 0)

	def show_feather(self, widget, event):
		""""""
		feather_width, feather_height = self.size_request()
		win_x, win_y = widget.parent.get_parent_window().get_position()
		rect = widget.get_allocation()
		self.move(win_x + rect.x - feather_width, win_y + rect.y - 20)
		self.show_all()
		
	def hide_feather(self, widget, event):
		""""""
		self.hide()

if __name__ == "__main__":
	w = FeatherWindow(None)
	gtk.main()