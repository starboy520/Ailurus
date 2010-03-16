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
import gtk, os, sys
from lib import *
from libu import *

class MainView:
    def __reset_enable_disable_buttons_state(self):
        if self.is_current_pane_disabled():
            self.toolbar_item_enable.set_sensitive(True)
            self.toolbar_item_disable.set_sensitive(False)
        else:
            self.toolbar_item_enable.set_sensitive(False)
            self.toolbar_item_disable.set_sensitive(True)
            
    def __toolbar(self):
        self.panel_name  = panel_name = gtk.Label()
        panel_name.set_tooltip_text(_('Name of current panel') )
        panel_name.set_size_request(300, -1)
        item_pane_name = gtk.ToolItem()
        item_pane_name.add(panel_name)

        self.toolbar_item_back = item_b_back = image_toolitem(D+'other_icons/toolbar_back.png', self.back_one_pane, tooltip=_('Go back one panel') )
        self.toolbar_item_forward = item_b_forward = image_toolitem(D+'other_icons/toolbar_forward.png', self.forward_one_pane, tooltip=_('Go forward one panel') )
        def enable_cb(w):
            self.disable_current_pane(False)
            self.__reset_enable_disable_buttons_state()
        def disable_cb(w):
            self.disable_current_pane(True)
            self.__reset_enable_disable_buttons_state()
        self.toolbar_item_enable = item_enable_current = image_toolitem(D+'other_icons/toolbar_enable.png', enable_cb, tooltip=_('Enable current pane') ) 
        self.toolbar_item_disable = item_disable_current = image_toolitem(D+'other_icons/toolbar_disable.png', disable_cb, tooltip=_('Disable current pane') )
        item_show_day_tip = image_toolitem(D+'other_icons/toolbar_study.png', self.show_day_tip, tooltip=_('Display "Tip of the day"') )
        item_propose_suggestion = image_toolitem(D+'umut_icons/m_propose_suggestion.png', lambda *w: report_bug(), tooltip=_('Propose suggestion and report bugs') )
        item_quit = image_toolitem(D+'other_icons/toolbar_quit.png', self.terminate_program, tooltip=_("Quit") )

        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        toolbar.insert(item_pane_name, 0)
        toolbar.insert(item_show_day_tip, 1)
        toolbar.insert(item_propose_suggestion, 2)
        toolbar.insert(item_b_back, 3)
        toolbar.insert(item_b_forward, 4)
        toolbar.insert(item_enable_current, 5)
        toolbar.insert(item_disable_current, 6)
        toolbar.insert(item_quit, 7)

        return toolbar

    def add_more_buttons_in_toolbar(self):
        List = [
            ('HardwareInfoPane', D+'umut_icons/m_hardware.png', _('Hardware information'), ),
            ('LinuxInfoPane', D+'umut_icons/m_linux.png', _('Linux information'), ),
            ('SystemSettingPane', D+'umut_icons/m_linux_setting.png', _('System settings'), ),
            ('InstallRemovePane', D+'umut_icons/m_install_remove.png', _('Install/Remove'), ),
            ('OfflineInstallPane', D+'umut_icons/m_cache_files.png', _('Cache installation files'), ),
            ('UbuntuFastestMirrorPane', D+'umut_icons/m_fastest_repos.png', _('Find fast repository mirror'), ),
            ('UbuntuAPTRecoveryPane', D+'umut_icons/m_apt_recovery.png', _('APT recovery'), ),
                     ]
        List.reverse()
        for name, icon, tooltip in List:
            if not name in self.contents: continue
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icon, 24, 24)
            button = gtk.Button()
            button.add( gtk.image_new_from_pixbuf(pixbuf) )
            button.set_relief(gtk.RELIEF_NONE)
            button.set_tooltip_text(tooltip)
            button.connect_object('clicked', self.activate_pane, name)
            item = gtk.ToolItem()
            item.add(button)
            self.toolbar.insert(item, 1)

    def __update_item_buttons_state(self):
        self.toolbar_item_back.set_sensitive(len(self.__navigate_1)>1)
        self.toolbar_item_forward.set_sensitive(len(self.__navigate_2))
        import common.menu
        common.menu.set_back_forward_sensitive(len(self.__navigate_1)>1, len(self.__navigate_2))

    def back_one_pane(self, w):
        if len(self.__navigate_1)>1:
            name = self.__navigate_1.pop()
            assert isinstance(name, str)
            self.__navigate_2.insert(0, name)
            name = self.__navigate_1[-1]
            self.change_content_basic(name)
            self.__update_item_buttons_state()
        
    def forward_one_pane(self, w):
        if len(self.__navigate_2):
            name = self.__navigate_2.pop(0)
            assert isinstance(name, str)
            self.__navigate_1.append(name)
            self.change_content_basic(name)
            self.__update_item_buttons_state()

    def activate_pane(self, name):
        assert isinstance(name, str)
        assert name in self.contents, [name, self.contents.keys()]
        if self.__navigate_1==[] or self.__navigate_1[-1]!=name:
            self.__navigate_1.append(name)
        self.__navigate_2 = []
        self.change_content_basic(name)
        self.__update_item_buttons_state()

    def change_content_basic(self, name):
        assert isinstance(name, str)
        self.current_pane = name
        for child in self.toggle_area.get_children():
            self.toggle_area.remove(child)
        if Config.is_pane_disabled(name): 
            content = self.disabledpane
        else:
            content = self.contents[name]
        self.toggle_area.add(content)
        self.toggle_area.show_all()
        self.panel_name.set_markup('<b>%s</b>'%self.contents[name].name)
        self.__reset_enable_disable_buttons_state()

    def is_current_pane_disabled(self):
        name = self.current_pane
        assert isinstance(name, str)
        return Config.is_pane_disabled(name)

    def disable_current_pane(self, value):
        name = self.current_pane
        assert isinstance(name, str)
        
        Config.set_pane_disabled(name, value)
        
        if value: content = self.disabledpane
        else: content = self.contents[name]
        for child in self.toggle_area.get_children():
            self.toggle_area.remove(child)
        self.toggle_area.add(content)
        self.toggle_area.show_all()

    def lock(self):
        self.stop_delete_event = True
        self.menubar.set_sensitive(False)
        self.toolbar.set_sensitive(False)
    
    def unlock(self):
        self.stop_delete_event = False
        self.menubar.set_sensitive(True)
        self.toolbar.set_sensitive(True)

    def terminate_program(self, *w):
        if self.stop_delete_event:
            return True
        
        from support.windowpos import WindowPos
        WindowPos.save(self.window,'main')
        
        for pane in self.contents.values():
            if hasattr(pane, 'save_state'):
                pane.save_state()

        gtk.main_quit()
        sys.exit()

    def show_day_tip(self, *w):
        from support.tipoftheday import TipOfTheDay
        w=TipOfTheDay()
        w.run()
        w.destroy()

    def offline_mode_button(self):
        button = image_stock_button(gtk.STOCK_HARDDISK, _('Cache installation files') )
        button.connect('clicked', lambda w: self.activate_pane('OfflineInstallPane'))
        return button

    def register(self, pane):
        key = pane.__class__.__name__
        try:
            assert not '.' in key, key
            assert not key in self.contents, key
            self.contents[key] = pane
        except:
            import traceback
            traceback.print_exc()

    def add_menu(self, menustruct):
        assert isinstance(menustruct, list)
        assert self.menubar
        
        map_menu = {}
        for i in menustruct:
            text, items = i[0], i[1]
            assert isinstance(text, (str,unicode) )
            assert isinstance(items, list)
            
            if not text in map_menu: 
                menu = gtk.Menu()
                title = gtk.MenuItem(text)
                title.set_submenu(menu)
                self.menubar.append(title)
                map_menu[text] = (title, menu)

        for i in menustruct:
            text, items = i[0], i[1]
            menu = map_menu[text][1]
            for j in items:
                assert isinstance(j, (gtk.MenuItem, gtk.SeparatorMenuItem) )
                menu.append(j)
        
        self.menubar.show_all()

    def __init__(self):
        self.app_classes = None
        self.window = None # MainView window
        self.stop_delete_event = False
        self.__navigate_1 = [] #backward and forward
        self.__navigate_2 = [] #backward and forward
        from support.disabledpane import DisabledPane
        self.disabledpane = DisabledPane()
        
        self.contents = {}
        
        self.toggle_area = gtk.VBox()
        self.toggle_area.set_border_width(5)
        
        vbox = gtk.VBox(False, 0)
        
        self.menubar = gtk.MenuBar()
        vbox.pack_start(self.menubar, False, False)
        
        self.toolbar = self.__toolbar()
        vbox.pack_start(self.toolbar, False)
        
        vbox.pack_start(self.toggle_area, True, True)
        
        self.window = window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Ailurus')
        window.connect("delete_event", self.terminate_program)
        window.add(vbox)

        from support.windowpos import WindowPos
        WindowPos.load(window,'main')

