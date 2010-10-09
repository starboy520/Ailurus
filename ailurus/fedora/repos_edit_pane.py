#coding: utf8
#
# Ailurus - a simple application installer and GNOME tweaker
#
# Copyright (C) 2009-2010, Ailurus developers and Ailurus contributors
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
import gtk
import sys, os
from lib import *
from libu import *
import gobject, pango

class _sections_store(gtk.ListStore):
    def __init__(self):
        gtk.ListStore.__init__(self, gobject.TYPE_PYOBJECT)
        self.reload()
        
    def reload(self):
        self.repo_objs = FedoraReposFile.all_repo_objs()
        for o in self.repo_objs:
            for s in o.all_section_objs():
                self.append([s])

class _sections_list_box(gtk.VBox):
    def r_enabled_cell_function(self, column, cell, model, iter):
        object = model.get_value(iter, 0)
        if object != None:
            assert isinstance(object, FedoraReposSection)
            cell.set_property('active', object.enabled())

    def r_enabled_toggled(self, render, path):
        path = self.sorted_store.convert_path_to_child_path(path)
        object = self.sections_store[path][0]
        enabled = object.enabled()
        object.set_enabled(not enabled)
    
    def r_name_cell_function(self, column, cell, model, iter):
        object = model.get_value(iter, 0)
        if object != None:
            assert isinstance(object, FedoraReposSection)
            cell.set_property('text', object.name)
    
    def sort_by_enabled(self, model, iter1, iter2):
        obj1 = model.get_value(iter1, 0)
        obj2 = model.get_value(iter2, 0)
        if obj1 and obj2: 
            return -cmp(obj1.enabled(), obj2.enabled()) or cmp(obj1.name, obj2.name)
        else: return 0
    
    def sort_by_name(self, model, iter1, iter2):
        obj1 = model.get_value(iter1, 0)
        obj2 = model.get_value(iter2, 0)
        if obj1 and obj2: return cmp(obj1.name, obj2.name)
        else: return 0
    
    def __init__(self, store):
        self.sections_store = store
        assert isinstance(self.sections_store, _sections_store)
        self.sorted_store = gtk.TreeModelSort(self.sections_store)
        self.sorted_store.set_sort_func(1000, self.sort_by_enabled)
        self.sorted_store.set_sort_func(1001, self.sort_by_name)
        
        r_enabled = gtk.CellRendererToggle()
        r_enabled.connect('toggled', self.r_enabled_toggled)
        r_enabled.set_property('xalign', 0.5)
        c_enabled = gtk.TreeViewColumn()
        c_enabled.set_title(_('Enabled'))
        c_enabled.pack_start(r_enabled)
        c_enabled.set_cell_data_func(r_enabled, self.r_enabled_cell_function)
        c_enabled.set_sort_column_id(1000)
        
        r_name = gtk.CellRendererText()
        r_name.set_property('ellipsize', pango.ELLIPSIZE_END)
        c_name = gtk.TreeViewColumn()
        c_name.set_title(_('Name'))
        c_name.pack_start(r_name)
        c_name.set_cell_data_func(r_name, self.r_name_cell_function)
        c_name.set_sort_column_id(1001)
        
        view = gtk.TreeView(self.sorted_store)
        view.append_column(c_enabled)
        view.append_column(c_name)
        
        scroll = gtk.ScrolledWindow()
        scroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.add(view)
        
        gtk.VBox.__init__(self, False, 0)
        self.pack_start(scroll)

class FedoraReposEditPane(gtk.VBox):
    icon = D+'sora_icons/m_repository_configure.png'
    text = _('Repositories')

    def __init__(self, main_view):
        gtk.VBox.__init__(self, False, 5)
        sections_store = _sections_store()
        sections_list_box = _sections_list_box(sections_store)
        self.pack_start(sections_list_box)