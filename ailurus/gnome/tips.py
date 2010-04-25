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
import sys, os
from lib import *

def get():
    return [
_('''~/.thumbnails/ directory is a cache dir GNOME makes when you browse through your folders in nautilus. 
It contains thumbnail pictures of picture files you've previously looked at.

You can get its total size by 
du -bs ~/.thumbnails/

You can delete the files in the .thumbnails directory that haven't been accessed for seven days, to free disk space.
find ~/.thumbnails/ -type f -atime +7 -exec rm {} \;
'''),

_("""Capture screen after 10 seconds
gnome-screenshot -d 10
Capture current window after 10 seconds
gnome-screenshot -wd 10
"""),

_('''Start GConf editor:
Press Alt+F2, type 'gconf-editor'.'''),

_('''GConf key:
/desktop/gnome/interface/menus_have_icons
If this is set to false, all icons in menu entries will be invisible.
'''),

_('''GConf key:
/apps/nautilus/preferences/show_desktop
If this is set to true, then icons on the desktop will be displayed. 
'''),

_('''GConf key:
/apps/nautilus/desktop/computer_icon_visible
If this is set to true, an icon linking to the computer location will be put on the desktop. 

/apps/nautilus/desktop/computer_icon_name
The custom name for the computer icon on the desktop. 
'''),

_('''GConf key:
/apps/nautilus/desktop/home_icon_visible
If this is set to true, an icon linking to the home folder will be put on the desktop. 

/apps/nautilus/desktop/home_icon_name
The custom name for the home icon on the desktop. 
'''),

_('''GConf key:
/apps/nautilus/desktop/network_icon_visible
If this is set to true, an icon linking to the Network Servers view will be put on the desktop. 

/apps/nautilus/desktop/network_icon_name
Thes custom name for the network servers icon on the desktop. 
'''),

_('''GConf key:
/apps/nautilus/desktop/trash_icon_visible
If this is set to true, an icon linking to the trash will be put on the desktop. 

/apps/nautilus/desktop/trash_icon_name
The custom name for the trash icon on the desktop. 
'''),

_('''GConf key:
/apps/nautilus/desktop/volumes_visible
If this is set to true, icons linking to mounted volumes will be put on the desktop. 
'''),

_('''GConf key:
/apps/metacity/general/button_layout
Arrangement of buttons on the titlebar. 
The value should be a string, such as "menu:minimize,maximize,spacer,close". 
The visibility and position of titlebar buttons can be changed by this key.
'''),

_('''GConf key:
/apps/metacity/general/action_double_click_titlebar
This option determines the effects of double-clicking on the title bar,
such as shade/unshade the window, maximize/unmaximize the window,
maximize/unmaximize the window in horizontal direction only.
'''),

_('''GConf key:
/apps/nautilus/preferences/show_advanced_permissions
If set to true, then Nautilus lets you edit and display file permissions in a more unix-like way, 
accessing some more esoteric options. 
'''),

_('''GConf key:
/apps/metacity/global_keybindings/
/apps/metacity/keybinding_commands/
Custom GNOME short-cut keys.

For example, to start 'gconf-editor' by pressing 'F12', you can set:
/apps/metacity/global_keybindings/run_command_1 = F12
/apps/metacity/keybinding_commands/command_1 = gconf-editor
'''),


_('''GConf key:
/desktop/gnome/background/picture_filename
File to use for the background image.
'''),

_('''GConf key:
/apps/gedit-2/preferences/editor/undo/max_undo_actions
Maximum number of actions that gedit will be able to undo or redo. Use "-1" for unlimited number of actions.'''),

_('''GConf key:
/apps/gedit-2/preferences/ui/recents/max_recents
Specifies the maximum number of recently opened files that will be displayed in the "Recent Files" submenu.'''),

_('''GConf key:
/apps/file-roller/general/compression_level
Compression level used when adding files to an archive.'''),

_('GConf key:\n'
'/apps/gnome-session/options/auto_save_session\n'
'If its value is true, GNOME will remember the running applications when you log out, '
'and re-launch these applications at the next time you log in to GNOME.'
),

_('GConf key:\n'
'/apps/gnome-session/options/show_splash_screen\n'
'If its value is true, a splash image is displayed after you log in to GNOME.\n'
'\n'
'/apps/gnome-session/options/splash_image\n'
'The file which is used as the splash image.'
),

_('GConf key:\n'
'/desktop/gnome/interface/show_input_method_menu\n'
'If its value is true, a "Change input method" entry is added in the context menu of all GTK text-boxes, including GEdit.'
),

_('GConf key:\n'
'/desktop/gnome/interface/show_unicode_menu\n'
'If its value is true, an "Insert Unicode control characters" entry is added in the context menu of all GTK text-boxes, including GEdit.'),

_('GConf key:\n'
'/apps/nautilus/preferences/show_advanced_permissions\n'
'If its value is true, Nautilus lets you edit and display file permissions in a more unix-like way, accessing owner permissions, group premissions and other permissions.'),

_('GConf key:\n'
'/apps/nautilus/icon_view/thumbnail_size\n'
'The default size of an icon for a thumbnail in the Nautilus icon view.'),

_('GConf key:\n'
'/desktop/gnome/thumbnail_cache/maximum_size\n'
'Maximum size of the Nautilus thumbnail cache, in megabytes. -1 means unlimited size.'),

_('GConf key:\n'
'/desktop/gnome/thumbnail_cache/maximum_age\n'
'Maximum age for files in the Nautilus thumbnail cache, in days. -1 means unlimited age.'),

_('GConf key:\n'
'/desktop/gnome/lockdown/disable_command_line\n'
'Prevent yourself from pressing Alt+F2 to launch applications -_-\n') + _('This configuration does not affect other users.'),

_('GConf key:\n'
'/desktop/gnome/lockdown/disable_lock_screen\n'
'Prevent yourself from pressing Ctrl+Alt+L to lock screen -_-\n') + _('This configuration does not affect other users.'),

_('GConf key:\n'
'/desktop/gnome/lockdown/disable_printing\n'
'Prevent yourself from printing any documents -_-\n') + _('This configuration does not affect other users.'),

_('GConf key:\n'
'/desktop/gnome/lockdown/disable_print_setup\n'
'Prevent yourself from modifying print settings -_-\n') + _('This configuration does not affect other users.'),

_('GConf key:\n'
'/desktop/gnome/lockdown/disable_save_to_disk\n'
'Prevent yourself from using "Save as ..." dialog -_-\n') + _('This configuration does not affect other users.'),

_('GConf key:\n'
'/desktop/gnome/lockdown/disable_user_switching\n'
'Prevent yourself from switching to another account, unless you log out from GNOME first. -_-\n') + _('This configuration does not affect other users.'),
]
    