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
        country = treestore.get_value(iter, self.COUNTRY)
        org = treestore.get_value(iter, self.ORG)
        url = treestore.get_value(iter, self.URL)
        return bool( 
             self.search_content.search(country) or 
             self.search_content.search(org) or
             self.search_content.search(url) )

    def __fill_candidate_store(self):
        for item in all_candidate_repositories():
            try:
                time = ResponseTime.get(item[self.URL])
            except KeyError:
                time = self.NO_PING_RESPONSE
            item.append(time)
            self.candidate_store.append(item)

    def __get_candidate_repositories_box(self):
#        label = gtk.Label(_('All repositories:'))
#        label.set_alignment(0, 0)
#        from support.searchbox import SearchBox
#        searchbox = SearchBox(self.__callback__search_content_changed)
#        treeview = self.__get_candidate_repositories_treeview()
#        box = gtk.VBox(False, 5)
#        box.set_border_width(5)
#        box.pack_start(label, False)
#        box.pack_start(searchbox, False)
#        box.pack_start(treeview)
#        return box
        print 'NotImplemented'
        return gtk.VBox()

    def __get_state_box(self):
        print 'NotImplemented'
        return gtk.VBox()

    def __init__(self, main_view):
        assert hasattr(main_view, 'lock')
        assert hasattr(main_view, 'unlock')
        self.main_view = main_view
        ResponseTime.load()
        gtk.VBox.__init__(self, False, 5)
        self.candidate_store = gtk.ListStore(str, str, str, int) # country, org, url, response_time
        self.filted_store = self.candidate_store.filter_new()
        self.search_content = None
        self.filted_store.set_visible_func(self.__repository_visibility_function)
        self.sorted_store = gtk.TreeModelSort(self.filted_store)
        self.sorted_store.set_sort_column_id(self.COUNTRY, gtk.SORT_ASCENDING)
        self.__fill_candidate_store()

        self.progress_box = gtk.VBox(False, 5)
        box2 = gtk.VBox(False, 5)
        box2.pack_start(self.__get_candidate_repositories_box())
        box2.pack_start(self.progress_box, False)
        vpaned = gtk.VPaned()
        vpaned.pack1(self.__get_state_box(), False, True)
        vpaned.pack2(box2, True, True)
        self.pack_start(vpaned)

if __name__ == '__main__':
    path = Config.get_config_dir() + 'response_time_2'
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write('a\n1\nb\n2\n')
    ResponseTime.load()
    print ResponseTime.map
    ResponseTime.set('b', 3)
    