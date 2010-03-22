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
from libu import *

class GConfCheckButton(gtk.CheckButton):
    def __toggled(self, w):
        value = self.get_active()
        import gconf
        g = gconf.client_get_default()
        g.set_bool(self.key, value)
    def __init__(self, text, key, tooltip = None):
        gtk.CheckButton.__init__(self)
        self.key = key
        self.set_label(text)
        if not tooltip: tooltip = _('GConf key: ')+key
        else: tooltip += _('\nGConf key: ')+key
        self.set_tooltip_markup(tooltip)
        import gconf
        g = gconf.client_get_default()
        self.set_active( g.get_bool(key) )
        self.connect('toggled', self.__toggled)

class GConfComboBox(gtk.HBox):
    def __init__(self, key, values_shown, values_gconf, tooltip = None):
        gtk.HBox.__init__(self, False, 10)
        
        self.key = key
        self.values_gconf = values_gconf
        
        combo = gtk.combo_box_new_text()
        if not tooltip: tooltip = _('GConf key: ')+key
        else: tooltip += _('\nGConf key: ')+key
        combo.set_tooltip_text(tooltip)
        for s in values_shown:
            combo.append_text(s)
        import gconf
        g = gconf.client_get_default()
        value = g.get_string(key)
        for i, s in enumerate(values_gconf):
            if s==value:
                combo.set_active(i)
                break
        combo.connect('changed', self.__option_changed)
        combo.connect('scroll-event', lambda *w:True)
        self.pack_start(combo, False, False)
    def __option_changed(self, combo):
        value = self.values_gconf[ combo.get_active() ]
        import gconf
        g = gconf.client_get_default()
        g.set_string(self.key, value)

class GConfTextEntry(gtk.HBox):
    def __value_changed(self, *w): 
        self.button.set_sensitive(True)
        
    def __button_clicked(self, *w):
        value = self.entry.get_text()
        import gconf
        g = gconf.client_get_default()
        g.set_string(self.key, value)
        self.button.set_sensitive(False)
    
    def __init__(self, key):
        self.key = key
        self.entry = gtk.Entry()    
        import gconf
        g = gconf.client_get_default()
        value = g.get_string(key)
        if value: self.entry.set_text(value) 
        
        self.button = gtk.Button(stock=gtk.STOCK_APPLY)
        self.button.set_sensitive(False)
        self.entry.connect('changed', self.__value_changed)
        self.button.connect('clicked', self.__button_clicked)
        
        tooltip_text = _('GConf key: ') + key
        self.entry.set_tooltip_text(tooltip_text)
        self.button.set_tooltip_text(tooltip_text)
        
        gtk.HBox.__init__(self, False, 5)
        self.pack_start(self.entry, False)
        self.pack_start(self.button, False)

class GConfImageEntry(gtk.HBox):
    def __choose_file(self,w):
        title = _('Choose a file for "%s" ')%self.text
        chooser = gtk.FileChooserDialog(title, None, gtk.FILE_CHOOSER_ACTION_OPEN,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                 gtk.STOCK_OPEN, gtk.RESPONSE_OK)
                )
        path = self.entry.get_text()
        import os
        if path: chooser.set_current_folder( os.path.dirname(path) )
        else:     chooser.set_current_folder( os.environ['HOME'] )
        
        chooser.set_select_multiple(False)

        filter = gtk.FileFilter()
        filter.set_name( _("Image file") )
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_mime_type("image/x-xpixmap")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.xpm")
        
        chooser.add_filter(filter)

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            self.image = chooser.get_filename()
            pixbuf = gtk.gdk.pixbuf_new_from_file(self.image)
            pixbuf = pixbuf.scale_simple(24, 24, gtk.gdk.INTERP_HYPER)
            pixbuf.save(self.image, 'png')
            self.__change_entry_content(self.image)
        chooser.destroy()
    def __apply(self,w):
        import os
        self.path = os.path.expanduser('~/.icons/%s/24x24/places/' % self.icon_theme)
        run('mkdir -p ' + self.path)
        run('cp %s %s/start-here.png' % (self.image, self.path))
        notify( _('Changed'), _('Application will work next time you restart your computer'))
        self.button2.set_sensitive(False)
    def __change_entry_content(self,path):
        self.entry.set_text('%s' %path)
        
    def __init__(self, text, key, path =''):
        gtk.HBox.__init__(self, False, 3)
        import gconf
        g = gconf.client_get_default()
        self.icon_theme = g.get_string(key)
        self.label = gtk.Label(text)
        self.text = text
        self.entry = gtk.Entry()
        self.entry.set_size_request(400,30)
        self.entry.set_editable(False)
        self.__change_entry_content(self.path)
        button1 = gtk.Button( _('Change'))
        button2 = self.button2 = gtk.Button( _('Apply'))
        button1.connect('clicked',self.__choose_file)
        button2.connect('clicked',self. __apply)

        self.pack_start(self.label,False)
        self.pack_start(self.entry,False)
        self.pack_start(button1,False)
        self.pack_start(button2,False)     
        
