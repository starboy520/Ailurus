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

def __study(main_view):
    study_url_items = [ 
        # (use stock?, stock name or icon path, text, web page url, Chinese only?
        None, # Separator
        (True, gtk.STOCK_HELP, _('Ubuntu/Kubuntu configuration guide'),
         'http://ubuntuguide.org/wiki/', False),
        (True, gtk.STOCK_HELP, _('Ubuntu skills'), 
         'http://wiki.ubuntu.org.cn/UbuntuSkills', True),
        (True, gtk.STOCK_HELP, _('Obtain "Full Circle" magazine'), 
         'http://fullcirclemagazine.org/', False),
        (True, gtk.STOCK_HELP, _('Obtain "Ubuntu pocket guide" book'), 
         'http://www.ubuntupocketguide.com/', False),
        (True, gtk.STOCK_HELP, _('Find more third-party repositories on http://repogen.simplylinux.ch/'), 
         'http://repogen.simplylinux.ch/', False),
        #(True, gtk.STOCK_HELP, _(u'How to install themes of Fedora® or OpenSolaris® on Ubuntu ?'), 
        # 'http://tdt.sjtu.edu.cn/S/how_to/fedora_theme.html', False),
        #(True, gtk.STOCK_HELP, _(u'How to install Warcraft III and DotA on Ubuntu ?'), 
        # 'http://ailurus.cn/?p=292', False),
        #(True, gtk.STOCK_HELP, _(u'How to install Matlab on Ubuntu ?'), 
        # 'http://ailurus.cn/?p=285', False),
        #(True, gtk.STOCK_HELP, _('Ubuntu forum in China'),
        # 'http://forum.ubuntu.org.cn/', True),
        #(True, gtk.STOCK_HELP, _('Quick configuration guide (in Chinese)'),
        # 'http://wiki.ubuntu.org.cn/Qref', True),
        #(True, gtk.STOCK_HELP, _('Enjoy online music in Ubuntu (in Chinese)'),
        # 'http://forum.ubuntu.org.cn/viewtopic.php?f=74&t=183104', True),
         ]

    def __get_menu(items):
        ret = []
        for item in items:
            if item == None: 
                ret.append( gtk.SeparatorMenuItem() )
                continue 
            if item[4]==False or (item[4] and Config.is_Chinese_locale()):
                if item[0]: menu_item = image_stock_menuitem(item[1], item[2])
                else: menu_item = image_file_menuitem(item[2], item[1], 16, 3)
                menu_item.url = item[3]
                menu_item.connect('activate', lambda w: open_web_page(w.url))
                ret.append( menu_item )
        return ret
    
    return __get_menu(study_url_items)

def __preferences(main_view):
    menu_not_clean_apt_cache=gtk.CheckMenuItem(_("""Don't automatically clean /var/cache/apt/"""))
    menu_not_clean_apt_cache.set_active( Config.get_disable_clean_apt_cache() )
    menu_not_clean_apt_cache.connect('toggled',
            lambda w: notify(_('Preferences changed'), _('Your changes will take effect at the next time when the program starts up.'))
                              or Config.set_disable_clean_apt_cache(w.get_active()))
    
    return [ menu_not_clean_apt_cache ]

def __quick_setup(main_view):
    import os
    assert os.path.exists('ubuntu/quick_setup.py')

    assert hasattr(main_view, 'lock')
    assert hasattr(main_view, 'unlock')
    assert main_view.install_remove_pane
    assert hasattr(main_view.install_remove_pane, 'app_class_installed_state_changed_by_external')
    
    from quick_setup import quick_setup
    def run_quick_setup_thread():
        try:
            import subprocess
            task = subprocess.Popen(['python', 'ubuntu/quick_setup.py'])
            task.wait()
        finally:
            gtk.gdk.threads_enter()
            main_view.install_remove_pane.app_class_installed_state_changed_by_external()
            main_view.unlock()
            main_view.install_remove_pane.set_sensitive(True)
            gtk.gdk.threads_leave()
    def callback(*w):
        import thread
        main_view.lock()
        main_view.install_remove_pane.set_sensitive(False)
        thread.start_new_thread(run_quick_setup_thread, ())
    menu = gtk.MenuItem( _('Quick setup') )
    menu.connect('activate', callback)
    return [ menu ]

def get(main_view):
    assert hasattr(main_view, 'activate_pane')

    return [
        [_('Quick setup'), __quick_setup(main_view), 10],
        [_('Learning'),      __study(main_view),     21],
        [_('Preferences'), __preferences(main_view), 22],
        ]
