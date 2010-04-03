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

from __future__ import with_statement
import gtk, traceback, sys, os
from lib import *
from libu import *

class InfoPane(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        self.left_box = gtk.VBox(False, 5)
        self.middle_box = gtk.VBox(False, 5)
        self.right_box = gtk.VBox(False, 5)
        hbox = gtk.HBox(False, 10)
        hbox.pack_start(self.left_box, False)
        hbox.pack_start(self.middle_box, False)
        hbox.pack_start(self.right_box)
        hbox_scroll = gtk.ScrolledWindow()
        hbox_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        hbox_scroll.add_with_viewport(hbox)
        self.pack_start(hbox_scroll)
    def add_row(self, text, value, icon=D+'umut_icons/i_default.png', tooltip = None):
        assert isinstance(text, (str,unicode) )
        assert isinstance(value, (str,unicode) )
        assert isinstance(icon, str)
        assert tooltip==None or isinstance(tooltip, (str,unicode) )

        pixbuf = get_pixbuf(icon, 24, 24)
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        if tooltip: image.set_tooltip_text(tooltip)
        self.left_box.pack_start(image)
        
        label = gtk.Label(text)
        if tooltip: label.set_tooltip_text(tooltip)
        self.middle_box.pack_start( left_align(label) )
        
        label2 = gtk.Label(value)
        label2.set_selectable(True)
        if tooltip: label2.set_tooltip_text(tooltip)
        self.right_box.pack_start( left_align(label2))
        
class InfoPane2(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        self.table = table = gtk.Table()
        self.table_pos = 0
        table.set_col_spacings(10)
        table.set_border_width(10)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.add_with_viewport(table)
        self.pack_start(scroll)
    def add_row(self, text, value, icon=D+'umut_icons/i_default.png', tooltip = None):
        assert isinstance(text, (str,unicode) )
        assert isinstance(value, (str,unicode) )
        assert isinstance(icon, str)
        assert tooltip==None or isinstance(tooltip, (str,unicode) )
        
        pos = self.table_pos
        pixbuf = get_pixbuf(icon, 32, 32)
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        if tooltip: image.set_tooltip_text(tooltip)
        self.table.attach(image, 0, 1, pos, pos+1, gtk.FILL, gtk.FILL)
        label = gtk.Label(text)
        if tooltip: label.set_tooltip_text(tooltip)
        align = gtk.Alignment(0,0.5)
        align.add(label)
        self.table.attach(align, 1, 2, pos, pos+1, gtk.FILL, gtk.FILL)
        label2 = gtk.Entry()
        gray_bg(label2)
        if tooltip: label2.set_tooltip_text(tooltip)
        label2.set_text(value)
        label2.set_editable(False)
        self.table.attach(label2, 2, 3, pos, pos+1, gtk.FILL|gtk.EXPAND, gtk.FILL)
        self.table_pos += 1

class HardwareInfoPane(InfoPane):
    name = _('Hardware Information')
    def __init__(self, main_view, rows):
        InfoPane.__init__(self)
        for row in rows:
            assert isinstance(row, tuple)
            assert len(row)==4
            self.add_row(*row)

class LinuxInfoPane(InfoPane):
    name = _('Linux Information')
    def __init__(self, main_view, rows):
        InfoPane.__init__(self)
        for row in rows:
            assert isinstance(row, tuple)
            assert len(row)==4
            self.add_row(*row)
