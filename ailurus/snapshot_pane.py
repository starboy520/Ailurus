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
import gtk, gobject
import sys, os
from lib import *
from libu import *

class _snapshot_store(gtk.ListStore):
    def __init__(self):
        gtk.ListStore.__init__(self, gobject.TYPE_PYOBJECT) # date & comment
        self.set_sort_func(1000, self.sort_by_time)
        self.reload()
    
    def reload(self):
        self.clear()
        ss = Snapshot.all_snapshots()
        for s in ss:
            self.append([s])

    def sort_by_time(self, model, iter1, iter2):
        s1 = model.get_value(iter1, 0)
        s2 = model.get_value(iter2, 0)
        if s1 and s2: return cmp(s1.time(), s2.time())
        else: return 0

class _snapshot_list(gtk.VBox):
    __gsignals__ = {
                'snapshot_selected': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, [gobject.TYPE_PYOBJECT]),
                }
    
    def __init__(self):
        self.store = _snapshot_store()
        self.sorted_store = gtk.TreeModelSort(self.store)
        self.sorted_store.set_sort_func(1000, self.store.sort_by_time)
        self.sorted_store.set_sort_column_id(1000, gtk.SORT_DESCENDING)
        
        r_time = gtk.CellRendererText()
        r_comment = gtk.CellRendererText()
        r_comment.set_property('editable', True)
        r_comment.connect('edited', self.r_comment_edited)
        c_date = gtk.TreeViewColumn()
        c_date.set_title(_('Date'))
        c_date.pack_start(r_time, False)
        c_date.set_cell_data_func(r_time, self.r_time_cell_function)
        c_date.set_sort_column_id(1000)
        c_comment = gtk.TreeViewColumn()
        c_comment.set_title(_('Comment'))
        c_comment.pack_start(r_comment)
        c_comment.set_cell_data_func(r_comment, self.r_comment_cell_function)
        view = self.view = gtk.TreeView(self.sorted_store)
        view.set_rules_hint(True)
        view.append_column(c_date)
        view.append_column(c_comment)
        view.get_selection().set_mode(gtk.SELECTION_SINGLE)
        view.get_selection().connect('changed', self.row_selected, view)
        view.set_tooltip_text(_('Double click to edit comment'))
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(view)
        scroll.set_size_request(300, -1)
        
        gtk.VBox.__init__(self, False, 5)
        self.pack_start(scroll)

    def r_comment_edited(self, render, path, new_text):
        snapshot = self.sorted_store[path][0]
        snapshot.set_comment(new_text)
        self.view.queue_draw()

    def row_selected(self, selection, treeview):
        store, iter = selection.get_selected()
        if iter == None:
            self.emit('snapshot_selected', None)
        else:
            sn = store.get_value(iter, 0)
            self.emit('snapshot_selected', sn)
    
    def r_time_cell_function(self, column, cell, model, iter):
        sn = model.get_value(iter, 0)
        if sn != None:
            assert isinstance(sn, Snapshot)
            cell.set_property('text', time_string(sn.time()))

    def r_comment_cell_function(self, column, cell, model, iter):
        sn = model.get_value(iter, 0)
        if sn != None:
            assert isinstance(sn, Snapshot)
            cell.set_property('text', sn.comment())

