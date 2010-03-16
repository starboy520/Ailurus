#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Ailurus - make Linux easier to use
#
# Copyright (C) 2007-2010, Trusted Digital Technology Laboratory, Shanghai Jiao Tong University, China.
#
# Ailurus is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ailurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ailurus; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

import gtk

class SplashWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self, gtk.WINDOW_POPUP)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_default_size(400, -1)
        self.set_border_width(15)
        color = gtk.gdk.color_parse('#202020')
        self.modify_bg(gtk.STATE_NORMAL, color)
        
        logo = gtk.Image()
        logo.set_from_file(D+'suyun_icons/splash.png')
        
        from lib import AILURUS_VERSION
        title = gtk.Label()
        title.set_markup('<span color="green" size="xx-large">Ailurus</span> '
                         '<span color="green" size="x-large">%s</span>' % AILURUS_VERSION)
        
        comment = gtk.Label()
        comment.set_markup(
            _('<span color="yellow">'
              'Help you install some nice applications.\n'
              'Help you do tedious settings.\n'
              'Tell you some Linux skills.'
              '</span>') )
        import pango
        comment.modify_font(pango.FontDescription('Sans 14'))
        
        titlevbox = gtk.VBox(False, 0)
        titlevbox.pack_start(title, False)
        titlevbox.pack_start(comment, False)

        header_box = gtk.HBox(False, 20)
        header_box.pack_start(logo, False)
        header_box.pack_start(titlevbox, True)
        
        loading = self.loading = gtk.Label()
        import StringIO
        self.buffer = StringIO.StringIO() 
        
        align = gtk.Alignment(0, 0)
        align.add(loading)

        self.progressbar = progressbar = gtk.ProgressBar()
        progressbar.set_pulse_step(0.1)
        
        box = gtk.VBox(False, 5)
        box.pack_start(header_box, True, True, 0)
        box.pack_start(align, False)
        box.pack_start(progressbar, False)
        
        self.add(box)

    def add_text(self, text):
        #append string
        self.buffer.write(text)
        #get content
        string = self.buffer.getvalue()
        #display last line
        list = string.split('\n')
        if list[-1]=='': del list[-1]
        self.loading.set_markup(list[-1])
        #change progressbar
        self.progressbar.set_fraction( min(1, 0.1*len(list) ) )
        #refresh
        while gtk.events_pending(): gtk.main_iteration()

from lib import *
if __name__ == '__main__':
    win = SplashWindow()
    win.show_all()
    import time
    win.add_text('<span color="yellow">Hello1</span>\n')
    time.sleep(2)
    win.add_text('<span color="yellow">Hello2</span>\n')
    time.sleep(2)
    gtk.main()