class GConfFileEntry(gtk.HBox):
    def __choose_file(self, w):
        title = _('Choose a file for "%s" ')%self.text
        chooser = gtk.FileChooserDialog(
            title, None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
             gtk.STOCK_OPEN,gtk.RESPONSE_OK)
            )
        
        path = self.entry.get_text()
        import os
        if path: chooser.set_current_folder( os.path.dirname(path) )
        else:     chooser.set_current_folder( os.environ['HOME'] )
        
        chooser.set_select_multiple(False)

        filter = gtk.FileFilter()
        filter.set_name( _("Image file") )
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_mime_type("image/x-xpixmap")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.xpm")
        
        chooser.add_filter(filter)

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            path = chooser.get_filename()
            import gconf
            g = gconf.client_get_default()
            g.set_string(self.key, path)
            self.__change_entry_content(path)
        chooser.destroy()
    def __change_entry_content(self, path):
        self.entry.set_text(path)
        self.entry.set_tooltip_text( self.tooltip+_('\nFile: ')+path )
    def __init__(self, text, key, tooltip='', show_label=True):
        gtk.HBox.__init__(self, False, 3)

        tooltip += _('\nGConf key: ')+key
        self.tooltip = tooltip
        
        self.text = text
        self.key = key
        
        self.entry = entry = gtk.Entry()
        entry.set_editable(False)
        gray_bg(self.entry)
        import gconf
        g = gconf.client_get_default()
        path = g.get_string(key)
        self.__change_entry_content(path)
        
        button = gtk.Button( _('Change') )
        button.connect('clicked', self.__choose_file)
        button.set_tooltip_text(tooltip)

        label = gtk.Label('%s '%text)
        label.set_tooltip_text(tooltip)
        if show_label: self.pack_start( label, False )
        self.pack_start( self.entry )
        self.pack_start( button, False )

class GConfNumericEntry(gtk.HBox):
    def __value_changed(self, *w):
        self.button_apply.set_sensitive(True)
    def __apply(self, *w):
        value = self.spin.get_value_as_int()
        import gconf
        g = gconf.client_get_default()
        g.set_int(self.key, value)
        self.button_apply.set_sensitive(False)
    def __init__(self, key, min, max, tooltip=''):
        self.key = key
        
        if tooltip: tooltip+='\n'
        tooltip += _('GConf key: ')+key
        tooltip += _('\nMinimum value: %(min)s. Maximum value: %(max)s.')%{'min':min, 'max':max}
        
        self.spin = spin = gtk.SpinButton()
        spin.set_size_request(100, -1)
        spin.set_range(min, max)
        spin.set_increments(1, 1)
        spin.set_update_policy(gtk.UPDATE_ALWAYS)
        spin.set_numeric(True)
        spin.set_tooltip_text(tooltip)
        spin.set_wrap(False)
        spin.set_snap_to_ticks(True)
        import gconf
        g = gconf.client_get_default()
        value = g.get_int(key)
        spin.set_value(value)
        spin.connect('value-changed', self.__value_changed)
        spin.connect('scroll-event', lambda *w:True)

        self.button_apply = button_apply = gtk.Button( _('Apply') )
        button_apply.set_sensitive(False)
        button_apply.connect('clicked', self.__apply)
        
        gtk.HBox.__init__(self, False, 5)
        self.pack_start(spin, False)
        self.pack_start(button_apply, False)

class GConfHScale(gtk.HScale):
    def __init__(self, gconf_key, min, max, tooltip = ''):
        self.gconf_key = gconf_key
        
        if tooltip: tooltip += '\n'
        tooltip += _('GConf key: ') + gconf_key
        
        gtk.HScale.__init__(self)
        self.set_value_pos(gtk.POS_RIGHT)
        self.set_digits(0)
        self.set_range(min, max)
        import gconf
        g = gconf.client_get_default()
        value = g.get_int(self.gconf_key)
        self.set_value(value)
        self.connect("value-changed", self.__value_changed)
        if tooltip: self.set_tooltip_text(tooltip)
        
    def __value_changed(self, *w):
        new_value = int( self.get_value() )
        import gconf
        g = gconf.client_get_default()
        g.set_int(self.gconf_key, new_value)
        
import gtk
class Setting(gtk.VBox):
    categories = [
                  'all',
                  'desktop', 'window', 'menu', 
                  'sound', 'icon', 'font', 'session', 
                  'memory', 'network',
                  'restriction',
                  'nautilus', 'terminal', 
                  'update', 'power', ]
    
    def __title(self, text):
        label = gtk.Label()
        label.set_markup('<b>%s</b>'%text)
        return left_align(label)

    def __init__(self, box, title, category):
        assert isinstance(box, gtk.Container)
        assert isinstance(title, (str, unicode) )
        assert isinstance(category, list)
        assert category != []
        for i in category: 
            assert isinstance(i, str)
            assert i in self.categories

        gtk.VBox.__init__(self, False, 0)
        self.set_border_width(5)
        self.pack_start( self.__title(title), False )
        self.pack_start( box, False)
        box.set_border_width(5)
        
        self.category = category

if __name__ == '__main__':
    pixbuf = gtk.gdk.pixbuf_new_from_file('')
    pixbuf = pixbuf.scale_simple(24, 24, gtk.gdk.INTERP_HYPER)
    