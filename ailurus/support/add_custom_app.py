#-*- coding: utf-8 -*-
#
# Ailurus - make Linux easier to use
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
import pango

from lib import *
from libu import *
from loader import *
from libapp import *
from libsetting import *
    
class AddCustomAppDialog(gtk.Dialog):
    liststore_all_pkg = gtk.ListStore(str)

    def clear(self):
        self.entry_detail.set_text('')
        self.entry_name.set_text('')
        self.entry_pkg.set_text('')
        self.entry_pkgs.set_text('')

    def __prompt(self, title, content):
        dialog = gtk.Dialog(title = title,
                            buttons = (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(gtk.Label(content))
        dialog.vbox.show_all()
        dialog.run()
        dialog.destroy()

    def __cancel(self, widget):
        self.response(gtk.RESPONSE_REJECT)

    def __get_category(self):
        s = self.combo_category.get_active_text()
        for c in Category.all():
            if c.text == s:
                return c.category
        return 'Other'   

    def __submit(self, button):
        dict={}
        if self.dict.has_key('appname'):
            dict['appname'] = self.dict['appname']
        else:
            dict['appname'] = 'C_%d' % Config.get_custom_app_count()
            Config.increase_custom_app_count()
        if getattr(self, 'new_icon_path', ''):
            pixbuf = gtk.gdk.pixbuf_new_from_file(self.new_icon_path)
            pixbuf.save(Config.get_config_dir() + '%s.png' % dict['appname'], 'png')
            if self.dict.has_key('appname'):
                obj = self.dict['appobj']
                obj.logo_pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.new_icon_path, 32, 32)
        dict['__doc__'] = self.entry_name.get_text()
        dict['detail'] = self.entry_detail.get_text()
        
        desktop_env = DISTRIBUTION
        dict[desktop_env] = self.entry_pkgs.get_text()
        if dict[desktop_env] == '':
            self.__prompt(_('Oops'), _('Package name should not be empty!'))
            return
        if dict['__doc__'] == '':
            self.__prompt(_('Oops'), _('Application name should not be empty!'))
            return
        try:
            
            if not self.dict.has_key('appname'):
                dict['category'] = self.__get_category()
                AppObjs.add_new_appobj(dict)
            else:                    
                dict['category'] = self.dict['category'].replace(self.origin_category, self.__get_category())
                obj = self.dict['appobj']
                obj.__doc__ = dict['__doc__']
                obj.detail = dict['detail']
                obj.category = dict['category']
                obj.pkgs = dict[DISTRIBUTION]
                obj.self_check()
                obj.fill()
            CUSTOM_APPS.addAppObjFromDict(dict)
        except:
            print_traceback()
        self.response(gtk.RESPONSE_ACCEPT)
        
    def __add_pkg(self, button, entry_pkgs_to_install, entry):
        new_pkg = entry.get_text()
        if new_pkg:
            if not new_pkg in entry_pkgs_to_install.get_text().split():
                if new_pkg in BACKEND.get_existing_pkgs_set():
                    entry_pkgs_to_install.set_text(entry_pkgs_to_install.get_text()+entry.get_text()+' ')
                    entry.set_text('')
                else:
                    self.__prompt(_('Oops'), _('Package is not contained by repository!'))
                    entry.set_text('')
                    return
            else:
                self.__prompt(_('Oops'), _('Package name already in list!'))
                entry.set_text('')
                return
        
    def __pkgname_callback(self, entry):
        self.__add_pkg(None, self.entry_pkgs, self.entry_pkg)
    
    def __choose_icon(self, widget, new_path):
        self.new_icon_path = new_path
        
    def __init__(self, dict={}):
        gtk.Dialog.__init__(self,
                            title=_('Edit custom application'),
                            flags=gtk.DIALOG_MODAL|gtk.DIALOG_NO_SEPARATOR)
        self.dict = dict
        self.set_position(gtk.WIN_POS_CENTER)
        label_name = gtk.Label(_('Name:'))
        label_name.set_alignment(0, 0.5)
        label_pkgs_to_install = gtk.Label(_('Packages to install:'))
        label_pkgs_to_install.set_alignment(0, 0.5)
        label_add_pkg_to_list = gtk.Label(_('Add package to list:'))
        label_add_pkg_to_list.set_alignment(0,0.5)
        self.entry_pkgs = entry_pkgs = gtk.Entry()
        if dict.has_key(DISTRIBUTION):
            entry_pkgs.set_text(dict[DISTRIBUTION] + ' ')
        label_detail = gtk.Label(_('Detail:'))
        label_detail.set_alignment(0,0.5)
        label_category = gtk.Label(_('Category:'))
        label_category.set_alignment(0,0.5)
        self.entry_name = entry_name = gtk.Entry()
        if dict.has_key('__doc__'):
            entry_name.set_text(dict['__doc__'])
        entry_name.set_max_length(50)
        self.entry_pkg = entry_pkg = gtk.Entry()
        pkg_completion = gtk.EntryCompletion()
        entry_pkg.set_completion(pkg_completion)
        if len(self.liststore_all_pkg) == 0:
            for pkg in BACKEND.get_existing_pkgs_set():
                self.liststore_all_pkg.append([pkg])
        liststore_pkgs = self.liststore_all_pkg
        pkg_completion.set_model(liststore_pkgs)
        pkg_completion.set_text_column(0)
        pkg_completion.set_minimum_key_length(3)

        entry_pkg.connect("activate",self.__pkgname_callback)
       
        button_add_pkg = stock_image_only_button(gtk.STOCK_ADD)
        button_add_pkg.connect("clicked",self.__add_pkg,self.entry_pkgs,entry_pkg)
        self.entry_detail = entry_detail = gtk.Entry()
        entry_detail.set_max_length(50)
        if dict.has_key('detail'):
            entry_detail.set_text(dict['detail'])
        
        button_submit = image_stock_button(gtk.STOCK_APPLY, _('Submit'))
        button_submit.connect('clicked', self.__submit)
        button_cancel = image_stock_button(gtk.STOCK_CANCEL, _('Cancel'))
        button_cancel.connect('clicked', self.__cancel)

        table = gtk.Table(False)
        table.set_col_spacings(10)
        table.set_row_spacings(5)
        table.attach(label_name, 0, 1, 0, 1, gtk.FILL, 0)
        table.attach(label_detail, 0, 1, 1, 2, gtk.FILL, 0)
        table.attach(entry_name, 1, 2, 0, 1, gtk.FILL, 0)
        table.attach(entry_detail, 1, 2, 1, 2, gtk.FILL, 0)
        hbox_bottom = gtk.HBox(False, 10)
        hbox_bottom.pack_end(button_cancel, False)
        hbox_bottom.pack_end(button_submit, False)
        
        self.combo_category = combo_category = gtk.combo_box_entry_new_text()
        index = 0
        target = ''
        if dict.has_key('category'):
            target = dict['category']
        
        for i in range(0,len(Category.all())):
            c = Category.all()[i]
            if len(target.split()) == 1:
                if c.category == target:
                    index = i
                
            else:
                if c.category in target.split() and not c.category in ['favourite','dustbin']:
                    index = i
            combo_category.append_text(c.text)
        
        combo_category.set_active(index)
        
        hbox_add_pkg = gtk.HBox()
        hbox_add_pkg.set_homogeneous(False)

        hbox_add_pkg.pack_start(entry_pkg, False, False, 0)
        hbox_add_pkg.pack_start(button_add_pkg, False, False, 0)
        table.attach(label_pkgs_to_install, 0, 1, 2, 3, gtk.FILL, 0)
        table.attach(entry_pkgs, 1, 2, 2, 3, gtk.FILL, 0)
        table.attach(label_category, 0, 1, 4, 5, gtk.FILL, 0)
        table.attach(combo_category, 1, 2, 4, 5, gtk.FILL, 0)
        table.attach(label_add_pkg_to_list, 0, 1, 3, 4, gtk.FILL, 0)
        table.attach(hbox_add_pkg, 1, 2, 3, 4, gtk.FILL, 0)
        table.set_homogeneous(False)
        
        self.icon_chooser = icon_chooser = ImageChooser('/usr/share/pixmaps/', 48, 48)
        icon_chooser.connect('changed',self.__choose_icon)
        if self.dict.has_key('appname'):       
            pixbuf = self.dict['appobj'].logo_pixbuf
        else:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(D + 'sora_icons/default_application_icon.png', 48, 48)
        icon_chooser.display_pixbuf(pixbuf)
        hbox_icon_and_table = gtk.HBox()
        tmp_vbox = gtk.VBox()
        tmp_vbox.pack_start(icon_chooser, False, False, 0)
        hbox_icon_and_table.set_homogeneous(False)
        hbox_icon_and_table.pack_start(tmp_vbox, False, False, 0)
        hbox_icon_and_table.pack_start(table, False, False, 0)
        self.vbox.pack_start(hbox_icon_and_table, False, False, 0)
        self.vbox.pack_end(hbox_bottom, False, False, 0)
        
        self.origin_category = self.__get_category()
