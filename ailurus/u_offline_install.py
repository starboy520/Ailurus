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
import gtk
from lib import *
from ulib import *

class OfflineInstallPane(gtk.VBox):
    name = _('Cache installation files')
    
    def __change_cache_dir_from_GUI(self, new_dir):
        self.entry_dir.set_text(new_dir)
        Config.set_cache_dir(new_dir)
        try:
            freespace = free_space(new_dir)
            text = derive_size(freespace)
        except OSError:
            text = _('N/A ( Directory does not exist. It will be automatically created before beginning cache files. )')
        except:
            import traceback, sys
            traceback.print_exc(file=sys.stderr)
        self.label_free_space.set_text(text)
    def select_cache_dir(self, widget, entry_dir):
        chooser = gtk.FileChooserDialog( _('Select a folder'), None,
                 gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
                 gtk.STOCK_OPEN,gtk.RESPONSE_OK)
                )
        chooser.set_current_folder( entry_dir.get_text() )
        chooser.set_select_multiple( False )

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            self.__change_cache_dir_from_GUI( chooser.get_filename() )

        chooser.destroy()
    def cached(self, filename):
        path = self.entry_dir.get_text()
        import os
        return os.path.exists(path+'/'+filename)
    def __refresh_files_list(self):
        self.uncached_files_liststore.clear()
        uncached = 0
        cached = 0
        for r in self.R_objs:
            if self.cached(r.filename):
                cached += 1
            else:
                uncached += 1
                self.uncached_files_liststore.append([r])
        self.label_files_msg.set_text( 
            _('%(uncached)s uncached files, %(cached)s cached files')
               %{'uncached':uncached, 'cached':cached} )
    def update_GUI(self):
        while gtk.events_pending(): gtk.main_iteration()
    def __download_thread(self):
        model, paths = self.treeview_uncached_files.get_selection().get_selected_rows()
        dir = self.entry_dir.get_text()
        import traceback, os, sys, StringIO
        #store error message
        error_msg = StringIO.StringIO()
        #count number
        success = fail = 0
        try:
            run.terminal = self.terminal
            r, w = os.pipe()
            os.dup2(w, sys.stdout.fileno())
            #do wget
            for path in paths:
                iter = model.get_iter(path)
                r = model.get_value(iter, 0)
                print >>sys.stderr, r.filename
                try: 
                    src = r.download()
                    dest = dir+'/'+r.filename
                    if src!=dest: run('mv "%s" "%s"'%(src, dest))
                    success += 1
                except: 
                    traceback.print_exc(file=error_msg)
                    fail += 1
        except:
            traceback.print_exc(file=error_msg)
        finally:
            run.terminal = None
            os.dup2(self.backup_stdout, sys.stdout.fileno())
            gtk.gdk.threads_enter()
            #display summary
            msg = StringIO.StringIO()
            print >>msg, _('Tried to download %s files.')%(success+fail)
            if success: print >>msg, _('%s files are downloaded successfully.')%success
            if fail: print >>msg, _('%s files cannot be downloaded.')%fail
            if error_msg.getvalue():
                print >>msg
                print >>msg, error_msg.getvalue()
            dialog = gtk.MessageDialog( None,
                gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,
                gtk.BUTTONS_OK, 
                msg.getvalue() )
            dialog.set_title('Summary')
            dialog.run()
            dialog.destroy()
            #change content
            parent = self.parent_window
            for child in parent.get_children():
                parent.remove(child)
            parent.add(self)
            parent.show_all()
            #refresh file list
            try:       self.__refresh_files_list()
            except: traceback.print_exc(file=sys.stderr)
            #unlock GUI
            self.mainview.unlock()
            gtk.gdk.threads_leave()
        
    def __cache_files(self, w):
        model, paths = self.treeview_uncached_files.get_selection().get_selected_rows()
        if len(paths)==0: return
        import traceback, sys, os
        try:
            #create dir if not exist
            dir = self.entry_dir.get_text()
            if not os.path.exists(dir):
                gksudo('mkdir -p %s'%dir)
            own_by_user(dir)
            #lock GUI
            self.mainview.lock()
            #change content
            self.parent_window = parent = self.parent
            for child in parent.get_children():
                parent.remove(child)
            parent.add(self.terminal.get_widget())
            self.terminal.terminal.reset(True, True)
            parent.show_all()
            import thread
            thread.start_new_thread(self.__download_thread, ())
        except: 
            traceback.print_exc(file=sys.stderr)
    
    def __show_urls(self, w):
        model, paths = self.treeview_uncached_files.get_selection().get_selected_rows()
        if len(paths)==0: return
        import traceback, sys
        try:
            temp = open('/tmp/ailurus___resource_URLs', 'w')
            for path in paths:
                iter = model.get_iter(path)
                obj = model.get_value(iter, 0)
                print >>temp, obj.filename
                for url in obj.url:
                    print >>temp, url
                print >>temp
            temp.close()
            run('xdg-open '+temp.name)
        except: 
            traceback.print_exc(file=sys.stderr)
    def __init__(self, mainview, R_objs):
        gtk.VBox.__init__(self, False, 5)
        assert hasattr(mainview, 'lock')
        assert hasattr(mainview, 'unlock')
        self.mainview = mainview
        assert isinstance(R_objs, list)
        for obj in R_objs: assert isinstance(obj, R)
        self.R_objs = R_objs
        from support.terminal import Terminal
        self.terminal = Terminal()
        import os, sys
        self.backup_stdout = os.dup(sys.stdout.fileno())
        
        self.set_border_width(5)
        
        text = _('You can install applications without Internet if software installation files are cached into your computer. ' 
'Moreover, the download time is saved by caching.')
        if Config.is_Ubuntu() or Config.is_Mint():
            text += _('\nAilurus cannot cache "*.deb" packages which are in /var/cache/apt . '
'You can cache them by "aptoncd", which is installed by "sudo apt-get install aptoncd". ')
        explain = gtk.TextView()
        explain.get_buffer().set_text(text)
        explain.set_wrap_mode(gtk.WRAP_WORD)
        explain.set_editable(False)
        explain.set_cursor_visible(False)
        gray_bg(explain)
        
        check_disable_clean = gtk.CheckButton( _('Do not automatically delete cached APT packages.') )
        check_disable_clean.set_active( Config.get_disable_clean_apt_cache() )
        check_disable_clean.connect( 'clicked', lambda w: Config.set_disable_clean_apt_cache(w.get_active()) )
        
        label_dir = gtk.Alignment(0)
        label_dir.add( gtk.Label(_('Cache files in this directory:')) )
        self.entry_dir = entry_dir = gtk.Entry()
        gray_bg(entry_dir)
        button_edit_dir = image_stock_button( gtk.STOCK_EDIT, _('Change') )
        button_edit_dir.connect('clicked', self.select_cache_dir, entry_dir)
        self.button_open_dir = button_open_dir = image_stock_button( gtk.STOCK_OPEN, _('Open') )
        def open_dir(w):
            dir = self.entry_dir.get_text()
            import os
            if not os.path.exists(dir):
                gksudo('mkdir -p "%s"'%dir)
            own_by_user(dir)
            KillWhenExit.add('xdg-open "%s"'%dir)
        button_open_dir.connect('clicked', open_dir)
        box_dir = gtk.HBox(False, 5)
        box_dir.pack_start(entry_dir)
        box_dir.pack_start(button_edit_dir, False, False)
        box_dir.pack_start(button_open_dir, False, False)
        self.label_free_space = label_free_space = gtk.Label()
        box_free_space = gtk.HBox(False, 5)
        box_free_space.pack_start( gtk.Label( _('Free disk space:') ), False, False )
        box_free_space.pack_start( label_free_space, False, False )
        
        label_uncached_files = gtk.Alignment(0, 0.5)
        label_uncached_files.add( gtk.Label( _('Uncached files:') ) )
        self.button_show_url = button_show_url = image_stock_button( gtk.STOCK_ZOOM_IN, _('Show URL') )
        button_show_url.connect('clicked', self.__show_urls)
        self.button_cache_files = button_cache_files = image_stock_button(gtk.STOCK_HARDDISK, _('Download') )
        button_cache_files.connect('clicked', self.__cache_files)

        box_uncached_files = gtk.HBox(False, 5)
        box_uncached_files.pack_start(label_uncached_files, False, False)
        box_uncached_files.pack_end(button_cache_files, False, False)
        box_uncached_files.pack_end(button_show_url, False, False)
        import gobject
        self.uncached_files_liststore = uncached_files_liststore = gtk.ListStore(gobject.TYPE_PYOBJECT) # R object
        def sort_filename_func(model, iter1, iter2):
            r1, r2 = model.get_value(iter1,0), model.get_value(iter2,0)
            if r1 and r2:
                assert isinstance(r1, R), type(r1)
                assert isinstance(r2, R), type(r2)
                return cmp(r1.filename, r2.filename) 
            else:
                return cmp(r1, r2)
        uncached_files_liststore.set_sort_func(1000, sort_filename_func)
        def sort_size_func(model, iter1, iter2):
            r1, r2 = model.get_value(iter1,0), model.get_value(iter2,0)
            if r1 and r2:
                assert isinstance(r1, R), type(r1)
                assert isinstance(r2, R), type(r2)
                return cmp(r1.size, r2.size)
            else:
                return cmp(r1, r2)
        uncached_files_liststore.set_sort_func(1001, sort_size_func)

        sorted_files_liststore = gtk.TreeModelSort(uncached_files_liststore)
        sorted_files_liststore.set_sort_func(1000, sort_filename_func)
        sorted_files_liststore.set_sort_func(1001, sort_size_func)
        sorted_files_liststore.set_sort_column_id(1000, gtk.SORT_ASCENDING)
        
        cell_filename = gtk.CellRendererText()
        column_filename = gtk.TreeViewColumn( _('File name') )
        column_filename.set_alignment(0.5)
        column_filename.pack_start(cell_filename)
        def filename_func(column, cell, model, iter):
            r = model.get_value(iter, 0)
            cell.set_property('text', r.filename)
        column_filename.set_cell_data_func(cell_filename, filename_func)
        column_filename.set_sort_column_id(1000)
        column_filename.set_resizable(True)
