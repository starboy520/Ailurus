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
from ulib import *
from settinglib import *

def audio_convert_pre():
    to_install = []
    for p in ['lame', 'vobis-tools', 'libid3-3.8.3-dev', 'flac', 'faac', 'faad', 'mppenc' ]:
        if APT.exist(p) and APT.installed(p)==False:
            to_install.append(p)
    if to_install:
        APT.install(*to_install)

def audio_convert_post():
    run('nautilus-script-manager enable ConvertAudioFile')

def collection_svn_post():
    run('nautilus-script-manager enable Subversion')

class InstallPackageCheckButton(gtk.CheckButton):
    import gobject
    __gsignals__ = {'changed':( gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, () ) }
    def __toggled(self, w):
        if self.installed==False and self.get_active():
            self.label.set_markup("<big>%s</big>"%self.plain_text)
        elif self.installed and not self.get_active():
            self.label.set_markup("<s>%s</s>"%self.plain_text)
        else:
            self.label.set_markup(self.plain_text)
        self.emit('changed')

    def __init__(self, apt_package_name, 
             plain_text, tooltip=None, pre_install = None, post_install = None):
        gtk.CheckButton.__init__(self)
        assert isinstance(apt_package_name, str)
        self.apt_package_name = apt_package_name
        assert isinstance(plain_text, (str,unicode))
        self.plain_text = plain_text
        self.label = gtk.Label(plain_text)
        self.add(self.label)
        if pre_install: 
            assert callable(pre_install)
            assert 'pre' in pre_install.__name__
        if post_install: 
            assert callable(post_install)
            assert 'post' in post_install.__name__
        self.pre_install = pre_install
        self.post_install = post_install
        self.tooltip = tooltip
        
        self.connect("query-tooltip", lambda *w: True)
        self.connect('toggled', self.__toggled)
        self.connect('enter-notify-event', self.__enter)
        self.reset_state()

    def __enter(self, *w):
        if self.get_tooltip_window() == None:
            self.set_tooltip_window(self.__create_tooltip_window())
            
    def __create_tooltip_window(self):
        dir_name = '%s/%s'%('../data/nautilus_screenshot', Config.get_locale())
        pkg_window_image_path = "%s/%s.png"%(dir_name, self.apt_package_name)
        pkg_menu_image_path = '%s/%s.menu.png'%(dir_name, self.apt_package_name)
        import os
        if not os.path.exists(pkg_window_image_path):
            pkg_window_image_path = "%s/%s.png"%('../data/nautilus_screenshot', self.apt_package_name)
        if not os.path.exists(pkg_menu_image_path):
            pkg_menu_image_path = '%s/%s.menu.png'%('../data/nautilus_screenshot', self.apt_package_name)
        
        tooltip_vbox = gtk.VBox(False, 5)
        n = 0
        # tooltip
        if self.tooltip:
            tooltip_label = gtk.Label()
            tooltip_label.set_markup(self.tooltip)
            tooltip_vbox.pack_start(left_align(tooltip_label), False)
            n += 1
        # command
        tooltip_vbox.pack_start(
            label_left_align(_('Command: sudo apt-get install/remove %s')%self.apt_package_name), False)
        # menu screenshot
        if os.path.exists(pkg_menu_image_path):
            if n: tooltip_vbox.pack_start(gtk.HSeparator(), False, False, 5)
            menu_label = label_left_align(_('Context menu screenshot:'))
            menu_image = image_left_align(pkg_menu_image_path)
            tooltip_vbox.pack_start(menu_label, False)
            tooltip_vbox.pack_start(menu_image, False)
            n += 1
        # window screenshot
        if os.path.exists(pkg_window_image_path):
            if n: tooltip_vbox.pack_start(gtk.HSeparator(), False, False, 5)
            window_label = label_left_align(_('Window screenshot:'))
            window_image = image_left_align(pkg_window_image_path)
            tooltip_vbox.pack_start(window_label, False)
            tooltip_vbox.pack_start(window_image, False)
        tooltip_vbox.show_all()

        tooltip_window = gtk.Window(gtk.WINDOW_POPUP)
        tooltip_window.set_border_width(10)
        tooltip_window.add(tooltip_vbox)
        tooltip_window.realize()
        tooltip_window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('#f7f7bf'))
        
        return tooltip_window

    def reset_state(self):
        self.installed = APT.installed(self.apt_package_name)
        self.set_active(self.installed)
        self.label.set_markup(self.plain_text)

