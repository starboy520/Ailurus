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
import gtk, pango
import sys, os
from lib import *
from libu import *
from libserver import *

class FedoraFastestMirrorPane(gtk.VBox):
    name = _('Find fastest repository mirror')

    COUNTRY = 0
    ORG = 1
    URL = 2
    RESPONSE_TIME = 3
    NO_PING_RESPONSE = 10000
    
    def __repository_visibility_function(self, treestore, iter):
        if self.search_content == None:
            return True
        else:
            country = treestore.get_value(iter, self.COUNTRY)
            org = treestore.get_value(iter, self.ORG)
            url = treestore.get_value(iter, self.URL)
            return bool( self.search_content.search(country) or 
                 self.search_content.search(org) or
                 self.search_content.search(url) )

    def __fill_candidate_store(self):
        for e in libserver.get_candidate_repositories():
            try:
                res_time = self.__response_times[ e[self.URL] ]
            except KeyError:
                res_time = self.NO_PING_RESPONSE
            e.append(res_time)
            self.candidate_store.append(e)

    def __callback__search_content_changed(self, itext):
        assert isinstance(itext, str)
        if not itext:
            self.search_content = None
        else:
            import StringIO
            import re
            otext = StringIO.StringIO()
            for char in itext:
                if char in r'.^$+*?{}[]\|()': otext.write('\\')
                otext.write(char)
            self.search_content = re.compile(otext.getvalue(), re.IGNORECASE)
        self.filted_store.refilter()

    def __show_response_time_in_cell(self, column, cell, model, iter):
        value = model.get_value(iter, 4)
        assert isinstance(value, int)
        if value == self.NO_PING_RESPONSE: 
            text = _('No response')
        else:
            text = '%s ms' % value
        cell.set_property('text', text)

    def __get_popupmenu_for_candidate_repos_treeview(self, treeview):
        detect_speed_of_selected_repos = image_stock_menuitem(gtk.STOCK_FIND,
            _('Detect response time of selected repositories'))
        detect_speed_of_selected_repos.connect('activate', self.__callback__detect_selected_repos_speed, treeview)

        detect_speed_of_all_repos = image_stock_menuitem(gtk.STOCK_FIND,
            _('Detect response time of all repositories'))
        detect_speed_of_all_repos.connect('activate', self.__callback__detect_all_repos_speed)

        use_selected = image_stock_menuitem(
            gtk.STOCK_GO_FORWARD, _('Use selected repositories'))
        use_selected.connect('activate', self.__callback__use_selected_repositories_via_treeview, treeview)
        
        select_all = image_stock_menuitem(gtk.STOCK_SELECT_ALL, _('Select all'))
        select_all.connect('activate', lambda w: treeview.get_selection().select_all())
        select_all_repos_in_this_county = image_stock_menuitem(gtk.STOCK_SELECT_ALL, 
            _('Select all repositories in these countries'))
        select_all_repos_in_this_county.connect('activate', self.__callback__select_all_repos_in_selected_country, treeview)
        
        unselect_all = gtk.MenuItem(_('Unselect all'))
        unselect_all.connect('activate', lambda w: treeview.get_selection().unselect_all())
        
        contact_maintainer = image_stock_menuitem(gtk.STOCK_DIALOG_WARNING, 
            _('If some repositories are not listed above, please click here to tell Ailurus developers.') )
        contact_maintainer.connect('activate', lambda w: report_bug() )
        
        popupmenu = gtk.Menu()
        popupmenu.append(detect_speed_of_selected_repos)
        popupmenu.append(detect_speed_of_all_repos)
        popupmenu.append(gtk.SeparatorMenuItem())
        popupmenu.append(use_selected)
        popupmenu.append(gtk.SeparatorMenuItem())
        popupmenu.append(select_all)
        popupmenu.append(select_all_repos_in_this_county)
        popupmenu.append(unselect_all)
        popupmenu.append(gtk.SeparatorMenuItem())
        popupmenu.append(contact_maintainer)
        popupmenu.show_all()
        return popupmenu

    def __get_candidate_repositories_treeview(self):
        render_country = gtk.CellRendererText()
        column_country = gtk.TreeViewColumn( _('Country') )
        column_country.pack_start(render_country)
        column_country.add_attribute(render_country, 'text', 1)
        column_country.set_sort_column_id(0)
        
        render_org = gtk.CellRendererText()
        render_org.set_property('ellipsize', pango.ELLIPSIZE_END)
        column_org = gtk.TreeViewColumn( _('Organization') )
        column_org.pack_start(render_org)
        column_org.add_attribute(render_org, 'text', 1)
        column_org.set_sort_column_id(1)
        column_org.set_expand(True)
        column_org.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        
        render_url = gtk.CellRendererText()
        render_url.set_property('ellipsize', pango.ELLIPSIZE_END)
        column_url = gtk.TreeViewColumn('URL')
        column_url.pack_start(render_url)
        column_url.add_attribute(render_url, 'text', 2)
        column_url.set_sort_column_id(2)
        column_url.set_expand(True)
        column_url.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        
        render_response_time = gtk.CellRendererText()
        render_response_time.set_property('ellipsize', pango.ELLIPSIZE_END)
        column_response_time = gtk.TreeViewColumn( _('Response time') )
        column_response_time.pack_start(render_response_time)
        column_response_time.set_cell_data_func(render_response_time, self.__show_response_time_in_cell)
        column_response_time.set_sort_column_id(3)
        
        candidate_treeview = gtk.TreeView(self.sorted_store)
        candidate_treeview.set_rules_hint(True)
        candidate_treeview.append_column(column_country)
        candidate_treeview.append_column(column_org)
        candidate_treeview.append_column(column_url)
        candidate_treeview.append_column(column_response_time)
        candidate_treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        candidate_treeview.set_tooltip_text(_('Click mouse right button to display the context menu.'))
        popupmenu = self.__get_popupmenu_for_candidate_repos_treeview(candidate_treeview)
        def button_press_event(w, event):
            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
                path = w.get_path_at_pos(int(event.x),int(event.y))
                selection = w.get_selection()
                if path == None: selection.unselect_all()
                elif selection.path_is_selected(path[0])==False: 
                    selection.unselect_all()
                    selection.select_path(path[0])
                popupmenu.popup(None, None, None, event.button, event.time)
                return True
            return False
        candidate_treeview.connect('button_press_event', button_press_event)
        
        candidate_scroll = gtk.ScrolledWindow()
        candidate_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        candidate_scroll.set_shadow_type(gtk.SHADOW_IN)
        candidate_scroll.add(candidate_treeview)

        return candidate_scroll

    def __get_candidate_repositories_box(self):
        label = gtk.Label(_('All repositories:'))
        label.set_alignment(0, 0)
        from support.searchbox import SearchBox
        searchbox = SearchBox(self.__callback__search_content_changed)
        treeview = self.__get_candidate_repositories_treeview()
        box = gtk.VBox(False, 5)
        box.set_border_width(5)
        box.pack_start(label, False)
        box.pack_start(searchbox, False)
        box.pack_start(treeview)
        return box

    def __init__(self, main_view):
        assert hasattr(main_view, 'lock')
        assert hasattr(main_view, 'unlock')
        self.main_view = main_view

        self.search_content = None # an RE pattern object

        gtk.VBox.__init__(self, False, 5)
        # country, org, url, response time(in millisecond)
        self.candidate_store = gtk.ListStore(str, str, str, int)
        self.filted_store = self.candidate_store.filter_new()
        self.filted_store.set_visible_func(self.__repository_visibility_function)
        self.sorted_store = gtk.TreeModelSort(self.filted_store)
        self.sorted_store.set_sort_column_id(1, gtk.SORT_ASCENDING)
        self.__fill_candidate_store()
        
        self.progress_box = gtk.VBox(False, 5)

        box2 = gtk.VBox(False, 5)
        box2.pack_start(self.__get_candidate_repositories_box())
        box2.pack_start(self.progress_box, False)
        self.pack_start(box2)

class FedoraFastestMirrorPane(gtk.VBox):
    name = _('Find fastest repository mirror')

    def __init__(self, *w):
        gtk.VBox.__init__(self, False, 10)