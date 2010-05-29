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
import sys, os
from lib import *
from libu import *
from libsetting import *

def __update_manager_setting():
    o = GConfCheckButton(_('Automatically check for update'), '/apps/update-notifier/auto_launch' )
    hbox = gtk.HBox(False, 10)
    hbox.pack_start( gtk.Label( _('Interval (in days) when to check for update:') ), False)
    e = GConfNumericEntry('/apps/update-notifier/regular_auto_launch_interval', 1, 30)
    hbox.pack_start(e, False)
    vbox = gtk.VBox(False, 0)
    vbox.pack_start(o, False)
    vbox.pack_start(hbox, False)
    return Setting(vbox, _('Ubuntu update manager setting'), ['update'])

def __reset_gconfig():
    reset_button = reset_gconfig_setting()
    return Setting(reset_button, _('Restore the Gnome Setting'), ['desktop'])

class reset_gconfig_setting(gtk.HBox):
        
    def text_data_func(self, column, cell, model, iter):
        keep = model.get_value(iter, 0)
        name = model.get_value(iter, 1)
        markup = '<b>%s</b> ' % (name)
        if not keep:
            markup += ' ' + _('will be removed')
        cell.set_property('markup', markup)

    def toggled(self, render_toggle, path):
        self.liststore[path][0] = not self.liststore[path][0]
        sensitive = False
        for row in self.liststore:
            keep = row[0]
            sensitive = sensitive or not keep
        self.button_delete.set_sensitive(sensitive)
    
    def refresh(self):
        import os
        self.liststore.clear()
        self.view.set_model(None)
        usr_list = os.listdir('/home')       
        if os.path.expanduser('~') == '/root':
            for row in usr_list:
                if (row != 'lost+found') & (os.path.exists('/home/'+row+'/.gconf')):
                    self.liststore.append([True, row])
                elif (row != 'lost+found') & (os.path.exists('/home/'+row+'/.gconf')):
                    self.liststore.append([False, row])
            self.view.set_model(self.liststore)
            self.view.set_sensitive(True)
            self.button_unselect_all.set_sensitive(True)
                    
        else:
            self.view.set_sensitive(False)
            self.liststore.append([True, _('You should login as root') ])
            self.view.set_model(self.liststore)
            self.button_delete.set_sensitive(False)
            self.button_unselect_all.set_sensitive(False)
            
    def unselect_all(self):
        for row in self.liststore:
            row[0] = False # do not keep
        self.button_delete.set_sensitive( bool(len(self.liststore)) )
    
    def delete_user_setting(self):
        to_delete = []
        for row in self.liststore:
            keep = row[0]
            name = row[1]
            if not keep: to_delete.append(name)
        if to_delete:
            try: 
                for name in to_delete:
                    run_as_root_in_terminal('rm /tmp/gconfd-'+name+' /tmp/orbit-'+name)
                    run_as_root_in_terminal('rm /home/'+name+'/.gnome* /home/'+name+'/.gconf* /home/'+name+'/.metacity /home/'+name+'/.nautilus -rf')
                notify(_('Reset Successful'), _('Setting will be applied when you login next time.'))
            except:
                print_traceback()
        self.refresh()
        
    def __init__(self):
        self.liststore = gtk.ListStore(bool, str)
        render_keep = gtk.CellRendererToggle()
        render_keep.connect('toggled', self.toggled)
        column_keep = gtk.TreeViewColumn()
        column_keep.pack_start(render_keep, False)
        column_keep.add_attribute(render_keep, 'active', 0)
        render_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn(_("Reset User's Gnome Settings"))
        column_text.pack_start(render_text, True)
        column_text.set_cell_data_func(render_text, self.text_data_func)
        self.view = view = gtk.TreeView(self.liststore)
        view.append_column(column_keep)
        view.append_column(column_text)
        view.set_rules_hint(True)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.add(view)
        
        button_refresh = gtk.Button(_('Refresh'))
        button_refresh.connect('clicked', lambda *w: self.refresh())
        self.button_unselect_all = button_unselect_all = gtk.Button(_('Select all'))
        button_unselect_all.connect('clicked', lambda *w: self.unselect_all())
        self.button_delete = button_delete = gtk.Button(_('Apply'))
        button_delete.connect('clicked', lambda *w: self.delete_user_setting())
        button_delete.set_tooltip_text(_('Remove the following files:\n'
                         '${HOME}/.gnome*'
                         '${HOME}/.gconf*\n'
                         '${HOME}/.metacity\n'
                         '${HOME}/.nautilus\n'
                         '/tmp/gconfd-${USER}\n'
                         '/tmp/orbit-${USER}'))
        button_box = gtk.VBox(False, 5)
        button_box.pack_start(button_refresh, False)
        button_box.pack_start(button_unselect_all, False)
        button_box.pack_start(button_delete, False)
        align = gtk.Alignment(0, 0.5)
        align.add(button_box)
        gtk.HBox.__init__(self, False, 10)
        self.pack_start(scroll)
        self.pack_start(align, False)
        view.set_sensitive(False)
        self.liststore.append([True, _('Please press the "Refresh" button.'),])
        button_unselect_all.set_sensitive(False)
        button_delete.set_sensitive(False)
        self.refresh()

def get():
    ret = []
    for f in [
            __update_manager_setting ,
            __reset_gconfig,
             ]:
        try:
            ret.append(f())
        except:
            print_traceback()
    return ret
