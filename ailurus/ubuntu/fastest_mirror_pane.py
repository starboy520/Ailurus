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
import gtk, pango
import sys, os
from lib import *
from libu import *
import libserver

class RepoCheckButton(gtk.CheckButton):
    def __init__(self, old_repo, new_repo):
        text = _('change %(old)s to %(new)s')%{'old':old_repo, 'new':new_repo}
        gtk.CheckButton.__init__(self, text)
        self.set_active(True)
        self.old_repo = old_repo
        self.new_repo = new_repo

class UbuntuFastestMirrorPane(gtk.VBox):
    icon = D+'sora_icons/m_fastest_repos.png'
    text = _('Fastest\nRepository')

    # This value is used in UbuntuFastestMirrorPane.candidate_store .
    # If the server does not respond PING, then its response time is NO_PING_RESPONSE .
    # This value is displayed as text "No response" in TreeView.
    NO_PING_RESPONSE = 100000000

    def get_fastest_repository(self):
        min_server = None
        min_time = self.NO_PING_RESPONSE
        # organization, country, URL, server, response time(in millisecond)
        for row in self.candidate_store:
            server = row[2]
            time = row[4]
            if time < min_time:
                min_server, min_time = server, time
        return min_server, min_time

    def __print_the_fastest_repository(self, msg, current_all, current_official):
        fastest, response_time = self.get_fastest_repository()
        if fastest:
            print >>msg, _('The fastest repository is %s;') % fastest, _('Its response time is %s millisecond.') % response_time
        else:
            print >>msg, _('<span color="red"><big>We have not searched out the fastest repository.</big></span>')

        if fastest:
            if fastest in current_official: 
                print >>msg, _('<span color="blue">The fastest repository is being used.</span>')
            else:
                print >>msg, _('<span color="red"><big>The fastest repository is not being used.</big></span>')
        print >>msg, ''

    def __print_repositories_currently_in_use(self, msg, current_all, current_official):
        print >>msg, _('Currently you are using these repositories:')
        for s in current_all:
            print >>msg, s,
            if s in current_official: print >>msg, _('(Official repository)'),
            else: print >>msg, _('(Third-party repository)'),
            print >>msg, ''
        print >>msg, ''

    def __print_repository_configuration_files(self, msg, current_all, current_official):
        import glob
        import os
        files = glob.glob('/etc/apt/sources.list.d/*.list')
        len_files = len(files)
        if len_files == 1:  print >>msg, _('There is one configuration file in /etc/apt/sources.list.d/')
        elif len_files > 1: print >>msg, _('There are %s configuration files in /etc/apt/sources.list.d/')%len_files

        if 0 < len_files <= 10:
            print >>msg, _('They are:'),
            for path in files:
                filename = os.path.split(path)[1]
                print >>msg, filename, 
            print >>msg, ''

    def __callback__refresh_state_box(self, *w):
        import StringIO
        msg = StringIO.StringIO()
        current_all = APTSource2.all_urls()
        current_official = APTSource2.official_urls()

        # print tip
        print >>msg, _('<small>(Click mouse right button to display the context menu.)</small>')
        
        self.__print_the_fastest_repository(msg, current_all, current_official)
        self.__print_repositories_currently_in_use(msg, current_all, current_official)
        self.__print_repository_configuration_files(msg, current_all, current_official)
        # show text
        self.label_state.set_markup(msg.getvalue())
        # set the menu-item sensitive state
        fastest = self.get_fastest_repository()[0]
        if fastest:
            self.mi_use_fastest_repo.set_sensitive(bool(fastest and (fastest not in current_official)))
        else:
            self.mi_use_fastest_repo.set_sensitive(False)

    def __callback__show_how_to_backup_repositories(self, *w):
        label = gtk.Label()
        label.set_selectable(True)
        label.set_markup(
          _('<b>Backup the configuration of repositories:</b>\n'
            'cd /etc/apt/\n'
            'tar czf ~/sources.backup.tar.gz sources.list sources.list.d/\n'
            '\n'
            '<b>Restore the configuration of repositories:</b>\n'
            'cd /etc/apt/\n'
            'sudo tar xzf ~/sources.backup.tar.gz') )
        def unselect(*w):
            if not label.unselected:
                label.unselected = True
                label.select_region(0, 0)
            return False
        label.unselected = False
        label.connect('expose-event', unselect)
        button_close = gtk.Button(stock = gtk.STOCK_CLOSE)
        button_close.connect('clicked', lambda *w: window.destroy())
        box = gtk.VBox(False, 10)
        box.pack_start(label, False)
        box.pack_start(button_close, False)
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_border_width(10)
        window.set_title( _('Backup and restore the configuration of repositories') )
        window.add(box)
        window.set_position(gtk.WIN_POS_CENTER)
        window.show_all()
        button_close.grab_focus()

    def __callback__use_fastest_repository(self, *w):
        fastest = self.get_fastest_repository()[0]
        if fastest:
            self.__use_repository(fastest)

    def __get_popupmenu_for_state_box(self):
        mi_refresh = image_stock_menuitem(gtk.STOCK_REFRESH, _('Refresh'))
        mi_refresh.connect('activate', self.__callback__refresh_state_box)
        self.mi_use_fastest_repo = mi_use_fastest_repo = image_stock_menuitem(gtk.STOCK_GO_FORWARD, _('Use the fastest repository'))
        mi_use_fastest_repo.connect('activate', self.__callback__use_fastest_repository)
        mi_edit_by_texteditor = image_stock_menuitem(gtk.STOCK_EDIT, _('Edit repository configuration by text editor'))
        mi_edit_by_texteditor.connect('activate', self.__callback__edit_repository_by_text_editor)
        mi_edit_by_synaptic = image_stock_menuitem(gtk.STOCK_EDIT, _('Edit repository configuration by Synaptic'))
        mi_edit_by_synaptic.connect('activate', self.__callback__edit_apt_sources_by_synaptic)
        mi_merge_sourceslist = gtk.MenuItem(_('Merge all files in /etc/apt/sources.list.d/ into /etc/apt/sources.list'))
        mi_merge_sourceslist.connect('activate', self.__callback__merge_sourceslist)
        how_to_backup = image_stock_menuitem(gtk.STOCK_HELP, _('How to backup and restore the configuration of repositories?'))
        how_to_backup.connect('activate', self.__callback__show_how_to_backup_repositories)
        menu = gtk.Menu()
        menu.append(mi_refresh)
        menu.append(mi_use_fastest_repo)
        menu.append(mi_edit_by_texteditor)
        import os
        if os.path.exists('/usr/bin/software-properties-gtk') or os.path.exists('/usr/bin/software-properties-kde'):
            menu.append(mi_edit_by_synaptic)
        menu.append(mi_merge_sourceslist)
        menu.append(how_to_backup)
        menu.show_all()
        return menu

    def __get_state_box(self):
        self.label_state = label_state = gtk.Label()
        label_state.set_alignment(0, 0)
        label_state.set_ellipsize(pango.ELLIPSIZE_END)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_border_width(5)
        scroll.add_with_viewport(label_state)
        scroll.get_child().set_shadow_type(gtk.SHADOW_ETCHED_IN)
        scroll.set_tooltip_text(_('Click mouse right button to display the context menu.'))
        popupmenu = self.__get_popupmenu_for_state_box()
        def button_press_event(w, event):
            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
                popupmenu.popup(None, None, None, event.button, event.time)
                return True
            return False
        scroll.connect('button_press_event', button_press_event)
        self.__callback__refresh_state_box()
        return scroll
    
    def __show_response_time_in_cell(self, column, cell, model, iter):
        value = model.get_value(iter, 4)
        assert isinstance(value, int)
        if value == self.NO_PING_RESPONSE: 
            text = _('No response')
        else:
            text = '%s ms' % value
        cell.set_property('text', text)

    def __callback__select_all_repos_in_selected_country(self, w, treeview):
        selection = treeview.get_selection()
        model, pathlist = selection.get_selected_rows()
        if pathlist == None or len(pathlist)==0: # select nothing
            return
        
        countries = set()
        for path in pathlist:
            iter = model.get_iter(path)
            country = model.get_value(iter, 1)
            countries.add(country)
        
        iter = model.get_iter_first()
        while iter:
            country = model.get_value(iter, 1)
            if country in countries:
                selection.select_path(model.get_path(iter))
            iter = model.iter_next(iter)

    def __show_and_return_widgets_in_progress_box(self):
        progress_label = gtk.Label()
        progress_bar = gtk.ProgressBar()
        for child in self.progress_box.get_children():
            self.progress_box.remove(child)
        self.progress_box.pack_start(progress_label, False)
        self.progress_box.pack_start(progress_bar, False)
        self.progress_box.show_all()
        while gtk.events_pending(): gtk.main_iteration()
        return progress_label, progress_bar

    def __delete_all_widgets_in_progress_box(self):
        for child in self.progress_box.get_children():
            self.progress_box.remove(child)
            child.destroy()

    def __show_result_in_progress_box(self, result, total, progress_label, progress_bar):
        assert isinstance(result, list)
        assert isinstance(total, int)
        
        len_result = len(result)
        if len_result == 0: return
        server, value = result[-1]

        #display progress
        progress = float(len_result) / total
        progress_bar.set_fraction(progress)
        progress_bar.set_text('%s / %s' % (len_result, total) )
        #display text
        if isinstance(value, float):
            text = _("<span color='black'>Response time of %(server)s is %(value).2f ms.</span>") % {'server' : server, 'value' : value}
        elif value == 'cannot ping' or value == 'unreachable':
            text = _("<span color='black'>Server %s is unreachable.</span>") % server
        else:
            raise ValueError(value)
        progress_label.set_markup(text)
        while gtk.events_pending(): gtk.main_iteration()

    def __use_repository(self, new_repo):
        assert isinstance(new_repo, str)
        assert ':' in new_repo
        
        old_repos = [ r for r in APTSource2.official_urls() if r != new_repo ]
        if old_repos == []: 
            notify(_('Currently you are using %s.')%new_repo, ' ')
            return
        
        check_boxes = []
        for r in old_repos:
            check_boxes.append( RepoCheckButton(r, new_repo) )
        
        dialog = gtk.Dialog( _('Change repository'), None, 
            gtk.DIALOG_NO_SEPARATOR,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_NO, gtk.STOCK_OK, gtk.RESPONSE_YES))
        dialog.vbox.set_spacing(5)
        for i in check_boxes: dialog.vbox.pack_start(i, False)
        dialog.vbox.show_all()
        ret = dialog.run()
        dialog.destroy()
        if ret!=gtk.RESPONSE_YES: return

        changes = {}
        for c in check_boxes:
            if c.get_active():
                changes[c.old_repo] = c.new_repo
        if changes == {}: return
        libserver.change_repositories_in_source_files(changes)
        self.__callback__refresh_state_box()
        notify(_('Run "apt-get update". Please wait for few minutes.'), ' ')
        APT.apt_get_update()
    
    def __callback__use_selected_repositories_via_treeview(self, w, treeview):
        selection = treeview.get_selection()
        model, pathlist = selection.get_selected_rows()
        if pathlist == None or len(pathlist)==0: # select nothing
            return
        
        if len(pathlist) > 1: 
            notify(_('Please select one repository only'), ' ')
        else:
            path = pathlist[0]
            iter = model.get_iter(path)
            URL = model.get_value(iter, 2)
            self.__use_repository(URL)
    
    def __detect_servers_speed(self, urls, servers):
        assert len(urls) == len(servers)
        assert isinstance(urls, list)
        assert isinstance(servers, list)
        
        import threading
        result = []
        total = len(servers)
        threads = []

        self.main_view.lock()
        self.set_sensitive(False)
        progress_label, progress_bar = self.__show_and_return_widgets_in_progress_box()

        for url,server in zip(urls,servers):
            def alive_threads(threads):
                i = 0
                for t in threads:
                    if t.isAlive(): i += 1
                return i
            while alive_threads(threads)>10:
                import time
                time.sleep(0.1)
            thread = PingThread(url, server, result)
            threads.append( thread )
            thread.start()
            self.__show_result_in_progress_box(result, total, progress_label, progress_bar)
        for thread in threads:
            if not thread.isAlive(): continue
            thread.join()
            self.__show_result_in_progress_box(result, total, progress_label, progress_bar)
        self.__update_candidate_store_with_ping_result(result)
        self.__callback__refresh_state_box()
        self.__delete_all_widgets_in_progress_box()
        self.main_view.unlock()
        self.set_sensitive(True)

    def __callback__detect_all_repos_speed(self, w):
        servers = []
        urls = []
        for row in self.candidate_store:
            urls.append(row[2]) 
            servers.append(row[3])
        self.__detect_servers_speed(urls, servers)
        
    def __callback__copy_selected_repos(self, w, treeview):
        selection = treeview.get_selection()
        model, pathlist = selection.get_selected_rows()
        if pathlist == None or len(pathlist)==0: # select nothing
            return
        
        import StringIO
        msg = StringIO.StringIO()
        for path in pathlist:
            iter = model.get_iter(path)
            print >>msg, model.get_value(iter, 2)
        content = msg.getvalue()
        clipboard = gtk.clipboard_get()
        clipboard.set_text(content)

    def __callback__detect_selected_repos_speed(self, w, treeview):
        selection = treeview.get_selection()
        model, pathlist = selection.get_selected_rows()
        if pathlist == None or len(pathlist)==0: # select nothing
            return
        
        servers = []
        urls = []
        for path in pathlist:
            iter = model.get_iter(path)
            server = model.get_value(iter, 3)
            url = model.get_value(iter, 2)
            servers.append(server)
            urls.append(url)
        self.__detect_servers_speed(urls, servers)
        
    def __update_candidate_store_with_ping_result(self, result):
        for i in result:
            server = i[0]
            if isinstance(i[1], float):
                time = int(i[1])
                ResponseTime.set(server, time)
            else:
                time = self.NO_PING_RESPONSE
        for row in self.candidate_store:
            try:
                server = row[3]
                row[4] = ResponseTime.get(server)
            except KeyError:
                pass
        
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
        
        copy_repos = gtk.ImageMenuItem(stock_id = gtk.STOCK_COPY)
        copy_repos.connect('activate', self.__callback__copy_selected_repos, treeview)
        popupmenu = gtk.Menu()
        popupmenu.append(use_selected)
        popupmenu.append(detect_speed_of_selected_repos)
        popupmenu.append(detect_speed_of_all_repos)
        popupmenu.append(select_all)
        popupmenu.append(copy_repos)
        popupmenu.append(select_all_repos_in_this_county)
        popupmenu.append(unselect_all)
        popupmenu.append(contact_maintainer)
        popupmenu.show_all()
        return popupmenu

    def __get_candidate_repositories_treeview(self):
        render_country = gtk.CellRendererText()
        column_country = gtk.TreeViewColumn( _('Country') )
        column_country.pack_start(render_country)
        column_country.add_attribute(render_country, 'text', 1)
        column_country.set_sort_column_id(1)
        
        render_org = gtk.CellRendererText()
        render_org.set_property('ellipsize', pango.ELLIPSIZE_END)
        column_org = gtk.TreeViewColumn( _('Organization') )
        column_org.pack_start(render_org)
        column_org.add_attribute(render_org, 'text', 0)
        column_org.set_sort_column_id(0)
        column_org.set_expand(True)
        column_org.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        
        render_url = gtk.CellRendererText()
        render_url.set_property('ellipsize', pango.ELLIPSIZE_END)
        column_url = gtk.TreeViewColumn('URL')
        column_url.pack_start(render_url)
        column_url.add_attribute(render_url, 'text', 2)
        column_url.set_sort_column_id(3)
        column_url.set_expand(True)
        column_url.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        
        render_response_time = gtk.CellRendererText()
        render_response_time.set_property('ellipsize', pango.ELLIPSIZE_END)
        column_response_time = gtk.TreeViewColumn( _('Response time') )
        column_response_time.pack_start(render_response_time)
        column_response_time.set_cell_data_func(render_response_time, self.__show_response_time_in_cell)
        column_response_time.set_sort_column_id(4)
        
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
    
    def __repository_visibility_function(self, treestore, iter):
        if self.search_content == None:
            return True
        else:
            org = treestore.get_value(iter, 0)
            country = treestore.get_value(iter, 1)
            URL = treestore.get_value(iter, 2)
            server = treestore.get_value(iter, 3)
            return bool( self.search_content.search(org) or 
                 self.search_content.search(country) or
                 self.search_content.search(URL) or
                 self.search_content.search(server) )
    
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

    def __fill_candidate_store(self):
        for e in libserver.get_candidate_repositories():
            try:
                res_time = ResponseTime.get(e[3])
            except KeyError:
                res_time = self.NO_PING_RESPONSE
            e.append(res_time)
            self.candidate_store.append(e)

    def __init__(self, main_view):
        assert hasattr(main_view, 'lock')
        assert hasattr(main_view, 'unlock')
        self.main_view = main_view
        
        ResponseTime.load()
        
        gtk.VBox.__init__(self, False, 5)
        # organization, country, URL, server, response time(in millisecond)
        self.candidate_store = gtk.ListStore(str, str, str, str, int)
        self.filted_store = self.candidate_store.filter_new()
        self.search_content = None
        self.filted_store.set_visible_func(self.__repository_visibility_function)
        self.sorted_store = gtk.TreeModelSort(self.filted_store)
        self.sorted_store.set_sort_column_id(1, gtk.SORT_ASCENDING)
        self.__fill_candidate_store()

        self.progress_box = gtk.VBox(False, 5)

        box2 = gtk.VBox(False, 5)
        box2.pack_start(self.__get_candidate_repositories_box())
        box2.pack_start(self.progress_box, False)
        vpaned = gtk.VPaned()
        vpaned.pack1(self.__get_state_box(), False, True)
        vpaned.pack2(box2, True, True)
        self.pack_start(vpaned)

    def __callback__edit_repository_by_text_editor(self, *w):
        fastest = self.get_fastest_repository()[0]
        if not fastest:
            fastest = 'http://archive.ubuntu.com/ubuntu/'
        
        # We create an example file.
        f = open('/tmp/Example-of-sources.list', 'w')
        f.write( _('''# Do not edit this file. This is just an example.
# The following content can be copy-pasted into /etc/apt/sources.list

''') )
        f.write('''deb %(fastest)s %(version)s main restricted universe multiverse 
deb %(fastest)s %(version)s-backports restricted universe multiverse 
deb %(fastest)s %(version)s-proposed main restricted universe multiverse 
deb %(fastest)s %(version)s-security main restricted universe multiverse 
deb %(fastest)s %(version)s-updates main restricted universe multiverse 
deb-src %(fastest)s %(version)s main restricted universe multiverse 
deb-src %(fastest)s %(version)s-backports main restricted universe multiverse 
deb-src %(fastest)s %(version)s-proposed main restricted universe multiverse 
deb-src %(fastest)s %(version)s-security main restricted universe multiverse 
deb-src %(fastest)s %(version)s-updates main restricted universe multiverse
'''%{'fastest':fastest, 'version':VERSION} )
        f.close()

        paths = ['/tmp/Example-of-sources.list'] + APTSource2.all_conf_files()
        editor = 'xdg-open'
        if os.path.exists('/usr/bin/gedit'): editor = 'gedit'
        elif os.path.exists('/usr/bin/kate'): editor = 'kate'
        elif os.path.exists('/usr/bin/mousepad'): editor = 'mousepad'
        for path in paths:
            spawn_as_root("%s '%s'"%(editor, path))

    def __callback__edit_apt_sources_by_synaptic(self, *w):
        import os
        if os.path.exists('/usr/bin/software-properties-gtk'):
            launcher = '/usr/bin/software-properties-gtk'
        elif os.path.exists('/usr/bin/software-properties-kde'):
            launcher = '/usr/bin/software-properties-kde'
        else:
            raise Exception
        
        spawn_as_root(launcher)
    
    def __callback__merge_sourceslist(self, *w):
        with TempOwn('/etc/apt/sources.list') as o:
            with open('/etc/apt/sources.list', 'w') as f:
                f.writelines(APTSource2.all_lines())
        run_as_root('rm /etc/apt/sources.list.d/* -rf')
        
if __name__ == '__main__':
    class Dummy:
        def lock(self): pass
        def unlock(self): pass
    window = gtk.Window()
    window.set_size_request(-1, 700)
    window.set_position(gtk.WIN_POS_CENTER)
    window.connect('delete-event', gtk.main_quit)
    obj = UbuntuFastestMirrorPane(Dummy())
    window.add(obj)
    window.show_all()
    gtk.main()