def detect_running_instances():
    string = get_output('ps -a -u $USER | grep ailurus', True)
    if string!='':
        notify(_('Warning!'), 
           _('Another instance of Ailurus is running. '
              'It is not recommended to run multiple instance concurrently.') )
def change_task_name():
    import ctypes
    libc = ctypes.CDLL('libc.so.6')
    libc.prctl(15, 'ailurus', 0, 0, 0)
def set_default_window_icon():
    gtk.window_set_default_icon_from_file(D+'suyun_icons/default.png')

detect_running_instances()
change_task_name()
set_default_window_icon()
# show splash window
from support.splashwindow import SplashWindow
splash = SplashWindow()
splash.show_all()
while gtk.events_pending(): gtk.main_iteration()
# import common
import common as COMMON
# check desktop environment
splash.add_text(_('<span color="yellow">Checking desktop environment ... </span>\n'))
if Config.is_XFCE():
    DESKTOP = None
elif Config.is_GNOME():
    import gnome as DESKTOP
else:
    DESKTOP = None
# check distribution
splash.add_text(_('<span color="yellow">Checking distribution ... </span>\n'))
if Config.is_Mint():
    try:
        versions = ['hardy', 'intrepid', 'jaunty', 'karmic', 'lucid', ]
        rs = Config.get_Mint_version()
        if rs in ['5', '6', '7', '8', '9']:
            version = versions[int(rs)-5]
        Config.set_Ubuntu_version( version )
        import ubuntu as DISTRIBUTION
    except:
        DISTRIBUTION = None
        import traceback
        traceback.print_exc()
