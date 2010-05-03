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

class GConfShortcutKeyEntry(gtk.HBox):
    def grab_key(self, *w):
        import support.keygrabber
        window = support.keygrabber.GrabberWindow ()
        window.main ()
        self.shortcut_entry.set_text(window.shortcut)

    def __entry_value_changed(self, *w):
        import gconf
        g = gconf.client_get_default()
        g.set_string('/apps/metacity/keybinding_commands/' + self.number, self.command_entry.get_text())
        g.set_string('/apps/metacity/global_keybindings/run_' + self.number, self.shortcut_entry.get_text())

    def __clear_entry_content(self, *w):        
        self.command_entry.set_text('')
        self.shortcut_entry.set_text('')
        
    def __init__(self, number):
        is_string_not_empty(number)
        gtk.HBox.__init__(self, False)
        
        import gconf
        g = gconf.client_get_default()

        self.number = number
        self.command_entry = gtk.Entry()
        self.command_entry.set_tooltip_text(
            _('The command which will be run.') + _('\nGConf key: ') + '/apps/metacity/keybinding_commands/' + self.number)
        value = g.get_string('/apps/metacity/keybinding_commands/'+number)
        if value: self.command_entry.set_text(value)
        self.command_entry.connect('changed', self.__entry_value_changed)

        self.shortcut_entry = gtk.Entry()
        self.shortcut_entry.set_tooltip_text(
            _('The shortcut key.') + _('\nGConf key: ') + '/apps/metacity/global_keybindings/run_' + self.number)
        self.shortcut_entry.connect('grab-focus', self.grab_key)
        value = g.get_string('/apps/metacity/global_keybindings/run_'+number)
        if value: self.shortcut_entry.set_text(value)
        self.shortcut_entry.connect('changed', self.__entry_value_changed)
        
        self.clear_entry_content_button = gtk.Button(stock = gtk.STOCK_CLEAR)
        self.clear_entry_content_button.connect('clicked', self.__clear_entry_content)

        self.pack_start(self.command_entry, True)
        self.pack_start(self.shortcut_entry, False)
        self.pack_start(self.clear_entry_content_button, False)

class ImageChooser(gtk.Button):
    import gobject
    __gsignals__ = {'changed':( gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_STRING,) ) }
    
    def get_image_filter(self):
        filter = gtk.FileFilter()
        filter.set_name(_("Images"))
        for type, pattern in [('image/png', '*.png'),
                              ('image/jpeg', '*.jpg'),
                              ('image/gif', '*.gif'),
                              ('image/x-xpixmap', '*.xpm'),
                              ('image/x-svg', '*.svg'),]:
            filter.add_mime_type(type)  
            filter.add_pattern(pattern)
        return filter
    
    def choose_image(self, *args):
        title = _('Choose an image')
        chooser = gtk.FileChooserDialog(title, None, gtk.FILE_CHOOSER_ACTION_OPEN,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                 gtk.STOCK_OPEN, gtk.RESPONSE_OK)
                )
        import os
        chooser.set_current_folder('/usr/share/pixmaps/')
        chooser.set_select_multiple(False)
        chooser.add_filter(self.get_image_filter())
        if chooser.run() == gtk.RESPONSE_OK:
            image_path = chooser.get_filename()
            self.emit('changed', image_path)
            self.display_image(image_path)
        chooser.destroy()
    
    def display_image(self, image_path):
        child = self.get_child()
        if child:
            self.remove(child)
        
        pixbuf = gtk.gdk.pixbuf_new_from_file(image_path)
        pixbuf = self.scale_pixbuf(pixbuf)
        image = gtk.image_new_from_pixbuf(pixbuf)
        self.add(image)
        self.show_all()

    def scale_pixbuf(self, pixbuf):
        pixbuf_height = pixbuf.get_height()
        pixbuf_width = pixbuf.get_width()
        if self.image_max_height != -1 and pixbuf_height > self.image_max_height:
            scale = float(pixbuf_height)/float(self.image_max_height)
            new_height = self.image_max_height
            new_width = pixbuf_width/scale
        elif self.image_max_width != -1 and pixbuf_width > self.image_max_width:
            scale = float(pixbuf_width)/float(self.image_max_width)
            new_width = self.image_max_width
            new_height = pixbuf_height/scale
        else:
            return pixbuf
        return pixbuf.scale_simple(int(new_width), int(new_height), gtk.gdk.INTERP_HYPER)

    def __init__(self, tooltip_text = '', image_max_width = -1, image_max_height = -1):
        is_string_not_empty(tooltip_text)
        assert isinstance(image_max_width, int)
        assert isinstance(image_max_height, int)
        
        gtk.Button.__init__(self)
        if tooltip_text: self.set_tooltip_text(tooltip_text)
        self.image_max_width = image_max_width
        self.image_max_height = image_max_height

        self.connect('clicked', self.choose_image)

    @classmethod
    def scale_image(cls, old_path, new_path, new_width, new_height):
        pixbuf = gtk.gdk.pixbuf_new_from_file(old_path)
        if pixbuf.get_width == new_width and pixbuf.get_height == new_height:
            pass
        else:
            pixbuf = pixbuf.scale_simple(new_width, new_height, gtk.gdk.INTERP_HYPER)
        pixbuf.save(new_path, 'png')

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
                  'nautilus', 'terminal', 'host_name',
                  'update', 'power', 'shortcut', 'firefox',]
    
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

class FirefoxConfig(gtk.CheckButton):
          
    def check_active(self):
        import os
        if not os.path.isfile(self.path + 'user.js'):
            return False
        else :
            with open(self.path + 'user.js') as f:
                v = f.readlines()
                for i in v:
                    if i == self.config_item:
                        return True
                return False

    def __init__(self, container, config_item, 
             plain_text, tooltip=None, ):
        import os
        self.path = os.path.expanduser('~/.mozilla/firefox/' + FirefoxExtensions.get_extensions_path().split('/')[5] + '/')
        gtk.CheckButton.__init__(self)
        assert isinstance(container, gtk.Container)
        self.__container = container
        assert isinstance(config_item, str)
        self.config_item = config_item
        assert isinstance(plain_text, (str,unicode))
        self.plain_text = plain_text
        self.label = gtk.Label(plain_text)
        self.add(self.label)
        self.tooltip = tooltip
        self.set_active(self.check_active())
        self.connect("query-tooltip", lambda *w: True)
