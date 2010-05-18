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

    def print_all_information(self):
        import StringIO
        f = StringIO.StringIO()
        
        root = self.treestore.get_iter_first()
        while root:
            value1 = self.treestore.get_value(root, 1)
            print >>f, value1
            
            child = self.treestore.iter_children(root)
            while child:
                value1 = self.treestore.get_value(child, 1)
                value2 = self.treestore.get_value(child, 2)
                print >>f, '\t', value1
                print >>f, '\t\t', value2
                child = self.treestore.iter_next(child)
                
            root = self.treestore.iter_next(root)

        show_text_window(_('Information'), f.getvalue())

    def __init__(self, main_view, tuples):
        gtk.VBox.__init__(self, False, 10)
        
        button = image_stock_button(gtk.STOCK_PRINT, _('Print all information'))
        button.connect('clicked', lambda w: self.print_all_information())
        align_button = gtk.Alignment(0, 0.5)
        align_button.add(button)
        
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
        self.pack_start(align_button, False)
        
        self.tuples = tuples
        self.function2trees = {}
        
        for title, icon, functions in self.tuples:
            pixbuf = get_pixbuf(icon, 24, 24)
            parent = self.treestore.append(None, [pixbuf, title, None])
            self.__build_subtree(parent, functions)

        self.treeview.expand_all()

        import gobject
        gobject.timeout_add(5000, self.refresh)
    
    def __build_subtree(self, tree, functions):
        for function in functions:
            rows = function()
            trees = self.function2trees[function] = []
            for row in rows:
                pixbuf = get_pixbuf(row[2], 24, 24)
                t = self.treestore.append(tree, [pixbuf, row[0], row[1]])
                trees.append(t)
        
    def refresh(self):
        for function in self.function2trees.keys():
            if hasattr(function, 'please_refresh_me'):
                rows = function()
                index = 0
                for tree in self.function2trees[function]:
                    row = rows[index]
                    self.treestore.set_value(tree, 2, row[1])
                    index += 1
        return True
