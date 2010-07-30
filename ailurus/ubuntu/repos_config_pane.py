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

class ReposConfigPane(gtk.VBox):
    icon = D+'sora_icons/m_repository_configure.png'
    text = _('Edit\nRepository')
    
    def __init__(self, main_view):
        gtk.VBox.__init__(self, False)
        
        self.treestore = treestore = gtk.TreeStore(gobject.TYPE_PYOBJECT, gobject.TYPE_STRING)
        self.treestore_filter = treestore_filter = treestore.filter_new()
        treestore_filter.set_visible_func(self.__treestore_item_visible_function)
        self.treeview = treeview = gtk.TreeView(treestore_filter)
        
        toggle_render = gtk.CellRendererToggle()
        toggle_render.set_property('activatable', True)
        toggle_render.connect('toggled',self.__repo_toggled, treestore_filter)
        toggle_column = gtk.TreeViewColumn()
        toggle_column.set_title(_('Enabled'))
        toggle_column.pack_start(toggle_render, False)
        toggle_column.set_cell_data_func(toggle_render, self.__repo_toggle_cell_function)
        
        text_render = gtk.CellRendererText()
        text_render.connect('edited', self.__repo_text_edited)
        text_column = gtk.TreeViewColumn()
        text_column.pack_start(text_render, False)
        text_column.set_cell_data_func(text_render, self.__repo_text_cell_function)
        
        treeview.append_column(toggle_column)
        treeview.append_column(text_column)
        treeview.set_rules_hint(True)
        self.__refresh_tree()
        
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.add(treeview)
        scrollwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrollwindow.set_shadow_type(gtk.SHADOW_IN)
        
        self.add_repos_area = add_repos_area = AddReposArea()
        self.add_debline_button = add_debline_button = image_stock_button(gtk.STOCK_ADD, _('Add'))
        add_debline_button.connect('clicked', self.__add_debline_button_clicked)
        add_debline_button_align = gtk.Alignment(0.5, 1)
        add_debline_button_align.add(add_debline_button) # put add_debline_button at right-bottom corner
        bottom_box = gtk.HBox(False, 10)
        bottom_box.set_border_width(5)
        bottom_box.pack_start(add_repos_area, True)
        bottom_box.pack_start(add_debline_button_align, False)
        
        self.treeview.expand_all()
        self.treeview.get_selection().select_path('0')
        
        def button_press_event(w, event):
            if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
                path = w.get_path_at_pos(int(event.x),int(event.y))
                selection = w.get_selection()
                if path:
                    selection.select_path(path[0])
                    #TODO
                    return True
            return False
        
        self.treeview.connect('button_press_event', button_press_event)

        self.pack_start(scrollwindow)
        self.pack_start(bottom_box, False)
    
    def __treestore_item_visible_function(self, treestore, iter):
        b = treestore.get_value(iter, 0)
        return b != None
    
    def __repo_toggle_cell_function(self, column, cell, model, iter):
        b = model.get_value(iter, 0)
        if b != None:
            cell.set_property('active', b)
    
    def __repo_text_cell_function(self, column, cell, model, iter):
        parent = model.iter_parent(iter)
        b = model.get_value(iter, 0)
        text = model.get_value(iter, 1)
        if parent == None:
            cell.set_property('markup', '<b><big>%s</big></b>' % text)
            cell.set_property('editable', False)
        elif b != None:
            cell.set_property('markup', self.__color_text(text, b))
            cell.set_property('editable', True)
    
    def __color_text(self, text, b):
        if not b:
            return '<span color="gray">%s</span>' % text
        
        words = text.split()
        if len(words) < 3:
            return text
        
        def check_deb(word):
            deb_heads = ['deb', 'deb-src']
            for deb_head in deb_heads:
                if word.startswith(deb_head):
                    return True
            return False
        
        def check_url(word):
            url_heads = ['http://', 'ftp://', 'https://', 'rstp://']
            for url_head in url_heads:
                if word.startswith(url_head):
                    return True
            return False
        
        if not check_deb(words[0]):
            return text
        if not check_url(words[1]):
            return text
        words[0] = '<span color="#6900B2">%s</span>' % words[0]
        words[1] = '<b><span color="red">%s</span></b>' % words[1]
        words[2] = '<span color="#007243">%s</span>' % words[2]
        for i in range(3, len(words)):
            words[i] = '<span color="blue">%s</span>' % words[i]
        return ' '.join(words)
    
    def __is_repos_enable(self, line):
        if len(line) <= 2:
            return None
        if line[0] == '#' and line[1:].strip().startswith('deb'):
            return False
        elif line.startswith('deb'):
            return True
        return None
    
    def __refresh_tree(self):
        import glob
        self.treestore.clear()
        for path in ['/etc/apt/sources.list'] + glob.glob('/etc/apt/sources.list.d/*'):
            if not path.endswith('.list'):
                continue
            parent = self.treestore.append(None, [True, path])
            with open(path, 'r') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                b = self.__is_repos_enable(line)
                if b == False:
                    line = line[1:].strip()
                self.treestore.append(parent, [b, line])
            self.__set_parent_toggle(parent)
        self.treestore_filter.refilter()
    
    def __apply(self):
        parent = self.treestore.get_iter_first()
        while parent:
            self.__apply_children(parent)
            parent = self.treestore.iter_next(parent)
    
    def __apply_children(self, parent):
        fn = self.treestore.get_value(parent, 1)
        lines = []
        child = self.treestore.iter_children(parent)
        while child:
            b = self.treestore.get_value(child, 0)
            text = self.treestore.get_value(child, 1)
            if b == False:
                line = '#' + text
            else:
                line = text
            lines.append(line)
            child = self.treestore.iter_next(child)
        with TempOwn(fn) as o:
            with open(fn, 'w') as f:
                f.write('\n'.join(lines))
    
    def __repo_toggled(self, cellrenderertoggle, path, treefilter):
        try:
            run_as_root('true')
            fiter = treefilter.get_iter_from_string(path)
            iter = treefilter.convert_iter_to_child_iter(fiter)
            parent = self.treestore.iter_parent(iter)
            
            b = self.treestore.get_value(iter, 0)
            if b == None:
                print >>sys.stderr, 'warning: b == None'
            b = not b
            
            if parent:
                self.__enable_repos(b, iter)
                self.__set_parent_toggle(parent)
            else:
                self.__enable_repos(b, iter)
                self.__set_children_toggle(iter, b)
            self.__apply()
        except AccessDeniedError:
            pass
    
    def __repo_text_edited(self, cellrenderertext, path, new_text):
        if self.treestore_filter[path][1] != new_text:
            try:
                run_as_root('true')
                fiter = self.treestore_filter.get_iter_from_string(path)
                iter = self.treestore_filter.convert_iter_to_child_iter(fiter)
                b = self.__is_repos_enable(new_text)
                if b == False:
                    new_text = new_text[1:]
                self.treestore.set_value(iter, 0, b)
                self.treestore.set_value(iter, 1, new_text)
                self.__apply()
                self.treestore_filter.refilter()
            except AccessDeniedError:
                pass
    
    def __add_debline_button_clicked(self, widget):
        text = self.add_repos_area.construct_debline_from_entries().strip()
        if not text:
            return
        b = self.__is_repos_enable(text)
        if b == None:
            msg = _(
                    'This is not a repository.\n' +
                    'Do you want to add it anymore ?'
                    )
            dlg = gtk.MessageDialog(buttons=gtk.BUTTONS_YES_NO,
                                    message_format=msg)
            re = dlg.run()
            dlg.destroy()
            if re == gtk.RESPONSE_NO:
                return
        try:
            run_as_root('true')
            selection = self.treeview.get_selection()
            model, fiter = selection.get_selected()
            iter = self.treestore_filter.convert_iter_to_child_iter(fiter)
            parent = self.treestore.iter_parent(iter)
            if b == False:
                text = text[1:].strip()
            if parent:
                self.treestore.insert_after(parent, iter, [b, text])
            else:
                self.treestore.append(iter, [b, text])
            self.add_repos_area.clear_entries()
            self.__apply()
            self.treestore_filter.refilter()
        except AccessDeniedError:
            pass
    
    def __set_parent_toggle(self, parent):
        fn = self.treestore.get_value(parent, 1)
        child = self.treestore.iter_children(parent)
        ret = None
        while child:
            b = self.treestore.get_value(child, 0)
            if b == False:
                ret = False
                break
            elif b == True:
                ret = True
            child = self.treestore.iter_next(child)
        self.__enable_repos(ret, parent)
    
    def __set_children_toggle(self, parent, b):
        child = self.treestore.iter_children(parent)
        while child:
            if self.treestore.get_value(child, 0) != None:
                self.__enable_repos(b, child)
            child = self.treestore.iter_next(child)
    
    def __enable_repos(self, b, iter):
        self.treestore.set_value(iter, 0, b)

