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
import gobject
import sys
import os
from lib import *
from libu import *

class ReposConfigPane(gtk.VBox):
    icon = D+'sora_icons/m_repository_configure.png'
    text = _('Repository\nConfigure')
    
    def __init__(self, main_view):
        gtk.VBox.__init__(self, False)
        self.main_view = main_view
        
        self.treestore = treestore = gtk.TreeStore(gobject.TYPE_PYOBJECT, gobject.TYPE_STRING)
        self.treefilter = treefilter = treestore.filter_new()
        treefilter.set_visible_func(self.__visible_func)
        self.treeview = treeview = gtk.TreeView(treefilter)
        
        toggle_render = gtk.CellRendererToggle()
        toggle_render.set_property('activatable', True)
        toggle_render.connect('toggled',self.__toggled, treefilter)
        toggle_column = gtk.TreeViewColumn()
        toggle_column.set_title(_('Enabled'))
        toggle_column.pack_start(toggle_render, False)
        toggle_column.set_cell_data_func(toggle_render, self.__toggle_cell_func)
        
        text_render = gtk.CellRendererText()
        text_render.connect('edited', self.__edited)
        text_column = gtk.TreeViewColumn()
        text_column.set_title(_('Repository'))
        text_column.pack_start(text_render, False)
        text_column.set_cell_data_func(text_render, self.__text_cell_func)
        
        treeview.append_column(toggle_column)
        treeview.append_column(text_column)
        treeview.set_rules_hint(True)
        self.__refresh_tree()
        
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.add(treeview)
        scrollwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrollwindow.set_shadow_type(gtk.SHADOW_IN)
        self.addArea = addArea = AddReposArea()
        self.add_btn = add_btn = image_stock_button(gtk.STOCK_ADD, _('Add'))
        add_btn.connect('clicked', self.__add_repos)
        buttom_box = gtk.HBox(False, 10)
        buttom_box.set_border_width(2)
        buttom_box.pack_start(addArea, True)
        add_btn_box = gtk.VBox()
        add_btn_box.pack_end(add_btn, False)
        buttom_box.pack_end(add_btn_box, False)
        
        self.treeview.expand_all()
        fiter_first = self.treefilter.get_iter_first()
        self.treeview.get_selection().select_iter(fiter_first)
        
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
        self.pack_start(buttom_box, False)
    
    def __visible_func(self, treestore, iter):
        b = treestore.get_value(iter, 0)
        return b != None
    
    def __toggle_cell_func(self, column, cell, model, iter):
        b = model.get_value(iter, 0)
        if b != None:
            cell.set_property('active', b)
    
    def __text_cell_func(self, column, cell, model, iter):
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
        self.treefilter.refilter()
    
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
    
    def __toggled(self, cellrenderertoggle, path, treefilter):
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
    
    def __edited(self, cellrenderertext, path, new_text):
        if self.treefilter[path][1] != new_text:
            try:
                run_as_root('true')
                fiter = self.treefilter.get_iter_from_string(path)
                iter = self.treefilter.convert_iter_to_child_iter(fiter)
                b = self.__is_repos_enable(new_text)
                if b == False:
                    new_text = new_text[1:]
                self.treestore.set_value(iter, 0, b)
                self.treestore.set_value(iter, 1, new_text)
                self.__apply()
                self.treefilter.refilter()
            except AccessDeniedError:
                pass
    
    def __add_repos(self, widget):
        text = self.addArea.getRepos().strip()
        if not text:
            return
        b = self.__is_repos_enable(text)
        if b == None:
            msg = _(
                    'This is not a repository.\n' +
                    'Do you want to add it anymore ?'
                    )
            dlg = gtk.MessageDialog(parent=self.main_view.window,
                                    buttons=gtk.BUTTONS_YES_NO,
                                    message_format=msg)
            re = dlg.run()
            dlg.destroy()
            if re == gtk.RESPONSE_NO:
                return
        try:
            run_as_root('true')
            selection = self.treeview.get_selection()
            model, fiter = selection.get_selected()
            iter = self.treefilter.convert_iter_to_child_iter(fiter)
            parent = self.treestore.iter_parent(iter)
            if b == False:
                text = text[1:].strip()
            if parent:
                self.treestore.insert_after(parent, iter, [b, text])
            else:
                self.treestore.append(iter, [b, text])
            self.addArea.clearContent()
            self.__apply()
            self.treefilter.refilter()
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
        
        self.currentBox = None
        self.officialBox = gtk.HBox(False, 10)
        self.thirdPartyBox = gtk.HBox(False, 10)
        
        self.officialBox.entry = entry = gtk.Entry()
        self.officialBox.pack_start(entry)
        
        userlabel = gtk.Label(_('user:'))
        self.thirdPartyBox.userentry = userentry = gtk.Entry()
        ppalabel = gtk.Label(_('ppa:'))
        self.thirdPartyBox.ppaentry = ppaentry = gtk.Entry()
        ppaentry.set_text('ppa')
        self.thirdPartyBox.pack_start(userlabel, False)
        self.thirdPartyBox.pack_start(userentry)
        self.thirdPartyBox.pack_start(ppalabel, False)
        self.thirdPartyBox.pack_start(ppaentry)
        
        self.textBox = gtk.VBox(False, 10)
        self.textBox.pack_start(self.officialBox)
        self.textBox.pack_start(self.thirdPartyBox)
        
        self.rbBox = gtk.VBox(False, 10)
        def toggled(widget, index):
            self.__changed(index)
        official_btn = gtk.RadioButton(None, _('Official'))
        official_btn.connect('toggled', toggled, 0)
        thirdparty_btn = gtk.RadioButton(official_btn, _('Third Party'))
        thirdparty_btn.connect('toggled', toggled, 1)
        official_btn.set_active(True)
        self.rbBox.pack_start(official_btn)
        self.rbBox.pack_start(thirdparty_btn)
        
        self.pack_start(self.textBox, True)
        self.pack_end(self.rbBox, False)
        
        self.__changed(0)
    
    def getRepos(self):
        if self.currentBox == self.officialBox:
            return self.officialBox.entry.get_text()
        elif self.currentBox == self.thirdPartyBox:
            user = self.thirdPartyBox.userentry.get_text()
            if not user:
                return ''
            ppa = self.thirdPartyBox.ppaentry.get_text()
            if not ppa:
                return ''
            text = 'deb http://ppa.launchpad.net/%s/%s/ubuntu %s main' % (user, ppa, self.__get_ubuntu_version())
            return text
        
    def clearContent(self):
        if self.currentBox == self.officialBox:
            self.__clear_offciial()
        elif self.currentBox == self.thirdPartyBox:
            self.__clear_thirdparty()
    
    def __changed(self, index):
        if index == 0:
            self.__set_current_box(self.officialBox)
            self.officialBox.set_sensitive(True)
            self.thirdPartyBox.set_sensitive(False)
        elif index == 1:
            self.__set_current_box(self.thirdPartyBox)
            self.thirdPartyBox.set_sensitive(True)
            self.officialBox.set_sensitive(False)
    
    def __set_current_box(self, box):
        self.currentBox = box
    
    def __clear_offciial(self):
        self.officialBox.entry.set_text('')
    
    def __clear_thirdparty(self):
        self.thirdPartyBox.userentry.set_text('')
    
    def __get_ubuntu_version(self):
        return Config.get_Ubuntu_version()