class _diff_list(gtk.VBox):
    def r_status_cell_func(column, cell, model, iter):
        installed = model.get_value(iter, 1)
        if installed:
            cell.set_property('text', _('was installed'))
            cell.set_property('foreground', 'blue')
        else:
            cell.set_property('text', _('was removed'))
            cell.set_property('foreground', 'red')

    def __init__(self):
        self.store = store = gtk.ListStore(str, bool) #package name, currently installed?
        self.sort_store = gtk.TreeModelSort(self.store)
        
        r_name = gtk.CellRendererText()
        c_name = gtk.TreeViewColumn()
        c_name.set_expand(True)
        c_name.pack_start(r_name)
        c_name.add_attribute(r_name, 'text', 0)
        c_name.set_sort_column_id(0)
        
        r_status = gtk.CellRendererText()
        c_status = gtk.TreeViewColumn()
        c_status.pack_start(r_status)
        c_status.set_sort_column_id(1)
        c_status.set_cell_data_func(r_status, self.r_status_cell_func)
        
        self.view = view = MultiDragTreeView(store)
        view.append_column(c_name)
        view.append_column(c_status)
        view.set_headers_visible(False)
        view.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.add(view)

        self.change_liststore = change_liststore = gtk.ListStore(str, bool) #package name, action
        r_name2 = gtk.CellRendererText()
        r_action2 = gtk.CellRendererText()
        c_name2 = gtk.TreeViewColumn()
        c_name2.set_expand(True)
        c_name2.pack_start(r_name2)
        c_name2.add_attribute(r_name2, 'text', 0)
        c_name2.set_sort_column_id(0)
        c_action2 = gtk.TreeViewColumn()
        c_action2.pack_start(r_action2)
        c_action2.set_sort_column_id(1)
        def change_render_action_func(column, cell, model, iter):
            installed = model.get_value(iter, 1)
            if installed: text = _('will be removed')
            else: text = _('will be installed')
            cell.set_property('text', text)
            if installed: cell.set_property('foreground', 'red')
            else: cell.set_property('foreground', 'blue')
        c_action2.set_cell_data_func(r_action2, 
                                                change_render_action_func)
        self.change_view = change_view = MultiDragTreeView(change_liststore)
        change_view.append_column(c_name2)
        change_view.append_column(c_action2)
        change_view.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

        change_view_scroll = gtk.ScrolledWindow()
        change_view_scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        change_view_scroll.set_shadow_type(gtk.SHADOW_IN)
        change_view_scroll.add(change_view)
        
        TARGETS = [('treeview_row', gtk.TARGET_SAME_APP, 0)]
        view.enable_model_drag_source(gtk.gdk.BUTTON1_MASK,
                                           TARGETS,
                                           gtk.gdk.ACTION_COPY)
        view.enable_model_drag_dest(TARGETS,
                                         gtk.gdk.ACTION_DEFAULT)
        view.connect('drag_data_get', self.drag_data_get_data)
        view.connect('drag_data_received', self.drag_data_received_data_dummy)
        change_view.enable_model_drag_source(gtk.gdk.BUTTON1_MASK,
                                             TARGETS,
                                             gtk.gdk.ACTION_MOVE)
        change_view.enable_model_drag_dest(TARGETS,
                                           gtk.gdk.ACTION_DEFAULT)
        change_view.connect('drag_data_get', self.drag_data_get_data)
        change_view.connect('drag_data_received', 
                            self.drag_data_received_data)

        table = gtk.Table()
        table.set_col_spacings(5)
        table.set_row_spacings(5)
        table.attach( scroll,                            0, 1, 1, 2 )
        table.attach( label_left_align( _('To do:') ),         1, 2, 0, 1, gtk.FILL, gtk.FILL )
        table.attach( change_view_scroll,                      1, 2, 1, 2 )
        bottom_box = gtk.HBox(False, 10)
        bottom_box.pack_start( self.__long_text_label(
         _('In order to revoke packages, '
            'you can drag items from the left box to the right box, '
            'then click the button. ') ) )
        button_apply = image_stock_button( gtk.STOCK_APPLY, _('Apply') )
        button_apply.connect('clicked', self.__revoke)
        bottom_box.pack_start(button_apply, False)
        table.attach( bottom_box,                                  0, 2, 2, 3, gtk.FILL, gtk.FILL)


    def show_difference(self, snapshot):
        assert isinstance(snapshot, Snapshot)
        

class SnapshotPane(gtk.VBox):
    icon = D+'sora_icons/m_snapshot.png'
    text = _('Snapshots')
    
    def __init__(self, main_view):
        self.snapshot_list = _snapshot_list()
        paned = gtk.HPaned()
        paned.pack1(self.snapshot_list)
        gtk.VBox.__init__(self, False, 5)
        self.pack_start(paned)
        