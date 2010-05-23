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
import gtk
from lib import *
from libu import *

class InstallRemovePane(gtk.VBox):
    icon = D+'sora_icons/m_install_remove.png'
    text = _('Install\nSoftware')
    
    def __left_tree_view_default_select(self):
        self.left_treeview.get_selection().unselect_all()
        self.left_treeview.expand_all()
        self.left_treeview.get_selection().select_path('0:0')

    def __left_pane_changed ( self, treeselection, treeview ):
        model, parent = treeselection.get_selected()
        if parent == None: return
        category = model.get_value(parent, 2)
        if category.startswith('*'): # A big class is selected
            # We add all children of this class to 'self.selected_categories'
            self.selected_categories = []
            child = model.iter_children(parent)
            while child:
                category = model.get_value(child, 2)
                self.selected_categories.append(category)
                child = model.iter_next(child)
                if child == None: break
        else: # An item is selected.
            self.selected_categories = [ category ]
        self.treestorefilter.refilter()

    def __left_pane_pixbuf(self, column, cell, model, iter):
        category = model.get_value(iter, 2)
        pixbuf = model.get_value(iter, 1)
        if category.startswith('*'): # This is a big class.
            cell.set_property('visible', False)
        else: # This is an item.
            cell.set_property('visible', True)
            cell.set_property('pixbuf', pixbuf)
    
    def __left_pane_text(self, column, cell, model, iter):
        category = model.get_value(iter, 2)
        text = model.get_value(iter, 0)
        if category.startswith('*'): # This is a big class.
            cell.set_property('markup', '<b>%s</b>'%text)
        else: # This is an item.
            cell.set_property('text', text)

    def __left_pane(self):
        pixbuf_render = gtk.CellRendererPixbuf()
        text_render = gtk.CellRendererText()
        column = gtk.TreeViewColumn()
        column.pack_start ( pixbuf_render, False )
        column.set_cell_data_func(pixbuf_render, self.__left_pane_pixbuf)
        column.pack_start ( text_render, False )
        column.set_cell_data_func(text_render, self.__left_pane_text)
        # each row of liststore contains ( title, icon, category )
        self.left_treestore = treestore = gtk.TreeStore ( str, gtk.gdk.Pixbuf, str )
        self.left_treeview = treeview = gtk.TreeView()
        treeview.append_column ( column )
        treeview.set_model(treestore)
        treeview.get_selection().set_mode(gtk.SELECTION_SINGLE)
        treeview.get_selection().connect('changed', self.__left_pane_changed, treeview )
        treeview.set_headers_visible(False)

        scrollwindow = gtk.ScrolledWindow ()
        scrollwindow.add ( treeview )
        scrollwindow.set_policy ( gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC )
        scrollwindow.set_shadow_type ( gtk.SHADOW_IN )
        return scrollwindow

    def __clean_and_show_vte_window(self):
        gtk.gdk.threads_enter()
        #clean_vte
        self.terminal.terminal.reset(True, True)
        #change_content
        parentbox = self.parent
        for child in parentbox.get_children():
            parentbox.remove(child)
        parentbox.add(self.terminal.get_widget())
        parentbox.show_all()
        gtk.gdk.threads_leave()
    
    def __query_work(self, to_install, to_remove):
        msg = ''
        if len(to_install):
            msg += _('To be installed:\n')
            for obj in to_install: 
                msg += '<span color="blue">%s</span>\n'%obj.__doc__
            msg += '\n'
        if len(to_remove):
            msg += _('To be removed:\n')
            for obj in to_remove: 
                msg += '<span color="red">%s</span>\n'%obj.__doc__
            msg += '\n' 
        
        dialog = gtk.MessageDialog( None,
            gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION,
            gtk.BUTTONS_YES_NO, _('Are you sure to change your system as follows?') )
        dialog.set_title( _('Confirmation') )
        dialog.format_secondary_markup(msg)
        ret = dialog.run()
        dialog.destroy()
        return ret == gtk.RESPONSE_YES

    def __show_summary(self, s_i, s_r, f_i, f_r):
        msg = _('Summary: \n\n')
        if len(s_i):
            msg += _('Successfully installed:\n')
            for obj in s_i: msg += '<span color="blue">%s</span>\n'%obj.__doc__
            msg += '\n'
        if len(s_r):
            msg += _('Successfully removed:\n')
            for obj in s_r: msg += '<span color="red">%s</span>\n'%obj.__doc__
            msg += '\n'
        if len(f_i):
            msg += _('Failed to install:\n')
            for tup in f_i:
                msg += '<span color="red">%s</span>\n'%tup[0].__doc__
            msg += _('The tracebacks are in the terminal window.\n\n')
        if len(f_r):
            msg += _('Failed to remove:\n')
            for tup in f_r: 
                msg += '<span color="red">%s</span>\n'%tup[0].__doc__
            msg += _('The tracebacks are in the terminal window.\n\n')
        gtk.gdk.threads_enter()
        dialog = gtk.MessageDialog( None,
            0, gtk.MESSAGE_QUESTION,
            gtk.BUTTONS_OK, _('All works finished.') )
        dialog.format_secondary_markup(msg)
        dialog.run()
        dialog.destroy()
        gtk.gdk.threads_leave()

    def app_class_installed_state_changed_by_external(self):
        for obj in self.app_objs:
            obj.showed_in_toggle = obj.cache_installed = obj.installed()
            
        level1 = self.treestore.get_iter_first()
        while level1!=None:
            level2 = self.treestore.iter_children(level1)
            while level2!=None:
                path = self.treestore.get_path(level2)
                self.treestore.row_changed(path, level2)
                level2 = self.treestore.iter_next(level2)
            level1 = self.treestore.iter_next(level1)

    def show_error(self, content):
        title_box = gtk.HBox(False, 5)
        import os
        if os.path.exists(D+'umut_icons/bug.png'):
            image = gtk.Image()
            image.set_from_file(D+'umut_icons/bug.png')
            title_box.pack_start(image, False)
        title = label_left_align( _('Some operations failed. Would you please copy and paste following text into bug report web-page?') )
        title_box.pack_start(title, False)
        
        textview = gtk.TextView()
        gray_bg(textview)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        textview.get_buffer().set_text(content)
        textview.set_cursor_visible(False)
        scroll = gtk.ScrolledWindow()
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add(textview)
        scroll.set_size_request(-1, 500)
        button_report_bug = image_stock_button(gtk.STOCK_DIALOG_WARNING, _('Click here to report bug via web-page') )
        button_report_bug.connect('clicked', lambda w: report_bug() )
        button_close = image_stock_button(gtk.STOCK_CLOSE, _('Close'))
        button_close.connect('clicked', lambda w: window.destroy())
        bottom_box = gtk.HBox(False, 10)
        bottom_box.pack_start(button_report_bug, False)
        bottom_box.pack_start(button_close, False)
        
        vbox = gtk.VBox(False, 5)
        vbox.pack_start(title_box, False)
        vbox.pack_start(scroll)
        vbox.pack_start(bottom_box, False)
        window = gtk.Window()
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_title(_('Some operations failed'))
        window.set_border_width(10)
        window.add(vbox)
        window.show_all()
    
    def __apply_change_thread(self):
        import os, sys, traceback, StringIO, thread, platform
        try:
            error_traceback = StringIO.StringIO()
            print >>error_traceback, platform.dist()
            print >>error_traceback, 'Ailurus version: ', AILURUS_VERSION
            self.__clean_and_show_vte_window()
            run.terminal = self.terminal
            r,w = os.pipe()
            os.dup2(w, sys.stdout.fileno())
            thread.start_new_thread(self.terminal.read, (r,) )
            run_as_root('true') # require authentication first. do not require authentication any more.
            s_i = []; s_r = []; f_i = []; f_r = []
            
            to_install = [ o for o in self.app_objs
                               if o.cache_installed==False
                               and o.showed_in_toggle ]
            depends = [ o.depends() for o in to_install # the type of o.depends is types.ClassType 
                                   if hasattr(o, 'depends') ]
            to_install += depends
            to_install_repos = [ o for o in to_install 
                                     if getattr(o, 'this_is_a_repository', False) ]
            to_install_non_repos = [ o for o in to_install
                                                 if o not in to_install_repos ]
            if to_install_repos:
                for obj in to_install_repos:
                    print '\x1b[1;32m', _('Installing:'), obj.__doc__, '\x1b[m'
                    try: 
                        reset_dir()
                        if not obj.installed(): obj.install()
                    except: f_i += [(obj, sys.exc_info())]
                    else: s_i += [obj]
                APT.apt_get_update()
                
            for obj in to_install_non_repos:
                print '\x1b[1;32m', _('Installing:'), obj.__doc__, '\x1b[m'
                try: 
                    reset_dir()
                    if not obj.installed(): obj.install()
                except: f_i += [(obj, sys.exc_info())]
                else: s_i += [obj]
            
            to_remove = [ o for o in self.app_objs
                         if o.cache_installed 
                         and o.showed_in_toggle==False ]
            for obj in to_remove:
                print '\x1b[1;35m', _('Removing:'), obj.__doc__, '\x1b[m'
                try: 
                    reset_dir()
                    obj.remove()
                except: f_r += [(obj, sys.exc_info())]
                else: s_r += [obj]
            
            for o in self.app_objs:
                o.showed_in_toggle = o.cache_installed = o.installed()
            
            gtk.gdk.threads_enter()
            level1 = self.treestore.get_iter_first()
            while level1!=None:
                level2 = self.treestore.iter_children(level1)
                while level2!=None:
                    path = self.treestore.get_path(level2)
                    self.treestore.row_changed(path, level2)
                    level2 = self.treestore.iter_next(level2)
                level1 = self.treestore.iter_next(level1)
            gtk.gdk.threads_leave()
            
            print '\n', _('Summary:'), '\n'
            if len(s_i):
                for o in s_i: print '\x1b[1;32m', _('Successfully installed:'), o.__doc__, '\x1b[m'
            if len(s_r):
                for o in s_r: print '\x1b[1;35m', _('Successfully removed:'), o.__doc__, '\x1b[m'
            if len(f_i):
                for tup in f_i:
                    print '\x1b[1;31m', _('Failed to install:'), tup[0].__doc__, '\x1b[m'
                    exc = tup[1]
                    print >>error_traceback, tup[0].__doc__
                    traceback.print_exception( exc[0], exc[1], exc[2], file=error_traceback) 
            if len(f_r):
                for tup in f_r: 
                    print '\x1b[1;31m', _('Failed to remove:'), tup[0].__doc__, '\x1b[m'
                    exc = tup[1]
                    print >>error_traceback, tup[0].__doc__
                    traceback.print_exception( exc[0], exc[1], exc[2], file=error_traceback)
            print 

            gtk.gdk.threads_enter()
            parentbox = self.terminal.get_widget().parent
            parentbox.pack_start(self.final_box, False)
            parentbox.show_all()
            if len(f_i) or len(f_r): #If any operation failed, we display "Report problems" dialog
                self.show_error(error_traceback.getvalue())
            gtk.gdk.threads_leave()
            
            delay_notify_firefox_restart(True)
            
            gtk.gdk.threads_enter()
            self.__show_detail('')
            self.treeview.get_selection().unselect_all()
            # self.__left_tree_view_default_select()
            gtk.gdk.threads_leave()
        except:
            print_traceback()
        finally:
            sys.stdout.flush()
            os.close(r)
            os.close(w)
            run.terminal = None
            os.dup2(self.backup_stdout, sys.stdout.fileno())

    def __return_to_app_view(self, *w):
        self.parentwindow.unlock()
        #change_content
        parentbox = self.terminal.get_widget().parent
        for child in parentbox.get_children():
            parentbox.remove(child)
        parentbox.add(self)
        parentbox.show_all()

    def __apply_button_clicked(self, widget):
        to_install = [ obj for obj in self.app_objs
                      if obj.cache_installed==False
                      and obj.showed_in_toggle ]
        to_remove = [ obj for obj in self.app_objs
                     if obj.cache_installed 
                     and obj.showed_in_toggle==False ]
        has_work = len(to_install) or len(to_remove)
        if not has_work: return
        if not self.__query_work(to_install, to_remove): return
        
        self.parentwindow.lock()
        import thread
        thread.start_new_thread(self.__apply_change_thread, () )
    
    def __sort_treestore ( self, model, iter1, iter2 ):
        obj1 = model.get_value ( iter1, 0 )
        obj2 = model.get_value ( iter2, 0 )
        import types
        assert isinstance ( obj1 , types.InstanceType )
        assert isinstance ( obj2 , types.InstanceType )        
        str1, str2 = obj1.__doc__, obj2.__doc__
        return cmp(str1, str2)

    def __toggle(self, render_toggle,path,treestore,treemodelsort,treestorefilter):
        path1 = treemodelsort.convert_path_to_child_path(path)
        path = treestorefilter.convert_path_to_child_path(path1)
        obj = treestore[path][0]
        import types
        assert isinstance(obj, types.InstanceType)
        assert hasattr(obj, 'showed_in_toggle')
        obj.showed_in_toggle = not obj.showed_in_toggle
        treestore.row_changed(path,  treestore.get_iter(path) )
        self.__show_detail(obj)

    def __toggle_cell_data_func ( self, column, cell, model, iter ):
        obj = model.get_value ( iter, 0 )
        import types
        assert isinstance ( obj, types.InstanceType )
        assert hasattr ( obj, 'showed_in_toggle' )
        cell.set_property ( 'active', obj.showed_in_toggle )

    def __text_cell_data_func ( self, column, cell, model, iter ):
        obj = model.get_value ( iter, 0 )
        import types
        assert isinstance ( obj, types.InstanceType )
        assert hasattr(obj, 'cache_installed') and hasattr(obj, 'showed_in_toggle')
        cell.set_property ( 'markup', '%s'%obj.__doc__ )
        cell.set_property ( 'strikethrough', 
                            obj.cache_installed==True and obj.showed_in_toggle==False )
        if obj.cache_installed==False and obj.showed_in_toggle==True :
            cell.set_property ( 'scale', 1.2 )
            cell.set_property ( 'underline', True )
        else :
            cell.set_property ( 'scale', 1 )
            cell.set_property ( 'underline', False )

    def __right_pane_changed(self, treeselection, treeview):
        ( store, pathlist ) = treeselection.get_selected_rows ()
        if pathlist == None or len(pathlist)==0: # select nothing 
            self.__show_detail('')
            return
        if len(pathlist)!=1: # select multi items 
            self.__show_detail('')
            return
        iter = store.get_iter( pathlist[0] )
        obj=store.get_value ( iter, 0 )
        import types
        assert isinstance(obj, types.InstanceType)
        assert hasattr(obj, 'cache_installed') and hasattr(obj, 'showed_in_toggle')
        self.__show_detail(obj)

    def __show_detail(self, obj):
        def begin_color():
            return '<span color="#870090">'
        
        def end_color():
            return '</span>'
        
        def color(string):
            return '%s%s%s'%( begin_color(), string, end_color() )

        if isinstance(obj, str) or isinstance(obj, unicode):
            self.detail.get_buffer().set_text(obj)
        else:
            import types
            assert isinstance(obj, types.InstanceType)
            assert hasattr(obj, 'cache_installed') and hasattr(obj, 'showed_in_toggle')
            
            import StringIO
            text = StringIO.StringIO()

            detail = getattr(obj, 'detail' ,'')
            if detail:
                text.write(detail)
                if detail[-1]!='\n': text.write('\n')
            
            license = getattr(obj, 'license' ,'')
            if license:
                print >>text, _('License:'), license   
            
            if obj.cache_installed==False: # can install
                # will be installed?
                if not obj.showed_in_toggle: 
                    print >>text, begin_color() + _('Not installed.'),
                    if hasattr(obj, 'get_reason'):
                        obj.get_reason(text)
                    text.write( end_color() )
                else:  
                    print >>text, color( _('Will be installed.') ),

            else: # already installed
                if obj.showed_in_toggle: print >>text, color(_('Installed.')), 
                else:                    print >>text, color(_('Will be removed.')), 
                        
            self.detail.get_buffer().set_text( text.getvalue() )
            text.close()

    def __visible_func(self, treestore, iter):
        import types
        assert isinstance(self.selected_categories, list)
        obj = treestore.get_value(iter, 0)
        if obj == None: return False
        assert isinstance(obj, types.InstanceType)
        assert hasattr(obj, 'category')
        
        is_right_category = obj.category in self.selected_categories
        if self.filter_text=='':
            return is_right_category
        else:
            def inside(p, str2):
                return p.search(str2) != None
            if self.filter_option=='name' or not hasattr(obj, 'detail'):
                return is_right_category and inside(self.filter_RE, obj.__doc__)
            else: # both
                return is_right_category and ( inside(self.filter_RE, obj.__doc__) or inside(self.filter_RE, obj.detail) )

    def __pixbuf_cell_data_func(self, column, cell, model, iter):
        class0 = model.get_value ( iter, 0 )
        cell.set_property('pixbuf', class0.logo_pixbuf)
        cell.set_property('visible', Config.get_show_software_icon())
        
    def __DE_pixbuf_cell_data_func(self, column, cell, model, iter):
        class0 = model.get_value ( iter, 0 )
        if hasattr(class0, 'DE'):
            if class0.DE == 'gnome':
                cell.set_property('pixbuf', self.DE_GNOME)
            elif class0.DE == 'kde':
                cell.set_property('pixbuf', self.DE_KDE)
        else:
            cell.set_property('pixbuf', self.DE_DEFAULT)
            
    def __launch_quick_setup(self, *w):
        self.parentwindow.lock()
        self.set_sensitive(False)
        def launch():
            import os
            me_path = os.path.dirname(os.path.abspath(__file__))
            with Chdir(me_path) as o:
                import subprocess
                task = subprocess.Popen(['python', 'ubuntu/quick_setup.py'])
                task.wait()
            gtk.gdk.threads_enter()
            self.app_class_installed_state_changed_by_external()
            self.parentwindow.unlock()
            self.set_sensitive(True)
            gtk.gdk.threads_leave()

        import thread
        thread.start_new_thread(launch, ())

    def __right_pane(self):
        import gobject
        self.treestore = treestore = gtk.TreeStore ( gobject.TYPE_PYOBJECT )
        
        self.treestorefilter = treestorefilter = treestore.filter_new()
        treestorefilter.set_visible_func( self.__visible_func )
        
        treemodelsort = gtk.TreeModelSort(treestorefilter)
        treemodelsort.set_sort_func ( 1000, self.__sort_treestore )
        treemodelsort.set_sort_column_id( 1000, gtk.SORT_ASCENDING )

        render_toggle = gtk.CellRendererToggle ()
        render_toggle.connect('toggled',self.__toggle,treestore, treemodelsort, treestorefilter)
        render_pixbuf = gtk.CellRendererPixbuf()
        render_DE_pixbuf = gtk.CellRendererPixbuf()
        render_text = gtk.CellRendererText ()

        col_toggle = gtk.TreeViewColumn ()
        col_toggle.pack_start (render_toggle,False)
        col_toggle.set_cell_data_func ( render_toggle, self.__toggle_cell_data_func )

        col_text = gtk.TreeViewColumn ()
        col_text.pack_start (render_pixbuf, False)
        col_text.set_cell_data_func ( render_pixbuf, self.__pixbuf_cell_data_func )
        col_text.pack_start (render_text, True)
        col_text.set_cell_data_func ( render_text, self.__text_cell_data_func )
        col_text.pack_end(render_DE_pixbuf, False)
        col_text.set_cell_data_func ( render_DE_pixbuf, self.__DE_pixbuf_cell_data_func )
        col_text.set_sort_column_id(1000)

        self.treeview = treeview = gtk.TreeView ( treemodelsort )
        treeview.append_column ( col_toggle )
        treeview.append_column ( col_text )
        treeview.set_rules_hint ( True )
        treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        treeview.get_selection().connect('changed', self.__right_pane_changed, treeview )

        def _all_shown_items():
            selection = treeview.get_selection()
            selection.select_all()
            model, pathlist = treeview.get_selection().get_selected_rows()
            selection.unselect_all()
            if pathlist == None:
                raise StopIteration
            for path in pathlist:
                obj = model[path][0]
                iter = model.get_iter(path)
                yield model, path, obj, iter, selection
        def select_all_items(widget):
            for model, path, obj, iter, selection in _all_shown_items():
                if not obj.showed_in_toggle:
                    obj.showed_in_toggle = True
                    model.row_changed(path, iter)
                    if obj.showed_in_toggle!= obj.cache_installed: 
                        selection.select_path(path)
        def select_no_item(widget):
            for model, path, obj, iter, selection in _all_shown_items():
                if obj.showed_in_toggle:
                    obj.showed_in_toggle = False
                    model.row_changed(path, iter)
                    if obj.showed_in_toggle!= obj.cache_installed: 
                        selection.select_path(path)
        def revert_all_items(widget):
            for model, path, obj, iter, selection in _all_shown_items():
                if obj.showed_in_toggle != obj.cache_installed:
                    obj.showed_in_toggle = obj.cache_installed
                    model.row_changed(path, iter)
                    if obj.showed_in_toggle!= obj.cache_installed: 
                        selection.select_path(path)
        select_all = image_stock_menuitem(gtk.STOCK_UNDERLINE, _('Select _All') )
        select_all.connect("activate", select_all_items )
        deselect_all = image_stock_menuitem(gtk.STOCK_STRIKETHROUGH, _('_Deselect All') )
        deselect_all.connect("activate", select_no_item )
        reset_all = image_stock_menuitem(gtk.STOCK_UNDO, _('_Reset All') )
        reset_all.connect("activate", revert_all_items )
        popupmenu = gtk.Menu()
        popupmenu.append(select_all)
        popupmenu.append(deselect_all)
        popupmenu.append(reset_all)
        popupmenu.show_all()
        def right_treeview_button_press_event(treeview, event):
            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
                popupmenu.popup(None, None, None, event.button, event.time)
                return True
            return False
        treeview.connect('button_press_event', right_treeview_button_press_event)
        
        scroll = gtk.ScrolledWindow()
        scroll.add(treeview)
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        
        from support.searchbox import SearchBoxForApp
        sbox = SearchBoxForApp()
        sbox.connect('changed', self.__search_content_changed)
        box1 = gtk.VBox(False, 10)
        box1.pack_start(sbox, False, False)
        box1.pack_start(scroll)
        
        from support.pangobuffer import PangoBuffer
        from support.releasenotesviewer import ReleaseNotesViewer
        detail = ReleaseNotesViewer( PangoBuffer() )
        detail.set_wrap_mode(gtk.WRAP_WORD)
        detail.set_editable(False)
        detail.set_cursor_visible(False)
        gray_bg(detail)
        self.detail = detail

        scroll_d = gtk.ScrolledWindow()
        scroll_d.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll_d.set_shadow_type(gtk.SHADOW_IN)
        scroll_d.add(detail)

        button_apply = image_stock_button(gtk.STOCK_APPLY, _('_Apply') )
        button_apply.connect('clicked', self.__apply_button_clicked)
        bottom_box = gtk.HBox(False, 10)
        bottom_box.pack_start(button_apply, False, False)

        box2 = gtk.VBox(False, 0)
        align = gtk.Alignment(0)
        align.add(gtk.Label( _('Details:') ))
        box2.pack_start(align , False, False)
        box2.pack_start(scroll_d, True, True, 5)
        box2.pack_start(bottom_box, False, False)

        self.vpaned = vpaned = gtk.VPaned()
        vpaned.pack1(box1, True, False)
        vpaned.pack2(box2, False, False)

        return vpaned 

    def __search_content_changed(self, widget, text, option):
        self.filter_text = text
        self.filter_option = option
        import re, locale, StringIO
        itext = self.filter_text.decode(locale.getpreferredencoding())
        otext = StringIO.StringIO()
        for char in itext:
            if char in r'.^$*+?{}[]\|()':
                otext.write('\\')
            otext.write(char)
        self.filter_RE = re.compile(otext.getvalue().encode(locale.getpreferredencoding()),
                                    re.IGNORECASE)
        self.treestorefilter.refilter()

    @classmethod
    def set_wget_parameters(cls):
        current_timeout = Config.wget_get_timeout()
        current_tries = Config.wget_get_triesnum()
        
        adjustment_timeout = gtk.Adjustment(current_timeout, 1, 60, 1, 1, 0)
        scale_timeout = gtk.HScale(adjustment_timeout)
        scale_timeout.set_digits(0)
        scale_timeout.set_value_pos(gtk.POS_BOTTOM)
        timeout_label = label_left_align(_('How long after the server does not respond, give up downloading? (in seconds)'))
        
        adjustment_tries = gtk.Adjustment(current_tries, 1, 20, 1, 1, 0)
        scale_tries = gtk.HScale(adjustment_tries)
        scale_tries.set_digits(0)
        scale_tries.set_value_pos(gtk.POS_BOTTOM)
        tries_label = label_left_align(_('How many times does Ailurus try to download the same resource?'))
        
        dialog = gtk.Dialog(
            _('Set Ailurus download parameter'), 
            None, gtk.DIALOG_MODAL|gtk.DIALOG_NO_SEPARATOR, 
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK) )
        dialog.set_border_width(5)
        dialog.vbox.pack_start(timeout_label, False)
        dialog.vbox.pack_start(scale_timeout, False)
        dialog.vbox.pack_start(tries_label, False)
        dialog.vbox.pack_start(scale_tries, False)
        dialog.vbox.show_all()
        ret = dialog.run()
        new_timeout = int(adjustment_timeout.get_value())
        new_tries = int(adjustment_tries.get_value())
        dialog.destroy()
        if ret == gtk.RESPONSE_OK:
            Config.wget_set_timeout(new_timeout)
            Config.wget_set_triesnum(new_tries)
    
    def get_preference_menuitems(self):
        show_quick_setup = gtk.MenuItem(_('Show "quickly install popular software" button'))
        show_quick_setup.connect('activate', lambda w: Config.set_hide_quick_setup_pane(False) or self.show_quick_setup())
    
        set_wget_param = gtk.MenuItem(_("Set download parameters"))
        set_wget_param.connect('activate', lambda w: self.set_wget_parameters())
        
        show_software_icon = gtk.CheckMenuItem(_('Show an icon by the side of software name'))
        show_software_icon.set_active(Config.get_show_software_icon())
        show_software_icon.connect('toggled', lambda w: Config.set_show_software_icon(w.get_active()) or self.treeview.queue_draw())
        
        if UBUNTU or MINT: # this feature only support UBUNTU or MINT.
            return [show_quick_setup, set_wget_param, show_software_icon]
        else:
            return [set_wget_param, show_software_icon]
    
    def hide_quick_setup(self):
        children = self.quick_setup_area.get_children()
        if children:
            for child in children:
                self.quick_setup_area.remove(child)
    
    def show_quick_setup(self):
        self.hide_quick_setup()
        self.quick_setup_area.pack_start(self.quick_setup_content, False)
        self.quick_setup_area.show_all()
    
    def __init__(self, parentwindow, app_objs):
        gtk.VBox.__init__(self, False, 0)
        self.detail = None # A gtk.Label which shows widget detail.
        self.treeview = None # A gtk.TreeView in right pane.
        self.treestore = None # A gtk.TreeStore behind self.treeview
        self.treestorefilter = None # A gtk.TreeModelFilter of self.treestore
        self.filter_text = ''
        self.filter_option = ''
        self.selected_categories = [ 'tweak' ] # Selected categories in the left pane
        self.app_objs = None # objs in self.treestore
        self.left_treeview = None # A gtk.TreeView in left pane.
        self.hpaned = hpaned = gtk.HPaned()
        self.vpaned = None
        assert hasattr(parentwindow, 'lock')
        assert hasattr(parentwindow, 'unlock')
        self.parentwindow = parentwindow
        from support.terminal import Terminal
        self.terminal = Terminal()
        self.DE_KDE = get_pixbuf(D + 'other_icons/kde.png', 24, 24)
        self.DE_GNOME = get_pixbuf(D + 'other_icons/gnome.png', 24, 24)
        self.DE_DEFAULT = get_pixbuf(D + 'other_icons/blank.png', 24, 24)

        self.final_box = gtk.VBox(False, 5)
        self.final_box.set_border_width(5)
        self._final_box_text = gtk.Label(_('All works finished. '))
        self._final_box_text.set_alignment(0, 0.5)
        self.final_box.pack_start( self._final_box_text, False )
        _close_button = image_stock_button( gtk.STOCK_CLOSE, _('Close this terminal') )
        _close_button.connect('clicked', self.__return_to_app_view )
        _hbox = gtk.HBox(False, 5)
        _hbox.pack_start(_close_button, False) 
        self.final_box.pack_start(_hbox, False)
        
        import os, sys
        self.backup_stdout = os.dup(sys.stdout.fileno())

        hpaned.pack1 ( self.__left_pane(), False, False )
        hpaned.pack2 ( self.__right_pane(), True, False )

        self.app_objs = app_objs
        for obj in app_objs :
            self.treestore.append ( None, [obj] )
        
        all_categories = set()
        for obj in app_objs :
            all_categories.add(obj.category)

        def icon(path):
            return get_pixbuf(path, 32, 32)
        
        treestore = self.left_treestore

        i_common = treestore.append(None, [_('Common'), None, '*common'])
        i_students = treestore.append(None, [_('For students'), None, '*students'])
        i_developers = treestore.append(None, [_('For developers'), None, '*developers'])
        i_advanced = treestore.append(None, [_('Advanced'), None, '*advanced'])
        
        items =  (
            [ i_common, _('Office'), D+'umut_icons/p_office.png', 'office' ] ,
            [ i_common, _('Education'), D+'umut_icons/p_education.png', 'education' ] ,
            [ i_common, _('Internet'), D+'umut_icons/p_internet.png', 'internet' ] ,
            [ i_common, _('Firefox extensions'), D+'umut_icons/p_firefox.png', 'firefox' ] ,
            [ i_common, _('Multimedia'), D+'umut_icons/p_multimedia.png', 'media' ] ,
            [ i_common, _('Appearance'), D+'umut_icons/p_appearance.png', 'appearance' ] ,
            [ i_common, _('Design'), D+'umut_icons/p_design.png', 'design' ] ,
            [ i_common, _('Enhancements'), D+'umut_icons/p_widgets.png', 'tweak' ] ,
            [ i_common, _('Game'), D+'umut_icons/p_game.png', 'game' ] ,
            [ i_common, _('Language support'), D+'other_icons/p_language_support.png', 'language'],
            [ i_common, _('Nautilus context menu'),  D+'other_icons/nautilus.png', 'nautilus'],

            [ i_advanced, _('Video card driver'), D+'umut_icons/p_video_card_driver.png', 'videocarddriver'],
            [ i_advanced, _('Third party repositories'), D+'umut_icons/p_repository.png', 'repository'],
            [ i_advanced, _('Virtual machine'), D+'umut_icons/p_virtualmachine.png', 'vm' ] ,
            [ i_advanced, _('Establish a server'), D+'umut_icons/p_server.png', 'server'],
            [ i_advanced, _('Hardware'), D+'umut_icons/p_hardware.png', 'hardware' ],
            
            [ i_students, _('Mathematics'), D+'umut_icons/p_math.png', 'math' ] ,
            [ i_students, _('Statistics'), D+'umut_icons/p_statistics.png', 'statistics' ],
            [ i_students, _('Biology'), D+'umut_icons/p_biology.png', 'biology' ],
            [ i_students, _('Electronics & Mechanics'), D+'umut_icons/p_em.png', 'em' ] ,
            [ i_students, _('Geography'), D+'umut_icons/p_geography.png', 'geography' ] ,
            [ i_students, _('LaTeX'), D+'umut_icons/p_latex.png', 'latex' ] ,
            [ i_students, _('Embedded system'),  D+'umut_icons/p_embedded_system.png', 'embedded' ],

            [ i_developers, _('Development'), D+'umut_icons/p_develop.png', 'dev' ] ,
            [ i_developers, _('Eclipse'), D+'umut_icons/eclipse.png', 'eclipse' ] ,
            [ i_developers, _('Firefox extensions'), D+'umut_icons/p_firefox.png', 'firefoxdev' ] ,
                )

        for item in items:
            parent, i1, i2, i3 = item
            if not i3 in all_categories: continue
            item = [i1, icon(i2), i3]
            treestore.append(parent, item)
        
        quick_setup_button = image_file_button(_('Quickly install popular software').center(60), D + 'umut_icons/quick_setup.png', 24)
        quick_setup_button.connect('clicked', self.__launch_quick_setup)
        quick_setup_checkbutton = gtk.CheckButton(_('Hide'))
        quick_setup_checkbutton.connect('clicked', lambda w: w.set_active(False) or Config.set_hide_quick_setup_pane(True) or self.hide_quick_setup())
        self.quick_setup_content = gtk.HBox(False, 10)
        self.quick_setup_content.set_border_width(5)
        self.quick_setup_content.pack_start(quick_setup_button, False)
        self.quick_setup_content.pack_start(quick_setup_checkbutton, False)
        self.quick_setup_area = gtk.HBox(False)
        if (UBUNTU or MINT) and not Config.get_hide_quick_setup_pane():
            self.show_quick_setup()
            
        self.__left_tree_view_default_select()

        self.pack_start(self.quick_setup_area, False)
        self.pack_start(hpaned)
        self.show_all()