class NautilusContextMenuSetting(gtk.VBox):
    def __get_package_msgs(self):
        return [
['nautilus-cd-burner',
_('"Write to Disc..." entry'),
_('When CD/DVD image file is clicked by mouse right button, \n'
  'show a "Write to Disc..." menu item.\n'
  '<span color="red">This item conflicts with "brasero".</span>'),],

['nautilus-actions',
_('"Actions Configuration" entry'),
_('It allows the configuration of programs to be launched \n'
  'on files selected.\n'
  '<span color="red">This entry is not in context menu. It is in "System"->"Preferences" menu.</span>'),],

['nautilus-filename-repairer',
_('"Repair filename" entry'),
_('When any file with wrong encoding filename is right clicked,\n')+_('show a "Repair filename" menu item.'),],

['nautilus-gksu',
_('"Open as administrator" entry'),
_('Launch selected files with administration privileges using the context menu.\n')+_('Open selected folder with administration privileges.'),],

['nautilus-image-converter',
_('"Resize/Rotate images" entries'),
_('Resize or rotate selected images.'),],

['nautilus-open-terminal',
_('"Open in terminal" entry'),
_('Open a terminal in current folder.'),],

['nautilus-script-audio-convert',
_('"Convert audio files" entry'),
_('Converts between WAV, OGG, MP3, MPC, FLAC, APE and AAC files.\n'
  'These packages will also be installed: \n'
  '<i>lame vobis-tools libid3-3.8.3-dev flac faac faad mppenc</i>'),
audio_convert_pre,
audio_convert_post,],

['nautilus-script-collection-svn',
_('"Subversion commands" entries'),
None,
None,
collection_svn_post,],

['nautilus-share',
_('"Share" entry for folders'),
_('Share folders by Samba.'),],

['nautilus-wallpaper',
_('"Set as wallpaper" entry'),],
                ]
        
    def __init__(self):
        gtk.VBox.__init__(self, False, 5)
        
        self.button_apply = button_apply = image_stock_button(gtk.STOCK_APPLY, _('Apply') )
        button_apply.connect('clicked', self.__apply_change)
        button_apply.set_sensitive(False)
        align_button_apply = gtk.HBox(False, 0)
        align_button_apply.pack_end(button_apply, False)

        self.checkbuttons = []

        for msg in self.__get_package_msgs():
            if APT.exist(msg[0]):
                button = InstallPackageCheckButton(*msg)
                button.connect('changed', self.set_apply_button_state)
                self.checkbuttons.append( button )
        
        btable = gtk.Table()
        btable.set_col_spacings(10)
        X = Y = 0
        for button in self.checkbuttons:
            btable.attach(button, X, X+1, Y, Y+1, gtk.FILL, gtk.FILL)
            X+=1
            if X==3: ( X,Y ) = ( 0,Y+1 )
        btable.attach(align_button_apply, 2, 3, Y+1, Y+2, gtk.FILL, gtk.FILL)

        self.pack_start(btable, False)

    def set_apply_button_state(self, *w):
        self.button_apply.set_sensitive(False)
        for button in self.checkbuttons:
            if button.installed != button.get_active():
                self.button_apply.set_sensitive(True)
                return

    def __apply_change(self, w):
        install_package = []
        pre_install = []
        post_install = []
        remove_package = []
        
        for button in self.checkbuttons:
            # To install
            if button.installed==False and button.get_active():
                install_package.append(button.apt_package_name)
                if button.pre_install: pre_install.append(button.pre_install)
                if button.post_install: post_install.append(button.post_install)
            # To remove
            if button.installed==True and button.get_active()==False:
                remove_package.append(button.apt_package_name)

        errors = []
        # Install
        import sys
        if len(install_package):
            for f in pre_install:
                try: f()
                except: errors.append( sys.exc_info() )
            
            try: APT.install(*install_package)
            except: errors.append( sys.exc_info() )
            
            for f in post_install:
                try:  f()
                except: errors.append( sys.exc_info() )
        # Remove
        if len(remove_package):
            try: APT.remove(*remove_package)
            except: errors.append( sys.exc_info() )
        #print exception
        if errors:
            import traceback
            import StringIO
            text = StringIO.StringIO()
            for error in errors:
                traceback.print_exception(error[0], error[1], error[2], file=text)
                print >>text
            
            dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR,
                gtk.BUTTONS_CLOSE, _('Traceback:') )
            dialog.set_title( _('Some operation failed.') )
            dialog.format_secondary_text( text.getvalue() )
            dialog.run()
            dialog.destroy()
        else:
            notify( _('All operations succeeded.'), _('The changes will take effect at the next time when GNOME starts up.') )
        
        #reset_state
        for button in self.checkbuttons:
            button.reset_state()
        self.button_apply.set_sensitive(False)

def __nautilus_menu_setting():
    import os
    if not os.path.exists('/usr/bin/nautilus'): raise Exception
    return Setting(NautilusContextMenuSetting(), _('Nautilus context menu'),
                   ['nautilus', 'menu'])

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

def get():
    try:
        return [__nautilus_menu_setting(), __update_manager_setting() ]
    except:
        return []