elif Config.is_Ubuntu(): 
    import ubuntu as DISTRIBUTION
elif Config.is_Fedora():
    import fedora as DISTRIBUTION
else:
    DISTRIBUTION = None
# acquire Firefox profile "~/.mozilla/firefox/profiles.ini"
import os
if os.path.exists('/usr/bin/firefox'):
    propath = os.path.expanduser('~/.mozilla/firefox/profiles.ini')
    splash.add_text(_('<span color="yellow">Acquiring Firefox profile ... </span>\n'))
    if not os.path.exists(propath):
        splash.add_text(_('<span color="yellow">Waiting for firefox to create profile ... </span>\n'))
        KillWhenExit.add('firefox -no-remote')
        import time
        start = time.time()
        while not os.path.exists(propath) and time.time() - start < 6:
            time.sleep(0.1)
# acquire installed package
if DISTRIBUTION and DISTRIBUTION.__name__ == 'ubuntu':
    splash.add_text(_('<span color="yellow">Acquire list of installed packages ... </span>\n'))
    APT.refresh_cache()
elif DISTRIBUTION and DISTRIBUTION.__name__ == 'fedora':
    splash.add_text(_('<span color="yellow">Acquire list of installed packages ... </span>\n'))
    RPM.refresh_cache()
# other initialization
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

splash.add_text(_('<span color="yellow">Loading tips ... </span>\n'))
from loader import load_tips
tips = load_tips(COMMON, DESKTOP, DISTRIBUTION)
import support.tipoftheday
support.tipoftheday.tips = tips

splash.add_text(_('<span color="yellow">Loading main window ... </span>\n'))
main_view = MainView()

splash.add_text(_('<span color="yellow">Loading information pane ... </span>\n'))
from loader import load_hardwareinfo
hwinfo = load_hardwareinfo(COMMON, DESKTOP, DISTRIBUTION)
from info_pane import HardwareInfoPane
pane = HardwareInfoPane(main_view, hwinfo)
main_view.register(pane)

from loader import load_linuxinfo
linuxinfo = load_linuxinfo(COMMON, DESKTOP, DISTRIBUTION)
from info_pane import LinuxInfoPane
pane = LinuxInfoPane(main_view, linuxinfo)
main_view.register(pane)

