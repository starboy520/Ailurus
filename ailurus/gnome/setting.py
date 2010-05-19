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
import sys, os
from lib import *
from libu import *
from libsetting import *
def __desktop_icon_setting():
    table = gtk.Table()
    table.set_col_spacings(10)
    o = GConfCheckButton(_('Show desktop content'), '/apps/nautilus/preferences/show_desktop',
             _('Show/hide icons on desktop.\n'
               '<span color="red">The change will take effect at the next time GNOME starts up.</span>'))
    def show_notify(checkbutton):
         if checkbutton.get_active():
             notify(_('Information'), _('Desktop content will be displayed at the next time GNOME starts up.'))
    o.connect('toggled', show_notify)
    table.attach(o, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
    o = GConfCheckButton(_('Display "Mounted volumn" icon'), '/apps/nautilus/desktop/volumes_visible',
             _('Put icons linking to mounted volumes on the desktop.'))
    table.attach(o, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
    
    o = GConfCheckButton(_('Display "Computer" icon'), '/apps/nautilus/desktop/computer_icon_visible',
             _('Put an icon linking to the computer location on the desktop.'))
    table.attach(o, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
    
    l = gtk.Label(_('Change icon name to:'))
    table.attach(l, 1, 2, 2, 3, gtk.FILL, gtk.FILL)
    
    en = GConfTextEntry('/apps/nautilus/desktop/computer_icon_name')
    table.attach(en, 2, 3, 2, 3, gtk.FILL, gtk.FILL)
    
    o = GConfCheckButton(_('Display "Home folder" icon'), '/apps/nautilus/desktop/home_icon_visible',
             _('Put an icon linking to the home folder on the desktop.'))
    table.attach(o, 0, 1, 3, 4, gtk.FILL, gtk.FILL)
    
    l = gtk.Label(_('Change icon name to:'))
    table.attach(l, 1, 2, 3, 4, gtk.FILL, gtk.FILL)
    
    en = GConfTextEntry('/apps/nautilus/desktop/home_icon_name')
    table.attach(en, 2, 3, 3, 4, gtk.FILL, gtk.FILL)
        
    o = GConfCheckButton(_('Display "Network server" icon'), '/apps/nautilus/desktop/network_icon_visible',
             _('Put an icon linking to the Network Servers view on the desktop.'))
    table.attach(o, 0, 1, 4, 5, gtk.FILL, gtk.FILL)
    
    l = gtk.Label(_('Change icon name to:'))
    table.attach(l, 1, 2, 4, 5, gtk.FILL, gtk.FILL)
    
    en = GConfTextEntry('/apps/nautilus/desktop/network_icon_name')
    table.attach(en, 2, 3, 4, 5, gtk.FILL, gtk.FILL)
    
    o = GConfCheckButton(_('Display "Trash" icon'),'/apps/nautilus/desktop/trash_icon_visible',
             _('Put an icon linking to the trash on the desktop.'))
    table.attach(o, 0, 1, 5, 6, gtk.FILL, gtk.FILL)
    
    l = gtk.Label(_('Change icon name to:'))
    table.attach(l, 1, 2, 5, 6, gtk.FILL, gtk.FILL)

    en = GConfTextEntry('/apps/nautilus/desktop/trash_icon_name')
    table.attach(en, 2, 3, 5, 6, gtk.FILL, gtk.FILL)

    return Setting(table, _('Desktop icons'), ['desktop', 'icon'])

def __start_here_icon_setting():
    def apply(imagechooser, old_image):
        imagechooser.scale_image(old_image, '/tmp/start-here.png', 24, 24)
        
        import os
        local_icons_dir = os.path.expanduser('~/.icons')
        for root, dirs, files in os.walk('/usr/share/icons/'):
            for file_name in files:
                if 'start-here' in file_name and '24' in root:
                    usr_path = os.path.join(root, file_name)
                    local_path = usr_path.replace('/usr/share/icons', local_icons_dir)
                    local_dir = os.path.dirname(local_path)
                    if not os.path.exists(local_dir): run('mkdir -p ' + local_dir)
                    run('cp /tmp/start-here.png %s' % local_path)
        
        notify(_('Icon changed'), _('Your changes will take effect at the next time when you log in to GNOME.'))

    def get_start_here_icon_path():
        import os , gconf
        g = gconf.client_get_default();
        local_dir = os.path.expanduser('~/.icons')
        theme_name = g.get_string('/desktop/gnome/interface/icon_theme')
        for root, dirs, files in os.walk('/usr/share/icons/' + theme_name):
            for file_name in files:
                if 'start-here' in file_name and '24' in root:
                    usr_path = os.path.join(root, file_name)
                    local_path = usr_path.replace('/usr/share/icons', local_dir)
                    if os.path.exists(local_path): return local_path
                    elif os.path.exists(usr_path): return usr_path
        return ''

    path = get_start_here_icon_path()
    i = ImageChooser(_('The "start-here" icon is %s') % path, 24, 24)
    try:
        i.display_image(path)
    except:
        i.display_image(D + '/other_icons/blank.png')
    i.connect('changed', apply)
    box = gtk.VBox(False, 0)
    box.pack_start(left_align(i))
    return Setting(box, _('Change "start-here" icon'), ['icon'])

def __login_icon_setting():
    def apply(w, image):
        path = os.path.expanduser('~/.face')
        os.system('cp %s %s' % (image, path))
        notify(_('Icon changed'), _('Your changes will take effect at the next time when you log in to GNOME.'))

    i = ImageChooser(_('The login icon is ~/.face'), 96, 96)
    try:
        i.display_image(os.path.expanduser('~/.face'))
    except:
        i.display_image(D + '/other_icons/blank.png')
    i.connect('changed',apply)
    box = gtk.VBox(False, 0)
    box.pack_start(left_align(i))
    return Setting(box, _('Change login icon'), ['icon'])
    
def __menu_icon_setting():
    vbox = gtk.VBox()
    o = GConfCheckButton(_('Show icons of menu entries'), 
             '/desktop/gnome/interface/menus_have_icons',
             _('Whether menus may display an icon next to a menu entry.'))
    vbox.pack_start(o, False)
    return Setting(vbox, _('Menu entry icons setting'), ['menu', 'icon'])


def __button_icon_setting():
    vbox = gtk.VBox()
    o = GConfCheckButton(_('Show icon in buttons'), 
             '/desktop/gnome/interface/buttons_have_icons',
             _('Whether buttons may display an icon next to text.'))
    vbox.pack_start(o, False)
    return Setting(vbox, _('Button icons setting'), ['icon'])

def __disable_terminal_beep():
    vbox = gtk.VBox()
    o = GConfCheckButton(_('Disable terminal bell'), 
             '/apps/gnome-terminal/profiles/Default/silent_bell',
             _("If it is set to true, gnome terminal will not generate beep sound when error happens.") )
    vbox.pack_start(o, False)
    return Setting(vbox, _('Terminal beep sound setting'), ['sound'])

def __more_nautilus_settings():
    table = gtk.Table()
    o = GConfCheckButton(_('Automatically mount CD and flash disks'), 
             '/apps/nautilus/preferences/media_automount', 
             _('If set to true, then Nautilus will automatically mount media such as CD and flash disks.'))
    table.attach(o, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
    m = GConfCheckButton(_('Show more permissions setting in file property dialog'),
                '/apps/nautilus/preferences/show_advanced_permissions' )
    table.attach(m, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
    return Setting(table, _('More Nautilus settings'), ['nautilus'])

def __font_size_setting():
    def change_font(w, isincrease):
        import gconf
        g = gconf.client_get_default()
        gconf_font_keys = [
          '/apps/nautilus/preferences/desktop_font',
          '/desktop/gnome/interface/document_font_name',
          '/desktop/gnome/interface/font_name',
          '/desktop/gnome/interface/monospace_font_name',
          '/apps/metacity/general/titlebar_font', ]
        for key in gconf_font_keys:
            value = g.get_string(key)
            l = value.rsplit(' ',1)
            size = int(float(l[-1]))
            if isincrease: size += 1
            else: size -= 1
            l[-1] = str(size)
            value = ' '.join(l)
            g.set_string(key, value)

    button_increase = image_stock_button(gtk.STOCK_ZOOM_IN, _('Larger font') )
    button_increase.connect('clicked', change_font, True)
    button_increase.set_tooltip_text(
                          _('Change these GConf keys:\n') +
                          '/apps/nautilus/preferences/desktop_font\n'
                          '/desktop/gnome/interface/document_font_name\n'
                          '/desktop/gnome/interface/font_name\n'
                          '/desktop/gnome/interface/monospace_font_name\n'
                          '/apps/metacity/general/titlebar_font')
    button_decrease = image_stock_button(gtk.STOCK_ZOOM_OUT, _('Smaller font') )
    button_decrease.connect('clicked', change_font, False)
    button_decrease.set_tooltip_text(
                          _('Change these GConf keys:\n') +
                          '/apps/nautilus/preferences/desktop_font\n'
                          '/desktop/gnome/interface/document_font_name\n'
                          '/desktop/gnome/interface/font_name\n'
                          '/desktop/gnome/interface/monospace_font_name\n'
                          '/apps/metacity/general/titlebar_font')
    hbox = gtk.HBox(False, 10)
    hbox.pack_start(button_increase, False, False)
    hbox.pack_start(button_decrease, False, False)
    hbox.show_all()
    return Setting(hbox, _('One-click changing font size'), ['font'])

def __layout_of_window_titlebar_buttons():
    label = gtk.Label(_('The layout of window title-bar buttons'))
    label.set_tooltip_text(_('GConf key: ') + '/app/metacity/general/button_layout\n'
                           + _("It can be used in Metacity only.") )
    o = GConfComboBox('/apps/metacity/general/button_layout', 
                      [_('GNOME classic'), _('MAC OS X')],
                      ['menu:minimize,maximize,close', 'close,minimize,maximize:'],)
    hbox = gtk.HBox(False, 10)
    hbox.pack_start(label, False)
    hbox.pack_start(o, False)
    return Setting(hbox, _('The layout of window title-bar buttons'), ['window'])

def __window_behaviour_setting():
    label_double = gtk.Label(_('double-clicked by mouse left button:'))
    label_double.set_tooltip_text(_('The effects of double-clicking on the title bar.')+_('\nGConf key: ')+'/apps/metacity/general/action_double_click_titlebar')
    label_right = gtk.Label(_('clicked by mouse right button:'))
    label_right.set_tooltip_text(_('The effects of right-clicking on the title bar.')+_('\nGConf key: ')+'/apps/metacity/general/action_right_click_titlebar')
    label_middle = gtk.Label(_('clicked by mouse wheel:'))
    label_middle.set_tooltip_text(_('The effects of clicking on the title bar by mouse wheel.')+_('\nGConf key: ')+'/apps/metacity/general/action_middle_click_titlebar')
    table = gtk.Table()
    table.set_col_spacings(5)
    table.attach(label_double, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
    table.attach(
            GConfComboBox(
              '/apps/metacity/general/action_double_click_titlebar',
              [_('maximize'),        _('minimize'), _('roll up'),    _('put behind others'), _('maximize horizontally'),             _('maximize vertically') ],
              ['toggle_maximize', 'minimize', 'toggle_shade', 'lower',                        'toggle_maximize_horizontally',   'toggle_maximize_vertically'],
              _('The effects of double-clicking on the title bar.')
              ),
              1, 2, 0, 1, gtk.FILL, gtk.FILL)
    table.attach(label_right, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
    table.attach(
        GConfComboBox(
              '/apps/metacity/general/action_right_click_titlebar',
              [_('show menu'), _('maximize'),             _('minimize'), _('roll up'),           _('put behind others'), _('maximize horizontally'),             _('maximize vertically')],
              ['menu',             'toggle_maximize',        'minimize', 'toggle_shade',         'lower',                        'toggle_maximize_horizontally',   'toggle_maximize_vertically'],
              _('The effects of right-clicking on the title bar.')
              ),
              1, 2, 1, 2, gtk.FILL, gtk.FILL)
    table.attach(label_middle, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
    table.attach(
        GConfComboBox(
              '/apps/metacity/general/action_middle_click_titlebar',
              [_('show menu'), _('maximize'),             _('minimize'), _('roll up'),           _('put behind others'), _('maximize horizontally'),             _('maximize vertically')],
              ['menu',             'toggle_maximize',        'minimize', 'toggle_shade',         'lower',                        'toggle_maximize_horizontally',   'toggle_maximize_vertically'],
              _('The effects of clicking on the title bar by mouse wheel.')
              ),
              1, 2, 2, 3, gtk.FILL, gtk.FILL)
    return Setting(table, _('Window effect after that window title bar is ...'), ['window'])

def __textbox_context_menu_setting():
    table = gtk.Table()
    table.set_col_spacings(10)
    o = GConfCheckButton(_('Show "Input method" entry'), '/desktop/gnome/interface/show_input_method_menu',
             _('This option affects GEdit and all GTK text-boxes.'))
    table.attach(o, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
    o = GConfCheckButton(_('Show "Insert Unicode control character" entry'), '/desktop/gnome/interface/show_unicode_menu',
             _('This option affects GEdit and all GTK text-boxes.'))
    table.attach(o, 1, 2, 0, 1, gtk.FILL, gtk.FILL)
    return Setting(table, _('Text-boxes context menu'), ['menu'])

def __gnome_splash_setting():
    def changed(w, new_path):
        g.set_string('/apps/gnome-session/options/splash_image', new_path)

    e = GConfCheckButton(_('Show login splash image: '),
     '/apps/gnome-session/options/show_splash_screen',
     _('If its value is true, a splash image is displayed after you log in to GNOME.'))
    
    import gconf
    g = gconf.client_get_default()
    image_path = g.get_string('/apps/gnome-session/options/splash_image')
    o = ImageChooser(_('GConf key: ') + '/apps/gnome-session/options/splash_image', 96, 96)
    try: o.display_image(image_path)
    except: o.display_image(D + '/other_icons/blank.png')
    o.connect('changed', changed)

    hbox = gtk.HBox(False)
    hbox.pack_start(e, False)
    hbox.pack_start(o, False)
    return Setting(hbox, _('GNOME splash image'), ['session'])

def __restriction_on_current_user():
    table = gtk.Table()
    table.set_col_spacings(10)
    table.attach(
           label_left_align(_('These settings restrict current user only. They do not affect other users.')),
           0, 2, 0, 1, gtk.FILL, gtk.FILL)
    o = GConfCheckButton(_('Disable Alt+F2 (Launch application)'),
           '/desktop/gnome/lockdown/disable_command_line',
           _('Prevent current user from pressing Alt+F2 to launch applications.') )
    table.attach(o, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
    o = GConfCheckButton(_('Disable Ctrl+Alt+L (Lock screen)'),
           '/desktop/gnome/lockdown/disable_lock_screen',
           _('Prevent current user from pressing Ctrl+Alt+L to lock screen.') )
    table.attach(o, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
    o = GConfCheckButton(_('Disable "print" entry in all menus.'),
           '/desktop/gnome/lockdown/disable_printing',
           _('Prevent current user from printing any documents.'))
    table.attach(o, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
    o = GConfCheckButton(_('Disable "print setup" entry in all menus.'),
           '/desktop/gnome/lockdown/disable_print_setup',
           _('Prevent current user from modifying print settings.'))
    table.attach(o, 1, 2, 2, 3, gtk.FILL, gtk.FILL)
    o = GConfCheckButton(_('Disable "save as" entry in all menus.'),
           '/desktop/gnome/lockdown/disable_save_to_disk',
           _('Prevent current user from saving files by "Save as ..." dialog') )
    table.attach(o, 0, 1, 3, 4, gtk.FILL, gtk.FILL)
    o = GConfCheckButton(_('Forbid running multiple GNOME session.'),
           '/desktop/gnome/lockdown/disable_user_switching',
           _('Prevent current user from switching to another account, unless she has logged out from GNOME before switching.') )
    table.attach(o, 1, 2, 3, 4, gtk.FILL, gtk.FILL)
    return Setting(table, _('Restriction on current user'), ['restriction'])

def __nautilus_thumbnail_setting():
    table = gtk.Table()
    table.set_col_spacings(10)
    
    import os
    text = label_left_align( _('The thumbnail cache directory is "%s/.thumbnails".')%os.environ['HOME'] )
    table.attach(text, 0, 2, 0, 1, gtk.FILL, gtk.FILL)
    
    label = label_left_align(_('Maximum size of thumbnail cache (in MBytes):'))
    key = '/desktop/gnome/thumbnail_cache/maximum_size'
    label.set_tooltip_text(_('GConf key: %s')%key)
    table.attach(label, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
    
    o = GConfNumericEntry(key, 0, 2048)
    table.attach(o, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
    
    label = label_left_align(_('Maximum time each thumbnail remains in cache (in days):'))
    key = '/desktop/gnome/thumbnail_cache/maximum_age'
    label.set_tooltip_text(_('GConf key: %s')%key)
    table.attach(label, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
    
    o = GConfNumericEntry(key, 0, 30)
    table.attach(o, 1, 2, 2, 3, gtk.FILL, gtk.FILL)
    
    label = label_left_align(_('Size of each thumbnail (in pixels):'))
    key = '/apps/nautilus/icon_view/thumbnail_size'
    label.set_tooltip_text(_('GConf key: %s')%key)
    table.attach(label, 0, 1, 3, 4, gtk.FILL, gtk.FILL)
    
    o = GConfNumericEntry(key, 16, 96)
    table.attach(o, 1, 2, 3, 4, gtk.FILL, gtk.FILL)
    
    return Setting(table, _('Nautilus thumbnail settings'), ['nautilus'])

def __gnome_session_setting():
    table = gtk.Table()
    table.set_col_spacings(10)
    pos = 0
    o = GConfCheckButton(_('Remember running applications when you log out.'),
             '/apps/gnome-session/options/auto_save_session',
             _('If its value is true, GNOME will remember the running applications when you log out, '
               'and re-launch these applications at the next time you log in to GNOME.') )
    table.attach(o, 0, 1, pos, pos+1, gtk.FILL, gtk.FILL)
    button = gtk.Button(_('Configure autostart applications'))
    button.set_tooltip_text(_('Run command: gnome-session-properties'))
    button.connect('clicked', lambda w: KillWhenExit.add('gnome-session-properties'))
    table.attach(button, 1, 2, pos, pos+1, gtk.FILL, gtk.FILL); pos += 1
    o = GConfCheckButton(_('Prompt you before you log out from GNOME.'),
            '/apps/gnome-session/options/logout_prompt',
            _('If its value is false, GNOME session will terminate immediately if you click the menu "System"->"Log out".') )
    table.attach(o, 0, 1, pos, pos+1, gtk.FILL, gtk.FILL); pos += 1
    o = GConfCheckButton(_('Allow connection from remote hosts.'),
            '/apps/gnome-session/options/allow_tcp_connections')
    table.attach(o, 0, 1, pos, pos+1, gtk.FILL, gtk.FILL); pos += 1
#    o = GConfCheckButton(_('Enable switch to different user from the "Unlock" dialog'),
#            '/apps/gnome-screensaver/user_switch_enable',
#            _('If its value is true, you will be able to switch to a different user account from the "Unlock" dialog.') )
#    table.attach(o, 0, 1, pos, pos+1, gtk.FILL, gtk.FILL); pos += 1
#    o = GConfCheckButton(_('Show confirmation dialogs when you using indicator session tool to logout/restart/shutdown'),
#            '/apps/indicator-session/suppress_logout_restart_shutdown', 
#            _('If its value is false, Gnome will not show confirmation '
#              'dialogs when you using the Indicator Session Tool to logout/restart/shutdown computer.') )
#    table.attach(o, 0, 1, pos, pos+1, gtk.FILL, gtk.FILL); pos += 1
    
    o = GConfCheckButton(_('Activate screen saver when computer is idle for long time'),
            '/apps/gnome-screensaver/idle_activation_enabled')
    table.attach(o, 0, 1, pos, pos+1, gtk.FILL, gtk.FILL); pos += 1
    
    o = GConfCheckButton(_('Lock screen when screen saver is activated'),
            '/apps/gnome-screensaver/lock_enabled')
    table.attach(o, 0, 1, pos, pos+1, gtk.FILL, gtk.FILL); pos += 1
    
    return Setting(table, _('GNOME session'), ['session'])

def __backlight():
    table = gtk.Table()
    table.set_col_spacings(10)
    table.set_row_spacings(5)
    label = gtk.Label(_('LCD brightness when on AC power:'))
    label.set_alignment(0, 0.5)
    label.set_tooltip_text( _('GConf Key: ') + '/apps/gnome-power-manager/backlight/brightness_ac' )
    o = GConfHScale( '/apps/gnome-power-manager/backlight/brightness_ac', 0, 100 )
    table.attach(label, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
    table.attach(o, 1, 2, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL)
    label = gtk.Label(_('LCD dimming amount when on battery:'))
    label.set_alignment(0, 0.5)
    label.set_tooltip_text( _('GConf Key: ') + '/apps/gnome-power-manager/backlight/brightness_dim_battery' )
    o = GConfHScale( '/apps/gnome-power-manager/backlight/brightness_dim_battery', 0, 100 )
    table.attach(label, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
    table.attach(o, 1, 2, 1, 2, gtk.FILL|gtk.EXPAND, gtk.FILL)
    return Setting(table, _('Backlight'), ['power'])

#def __suspend_and_hibernate():
#    vbox = gtk.VBox()
#    i = GConfCheckButton(_('Enable suspending function'),
#                '/apps/gnome-power-manager/lock/suspend')
#    j = GConfCheckButton(_('Enable hibernating function'),
#                '/apps/gnome-power-manager/lock/suspend')
#    vbox.pack_start(i, False)
#    vbox.pack_start(j, False)
#    return Setting(vbox, _('Suspending/hibernating funtion'), ['power'])

def __advance_setting():
    table = gtk.Table()
    table.set_col_spacings(10)    
    
    o = GConfCheckButton(_('Use your home folder as the desktop'),
                '/apps/nautilus/preferences/desktop_is_home_dir')
    table.attach(o, 0, 1, 0, 1, gtk.FILL, gtk.FILL)

    def clicked(button, path):
        if button.get_active():
            os.system('mkdir ~/.local/share/applications/')
            with open(path, 'w') as f:
                f.write('[Desktop Entry]\n'
                        'Name=Gnome Control Center\n'
                        'Exec=gnome-control-center\n'
                        'Icon=gnome-control-center\n'
                        'Terminal=false\n'
                        'Type=Application\n'
                        'Categories=System;')
        else:
            os.unlink(path)

    path = os.path.expanduser('~/.local/share/applications/gnome-control-center.desktop')
    button = gtk.CheckButton(_('Display "GNOME control center" entry in "System" menu'))
    button.set_tooltip_text(_('Create a file ~/.local/share/applications/gnome-control-center.desktop'))
    button.set_active(os.path.exists(os.path.expanduser('~/.local/share/applications/gnome-control-center.desktop')))
    button.connect('clicked', clicked, path)
    table.attach(button, 0, 1, 1, 2, gtk.FILL, gtk.FILL)

    o = label_left_align(_('Change default file manager to:'))
    table.attach(o, 0, 1, 2, 3, gtk.FILL, gtk.FILL)

    o = GConfTextEntry('/desktop/gnome/session/required_components/filemanager')
    table.attach(o, 1, 2, 2, 3, gtk.FILL, gtk.FILL )
    
    o = label_left_align(_('Change default panel program to:') )
    table.attach(o, 0, 1, 3, 4, gtk.FILL, gtk.FILL)
    
    o = GConfTextEntry('/desktop/gnome/session/required_components/panel')
    table.attach(o, 1, 2, 3, 4, gtk.FILL, gtk.FILL)
    
    o = label_left_align(_('Change default window manager to:') )
    table.attach(o, 0, 1, 4, 5, gtk.FILL, gtk.FILL)
    
    o = GConfTextEntry('/desktop/gnome/session/required_components/windowmanager')
    table.attach(o, 1, 2, 4, 5, gtk.FILL, gtk.FILL)

    return Setting(table, _('Advance settings'), ['desktop'])

def __shortcut_setting():
    l1 = gtk.Label(_('Command line'))
    l2 = gtk.Label(_('Shortcut key'))
    hbox = gtk.HBox(False, 0)
    hbox.pack_start(l1, False, False, 60)
    hbox.pack_start(gtk.Label(), True)
    hbox.pack_start(l2, False, False, 60)
    table = gtk.Table()
    table.set_col_spacings(5)
    table.attach(hbox, 0, 2, 0, 1, gtk.FILL|gtk.EXPAND, gtk.FILL)
    for number in range(1, 13):
        o = label_left_align(_('%2d:' % number))
        table.attach(o, 0, 1, number, number+1, gtk.FILL, gtk.FILL)
        o = GConfShortcutKeyEntry('command_%d' % number)
        table.attach(o, 1, 2, number, number+1, gtk.FILL|gtk.EXPAND, gtk.FILL)
    return Setting(table, _('Shortcut key'), ['shortcut'])

#def __gconfig_backup():
#    table = gtk.Table()
#    table.set_col_spacings(30)
#    table.set_row_spacings(10)
#    label = gtk.Label(_('Gconfig Settings are saved as XML files in the folder ~/.gconf, Ailurus can help you backup and reset this file.'))
#    backup_button = gtk.Button(_('Backup Gconfig Setting'))
#    def backup_gconf(w):
#        run('cd ~ && tar cvzf ~/.config/ailurus/gconfbackup.tar.gz /usr/share/gconf .gconf')
#    backup_button.connect('clicked', backup_gconf)
#    backup_button.set_tooltip_text(_("The backup file stored in ~/.config/ailurus/gconfbackup.tar.gz"))
#    recover_button = gtk.Button(_('Reset Gconfig Setting'))
#    def reset_gconf(w):
#        run('cd ~ && tar zxvf ~/.config/ailurus/gconfbackup.tar.gz .gconf')
#	run_as_root('cd / && tar zxvf ~/.config/ailurus/gconfbackup.tar.gz usr/share/gconf')
#	notify(_('Reset Successful'), _('Some Setting will be applied when you login next time.'))
#    recover_button.connect('clicked', reset_gconf)
#    import os
#    if not os.path.exists(os.path.expanduser('~/.config/ailurus/gconfbackup.tar.gz')):
#        recover_button.set_sensitive(False)
#    table.attach(label, 0, 2, 0, 1, gtk.FILL, gtk.FILL)
#    table.attach(backup_button, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
#    table.attach(recover_button, 1, 2, 1, 2, gtk.FILL, gtk.FILL)
#    return Setting(table, _("backup and rset Gconfig Setting"), ['desktop'])

#def __compiz_setting():
#    table = gtk.Table()
#    table.set_col_spacings(5)
#    table.set_row_spacings(10)
#    # Window Decorator    
#    label = gtk.Label(_('Set Window Decorator:'))
#    label.set_alignment(0, 0.5)
#    label.set_tooltip_markup(_("<span color='red'>It takes effect after next startup. "
#                               "If you are using Fedora, please run 'yum install fusion-icon' to install Fusion icons. "
#                               "Otherwise, this option does not work.</span>\n")
#                           + _('GConf key: ') + '/apps/compiz/plugins/decoration/allscreens/options/command')
#    hbox = gtk.HBox()
#    o = GConfComboBox('/apps/compiz/plugins/decoration/allscreens/options/command', 
#                      [_('Metacity'), _('Emerald')],
#                      ['/usr/bin/compiz-decorator', 'emerald --replace',] ) 
#    hbox.pack_start(label, False)
#    hbox.pack_start(o, False, True, 20)
#    table.attach(hbox, 0, 1, 0, 1, gtk.FILL, gtk.FILL)
#    # Compiz Effect    
#    def disable_minimize_effects(button):
#        import gconf
#        g = gconf.client_get_default()
#        value = []
#        g.set_list('/apps/compiz/plugins/animation/screen0/options/minimize_effects', gconf.VALUE_STRING, value)
#    def random_all_effects(button):
#        assert isinstance(button, gtk.Button)
#        import gconf
#        g = gconf.client_get_default()
#        g.set_bool('/apps/compiz/plugins/animation/screen0/options/all_random', True)
#    n = gtk.Button(_('Disable Minimize Effect'))
#    n.connect('clicked', disable_minimize_effects)
#    n.set_tooltip_text(_('GConf key: ')+'/apps/nautilus/list_view/default_visible_columns\n'
#                       'you can reset it in CompizConfig Settings Manager')
#    m = gtk.Button(_('Random All Effects'))
#    m.set_tooltip_text(_('GConf Key: ') + '/apps/compiz/plugins/animation/screen0/options/all_random\n'
#                       'All effects are chosen randomly, ignoring the selected effect. '
#                       'If None is selected for an event, that event won\'t be animated.')
#    m.connect('clicked', random_all_effects)
#    hbox = gtk.HBox()
#    hbox.pack_start(m, False)
#    hbox.pack_start(n, False, True, 20)
#    table.attach(hbox, 0, 1, 1, 2, gtk.FILL, gtk.FILL)
#    # number of desktop    
#    label = gtk.Label(_('Screen horizontal size coefficient'))
#    label.set_alignment(0, 0.5)
#    label.set_tooltip_text( _('GConf Key: ') + '/apps/compiz/general/screen0/options/hsize' )
#    o = GConfHScale( '/apps/compiz/general/screen0/options/hsize', 1, 32 )
#    table.attach(label, 0, 1, 2, 3, gtk.FILL, gtk.FILL)
#    table.attach(o, 1, 2, 2, 3, gtk.FILL|gtk.EXPAND, gtk.FILL)
#    label = gtk.Label(_('Screen vertical size coefficient'))
#    label.set_alignment(0, 0.5)
#    label.set_tooltip_text( _('GConf Key: ') + '/apps/compiz/general/screen0/options/vsize' )
#    o = GConfHScale( '/apps/compiz/general/screen0/options/vsize', 1, 32 )
#    table.attach(label, 0, 1, 3, 4, gtk.FILL, gtk.FILL)
#    table.attach(o, 1, 2, 3, 4, gtk.FILL|gtk.EXPAND, gtk.FILL)
#    
#    
#    return Setting(table, _('CompizConfig Settings'), ['window'])

def get():
    ret = []
    for f in [
            __desktop_icon_setting,
            __menu_icon_setting,
            __button_icon_setting,
            __start_here_icon_setting,
            __login_icon_setting,
            __font_size_setting,
            __window_behaviour_setting,
            __nautilus_thumbnail_setting,
            __gnome_splash_setting,
            __gnome_session_setting,
            __textbox_context_menu_setting,
            __disable_terminal_beep,
            __backlight,
            __advance_setting,
#            __suspend_and_hibernate,
            __restriction_on_current_user,
            __layout_of_window_titlebar_buttons,
            __more_nautilus_settings,
            __shortcut_setting,
#            __compiz_setting,
#            __gconfig_backup,
            ]:
        try:
            import gconf
            ret.append(f())
        except:
            print_traceback()
    return ret
