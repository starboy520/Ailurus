#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Ailurus - make Linux easier to use
#
# Copyright (C) 2007-2010, Trusted Digital Technology Laboratory, Shanghai Jiao Tong University, China.
# Copyright (C) 2009-2010, Ailurus Developers Team
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
    def __tree_pixbuf(self, column, cell, model, iter):
        pixbuf = model.get_value(iter, 0)
        cell.set_property('pixbuf', pixbuf)
    
    def __tree_text(self, column, cell, model, iter):
        text = model.get_value(iter, 1)
        cell.set_property('text', text)
    
    def __tree_value(self, column, cell, model, iter):
        text = model.get_value(iter, 2)
        cell.set_property('text', text)

    def __init__(self, main_view, COMMON, DESKTOP, DISTRIBUTION, tuples):
        gtk.VBox.__init__(self)
        
        self.treestore = gtk.TreeStore(gtk.gdk.Pixbuf, str, str)
        self.treeview = treeview = gtk.TreeView(self.treestore)
        column = gtk.TreeViewColumn()
        treeview.append_column(column)
        treeview.set_headers_visible(False)
        pixbuf_render = gtk.CellRendererPixbuf()
        text_render = gtk.CellRendererText()
        value_render = gtk.CellRendererText()
        column.pack_start(pixbuf_render, False)
        column.set_cell_data_func(pixbuf_render, self.__tree_pixbuf)
        column.pack_start(text_render, False)
        column.set_cell_data_func(text_render, self.__tree_text)
        column.pack_start(value_render, False)
        column.set_cell_data_func(value_render, self.__tree_value)
        
        scrollwindow = gtk.ScrolledWindow ()
        scrollwindow.add (treeview)
        scrollwindow.set_policy (gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrollwindow.set_shadow_type (gtk.SHADOW_IN)
        
        self.pack_start(scrollwindow)
    
        self.COMMON = COMMON
        self.DESKTOP = DESKTOP
        self.DISTRIBUTION = DISTRIBUTION
        self.tuples = tuples

        self.refresh()
        import gobject
        gobject.timeout_add(5000, self.refresh)
        
    def refresh(self):
        self.treestore.clear()
        for title, icon, function in self.tuples:
            pixbuf = get_pixbuf(icon, 24, 24)
            parent = self.treestore.append(None, [pixbuf, title, None])
            info = function(self.COMMON, self.DESKTOP, self.DISTRIBUTION)
            for row in info:
                pixbuf = get_pixbuf(row[2], 24, 24)
                self.treestore.append(parent, [pixbuf, row[0], row[1]])
        self.treeview.expand_all()
        return True
    
    def register(self, title, icon, load_info, *w):
        pixbuf = get_pixbuf(icon, 24, 24)
        parent = self.treestore.append(None, [pixbuf, title, None])
        self.__refresh_sub(parent, load_info, *w)
        
    def __refresh_sub(self, tree, load_info, *w):
        info = load_info(*w)
        for row in info:
            pixbuf = get_pixbuf(row[2], 24, 24)
            self.treestore.append(tree, [pixbuf, row[0], row[1]])
#        import gobject
#        gobject.timeout_add(5000, self.__refresh_sub, tree, load_info, *w)

#class InfoPane(gtk.VBox):
#    def __init__(self):
#        gtk.VBox.__init__(self)
#        self.left_box = gtk.VBox(False, 5)
#        self.middle_box = gtk.VBox(False, 5)
#        self.right_box = gtk.VBox(False, 5)
#        hbox = gtk.HBox(False, 10)
#        hbox.pack_start(self.left_box, False)
#        hbox.pack_start(self.middle_box, False)
#        hbox.pack_start(self.right_box)
#        hbox_scroll = gtk.ScrolledWindow()
#        hbox_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
#        hbox_scroll.add_with_viewport(hbox)
#        self.pack_start(hbox_scroll)
#    def add_row(self, text, value, icon=D+'umut_icons/i_default.png', tooltip = None):
#        assert isinstance(text, (str,unicode) )
#        assert isinstance(value, (str,unicode) )
#        assert isinstance(icon, str)
#        assert tooltip==None or isinstance(tooltip, (str,unicode) )
#
#        pixbuf = get_pixbuf(icon, 24, 24)
#        image = gtk.Image()
#        image.set_from_pixbuf(pixbuf)
#        if tooltip: image.set_tooltip_text(tooltip)
#        self.left_box.pack_start(image)
#        
#        label = gtk.Label(text)
#        if tooltip: label.set_tooltip_text(tooltip)
#        self.middle_box.pack_start( left_align(label) )
#        
#        label2 = gtk.Label(value)
#        label2.set_selectable(True)
#        if tooltip: label2.set_tooltip_text(tooltip)
#        self.right_box.pack_start( left_align(label2))
#        
#class InfoPane2(gtk.VBox):
#    def __init__(self):
#        gtk.VBox.__init__(self)
#        self.table = table = gtk.Table()
#        self.table_pos = 0
#        table.set_col_spacings(10)
#        table.set_border_width(10)
#        scroll = gtk.ScrolledWindow()
#        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
#        scroll.add_with_viewport(table)
#        self.pack_start(scroll)
#    def add_row(self, text, value, icon=D+'umut_icons/i_default.png', tooltip = None):
#        assert isinstance(text, (str,unicode) )
#        assert isinstance(value, (str,unicode) )
#        assert isinstance(icon, str)
#        assert tooltip==None or isinstance(tooltip, (str,unicode) )
#        
#        pos = self.table_pos
#        pixbuf = get_pixbuf(icon, 32, 32)
#        image = gtk.Image()
#        image.set_from_pixbuf(pixbuf)
#        if tooltip: image.set_tooltip_text(tooltip)
#        self.table.attach(image, 0, 1, pos, pos+1, gtk.FILL, gtk.FILL)
#        label = gtk.Label(text)
#        if tooltip: label.set_tooltip_text(tooltip)
#        align = gtk.Alignment(0,0.5)
#        align.add(label)
#        self.table.attach(align, 1, 2, pos, pos+1, gtk.FILL, gtk.FILL)
#        label2 = gtk.Entry()
#        gray_bg(label2)
#        if tooltip: label2.set_tooltip_text(tooltip)
#        label2.set_text(value)
#        label2.set_editable(False)
#        self.table.attach(label2, 2, 3, pos, pos+1, gtk.FILL|gtk.EXPAND, gtk.FILL)
#        self.table_pos += 1
#
#class HardwareInfoPane(InfoPane):
#    name = _('Hardware Information')
#    def __init__(self, main_view, rows):
#        InfoPane.__init__(self)
#        for row in rows:
#            assert isinstance(row, tuple)
#            assert len(row)==4
#            self.add_row(*row)
#
#class LinuxInfoPane(InfoPane):
#    name = _('Linux Information')
#    def __init__(self, main_view, rows):
#        InfoPane.__init__(self)
#        for row in rows:
#            assert isinstance(row, tuple)
#            assert len(row)==4
#            self.add_row(*row)
