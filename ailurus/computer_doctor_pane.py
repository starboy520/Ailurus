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
import gtk, gobject, sys, os
from lib import *
from libu import *

class ComputerDoctorPane(gtk.VBox):
    def render_type_func(self, column, cell, model, iter):
        cure_obj = model.get_value(iter, 1)
        pixbuf = [self.icon_must_fix, self.icon_suggestion][cure_obj.type]
        cell.set_property('pixbuf', pixbuf)
    def render_text_func(self, column, cell, model, iter):
        cure_obj = model.get_value(iter, 1)
        text = cure_obj.__doc__
        cell.set_property('text', text)
    def refresh(self):
        self.liststore.clear()
        for obj in self.cure_objs:
            if obj.exists():
                self.liststore.append([False, obj])
    def __init__(self, cure_objs):
        self.cure_objs = cure_objs
        self.icon_must_fix = get_pixbuf(D+'sora_icons/c_must_fix.png', 24, 24)
        self.icon_suggestion = get_pixbuf(D+'sora_icons/c_suggestion.png', 24, 24)
        self.liststore = liststore = gtk.ListStore(bool, gobject.TYPE_PYOBJECT) # apply?, cure_object
        render_toggle = gtk.CellRendererToggle()
        render_type = gtk.CellRendererPixbuf()
        render_text = gtk.CellRendererText()
        column_toggle = gtk.TreeViewColumn()
        column_toggle.pack_start(render_toggle, False)
        column_toggle.add_attribute(render_toggle, 'active', 0)
        column_type = gtk.TreeViewColumn()
        column_type.pack_start(render_type, False)
        column_type.set_cell_data_func(render_type, self.render_type_func)
        column_text = gtk.TreeViewColumn()
        column_text.pack_start(render_text)
        column_text.set_cell_data_func(render_text, self.render_text_func)
        view = gtk.TreeView(liststore)
        view.append_column(column_toggle)
        view.append_column(column_type)
        view.append_column(column_text)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.add(view)
        gtk.VBox.__init__(self, False, 10)
        self.pack_start(scroll)
        self.refresh()