#        column_filename.set_expand(True)
        
        cell_size = gtk.CellRendererText()
        column_size = gtk.TreeViewColumn( _('Size') )
        column_size.set_alignment(0.5)
        column_size.pack_start(cell_size)
        def size_func(column, cell, model, iter):
            r = model.get_value(iter, 0)
            if r.size: cell.set_property('text', derive_size(r.size))
            else:      cell.set_property('text', _('Unknown') )
        column_size.set_cell_data_func(cell_size, size_func)
        column_size.set_sort_column_id(1001)
        column_size.set_resizable(False)
        
        self.treeview_uncached_files = treeview_uncached_files = gtk.TreeView(sorted_files_liststore)
        treeview_uncached_files.append_column(column_filename)
        treeview_uncached_files.append_column(column_size)
        treeview_uncached_files.set_search_column(0)
        treeview_uncached_files.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        treeview_uncached_files.set_rules_hint(True)
        
        scroll_uncached_files = gtk.ScrolledWindow()
        scroll_uncached_files.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll_uncached_files.set_shadow_type(gtk.SHADOW_IN)
        scroll_uncached_files.add(treeview_uncached_files)

        self.label_files_msg = label_files_msg = gtk.Label( _('(States of files are not detected yet.)') )
        align_files_msg = gtk.Alignment(0, 0.5)
        align_files_msg.add(label_files_msg)
        box_files_msg = gtk.HBox(False, 5)
        box_files_msg.pack_start( align_files_msg, False, False )

        self.pack_start(explain, False, False)
        self.pack_start( gtk.HSeparator(), False, False)
        self.pack_start(label_dir, False, False)
        self.pack_start(box_dir, False, False)
        self.pack_start(box_free_space, False, False)
        self.pack_start( gtk.HSeparator(), False, False)
        self.pack_start(box_uncached_files, False, False)
        self.pack_start(scroll_uncached_files, True, True)
        self.pack_start(box_files_msg, False, False)
        self.show_all()
        
        dir = Config.get_cache_dir()
        self.__change_cache_dir_from_GUI( dir )
        self.__refresh_files_list()