splash.add_text(_('<span color="yellow">Loading system settings pane ... </span>\n'))
from loader import load_setting
items = load_setting(COMMON, DESKTOP, DISTRIBUTION)
from system_setting_pane import SystemSettingPane
pane = SystemSettingPane(items)
main_view.register(pane)

splash.add_text(_('<span color="yellow">Loading applications pane ... </span>\n'))
from loader import load_app_classes
app_classes = load_app_classes(COMMON, DESKTOP, DISTRIBUTION)
main_view.app_classes = app_classes
from loader import load_custom_app_classes
custom_app_classes = load_custom_app_classes()
from install_remove_pane import InstallRemovePane
pane = InstallRemovePane(main_view, app_classes + custom_app_classes)
main_view.register(pane)
main_view.install_remove_pane = pane

splash.add_text(_('<span color="yellow">Loading off-line pane ... </span>\n'))
from loader import load_R_objs
r_objs = load_R_objs(COMMON, DESKTOP, DISTRIBUTION)
from offline_install_pane import OfflineInstallPane
pane = OfflineInstallPane(main_view, r_objs)
main_view.register(pane)

splash.add_text(_('<span color="yellow">Loading menu ... </span>\n'))
from loader import load_menu
menustruct = load_menu(COMMON, DESKTOP, DISTRIBUTION, main_view)
main_view.add_menu(menustruct)

for module in [ COMMON, DESKTOP, DISTRIBUTION ]:
    if hasattr(module, 'pane_register'):
        module.pane_register.register(main_view)

main_view.add_more_buttons_in_toolbar()

main_view.activate_pane('InstallRemovePane')
main_view.window.show_all()
splash.destroy()
# show tip of the day
if not Config.get_disable_tip():
    main_view.show_day_tip()
#
def exception_happened(etype, value, tb):
    if etype == KeyboardInterrupt: return
    
    import traceback, StringIO
    msg = StringIO.StringIO()
    print >>msg, _('Traceback:')
    traceback.print_tb(tb, file=msg)
    print >>msg, etype, ':', value

    title_box = gtk.HBox(False, 5)
    import os
    if os.path.exists(D+'umut_icons/bug.png'):
        image = gtk.Image()
        image.set_from_file(D+'umut_icons/bug.png')
        title_box.pack_start(image, False)
    title = label_left_align( _('A bug appears. Would you please tell Ailurus developers? Thank you!') )
    title_box.pack_start(title, False)
    
    textview_traceback = gtk.TextView()
    gray_bg(textview_traceback)
    textview_traceback.set_wrap_mode(gtk.WRAP_WORD)
    textview_traceback.get_buffer().set_text(msg.getvalue())
    textview_traceback.set_cursor_visible(False)
    scroll_traceback = gtk.ScrolledWindow()
    scroll_traceback.set_shadow_type(gtk.SHADOW_IN)
    scroll_traceback.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scroll_traceback.add(textview_traceback)
    scroll_traceback.set_size_request(-1, 300)
    button_report_bug = image_stock_button(gtk.STOCK_DIALOG_WARNING, _('Click here to report bug via web-page') )
    button_report_bug.connect('clicked', lambda w: report_bug() )
    button_close = image_stock_button(gtk.STOCK_CLOSE, _('Close'))
    button_close.connect('clicked', lambda w: dialog.destroy())
    bottom_box = gtk.HBox(False, 10)
    bottom_box.pack_start(button_report_bug, False)
    bottom_box.pack_start(button_close, False)
    
    dialog = gtk.Dialog(_('Bug appears!'), None, gtk.DIALOG_NO_SEPARATOR)
    dialog.set_border_width(10)
    dialog.vbox.set_spacing(5)
    dialog.vbox.pack_start(title_box, False)
    dialog.vbox.pack_start(scroll_traceback)
    dialog.vbox.show_all()
    
    dialog.action_area.pack_start(bottom_box, False)
    dialog.action_area.show_all()
    
    dialog.run()
    dialog.destroy()
    sys.exit()

import sys
sys.excepthook = exception_happened
# all right
gtk.gdk.threads_init()
gtk.gdk.threads_enter()
gtk.main()
gtk.gdk.threads_leave()
sys.exit()