class AddReposArea(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self, False)
        
        self.selected_box = None # self.selected_box is in [self.add_deb_line_box, self.add_PPA_repo_box]
        self.add_deb_line_box = gtk.HBox(False, 10)
        self.add_PPA_repo_box = gtk.HBox(False, 10)
        
        self.add_deb_line_box.entry = entry = gtk.Entry()
        self.add_deb_line_box.pack_start(entry)
        
        ppa_owner_label = gtk.Label(_('PPA owner:'))
        self.add_PPA_repo_box.ppa_owner_entry = ppa_owner_entry = gtk.Entry()
        ppa_name_label = gtk.Label(_('PPA name:'))
        self.add_PPA_repo_box.ppa_name_entry = ppa_name_entry = gtk.Entry()
        ppa_name_entry.set_text('ppa')
        self.add_PPA_repo_box.pack_start(ppa_owner_label, False)
        self.add_PPA_repo_box.pack_start(ppa_owner_entry)
        self.add_PPA_repo_box.pack_start(ppa_name_label, False)
        self.add_PPA_repo_box.pack_start(ppa_name_entry)
        
        self.box1 = gtk.VBox(False, 10)
        self.box1.pack_start(self.add_deb_line_box)
        self.box1.pack_start(self.add_PPA_repo_box)
        
        self.box2 = gtk.VBox(False, 10)
        def toggled(widget, index):
            self.__changed(index)
        radiobutton_deb = gtk.RadioButton(None, _('Add a line'))
        radiobutton_deb.connect('toggled', toggled, 0)
        radiobutton_ppa = gtk.RadioButton(radiobutton_deb, _('Add a PPA line'))
        radiobutton_ppa.connect('toggled', toggled, 1)
        radiobutton_deb.set_active(True)
        self.box2.pack_start(radiobutton_deb)
        self.box2.pack_start(radiobutton_ppa)
        
        self.pack_start(self.box1, True)
        self.pack_start(self.box2, False)
        
        self.__changed(0)
    
    def construct_debline_from_entries(self):
        if self.selected_box == self.add_deb_line_box:
            return self.add_deb_line_box.entry.get_text()
        elif self.selected_box == self.add_PPA_repo_box:
            user = self.add_PPA_repo_box.ppa_owner_entry.get_text()
            if not user:
                return ''
            ppa = self.add_PPA_repo_box.ppa_name_entry.get_text()
            if not ppa:
                return ''
            text = 'deb http://ppa.launchpad.net/%s/%s/ubuntu %s main' % (user, ppa, VERSION)
            return text
        
    def clear_entries(self):
        if self.selected_box == self.add_deb_line_box:
            self.add_deb_line_box.entry.set_text('')
        elif self.selected_box == self.add_PPA_repo_box:
            self.add_PPA_repo_box.ppa_owner_entry.set_text('')
            self.add_PPA_repo_box.ppa_name_entry.set_text('')
    
    def __changed(self, index):
        if index == 0:
            self.selected_box = self.add_deb_line_box
            self.add_deb_line_box.set_sensitive(True)
            self.add_PPA_repo_box.set_sensitive(False)
        elif index == 1:
            self.selected_box = self.add_PPA_repo_box
            self.add_deb_line_box.set_sensitive(False)
            self.add_PPA_repo_box.set_sensitive(True)
