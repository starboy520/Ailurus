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

import sys, os
from applib import *
from lib import *

class ChangeTerminalColor(_set_gconf):
    __doc__ = _('Change background color of GNOME terminal to black.')
    detail = _('Set background color to black. Set foreground color to white.\n'
       'The trick is to change GConf values:\n'
       '/apps/gnome-terminal/profiles/Default/use_theme_colors = False\n'
       '/apps/gnome-terminal/profiles/Default/background_color = #000000000000\n'
       '/apps/gnome-terminal/profiles/Default/foreground_color = #FFFFFFFFFFFF')
    logo = 'terminal-color.png'
    def __init__(self):
        self.set=(
('/apps/gnome-terminal/profiles/Default/use_theme_colors',False,True), 
('/apps/gnome-terminal/profiles/Default/background_color','#000000000000','#FFFFFFFFFFFF'), 
('/apps/gnome-terminal/profiles/Default/foreground_color','#FFFFFFFFFFFF','#000000000000'),
                  )
        self.add=()

class Gedit_GB2312(_set_gconf) :
    __doc__ = _('Add GB2312 detection ability to GEdit')
    detail = _('The trick behind is to change GConf values:\n'
       '/apps/gedit-2/preferences/encodings/auto_detected += ["GB2312", "GBK", "GB18030"]\n'
       '/apps/gedit-2/preferences/encodings/shown_in_menu += ["GB2312"]')
    Chinese = True
    logo = 'gedit.png'
    def __init__(self):
        self.set = ()
        self.add = (
('/apps/gedit-2/preferences/encodings/auto_detected', [ 'GB2312', 'GBK', 'GB18030' ] ),
('/apps/gedit-2/preferences/encodings/shown_in_menu', [ 'GB2312' ] ),
                    )
    def get_reason(self, f):
        self._get_reason(f)

class Speedup_Nautilus(_set_gconf):
    __doc__ = _('Speed up Nautilus')
    detail = _('Change Nautilus settings: '
       'Do not count directory items. Do not preview sound. '
       'Do not show texts in icon. Use tighter layout. \n'
       'The trick behind is to change GConf settings as follows.\n'
       '/apps/nautilus/preferences/show_directory_item_counts = never\n'
       '/apps/nautilus/preferences/preview_sound = never\n'
       '/apps/nautilus/preferences/show_icon_text = never\n'
       '/apps/nautilus/icon_view/default_use_tighter_layout = true')
    logo = 'nautilus.png'
    def __init__(self):
        self.set=(
('/apps/nautilus/preferences/show_directory_item_counts','never','local_only'),
('/apps/nautilus/preferences/preview_sound','never','local_only'),
('/apps/nautilus/preferences/show_icon_text','never','local_only'),
('/apps/nautilus/icon_view/default_use_tighter_layout',True,False),
                  )
        self.add=()
    def get_reason(self, f):
        self._get_reason(f)

#class Gedit_Assembly_Highlight(_path_lists):
#    __doc__ = _('Assembly language syntax highlighting for GEdit')
#    detail = _('The trick behind is to put an XML file in ~/.gnome2/gedit/plugins/ \n'
#               'Welcome to improve syntax highlighting on https://bugzilla.gnome.org/show_bug.cgi?id=152267')
#    logo = 'gedit.png'
#    category = 'dev'
#    def __init__(self):
#        import os
#        self.file = '/usr/share/gtksourceview-2.0/language-specs/asm.lang'
#        self.paths = [ self.file ]
#    def install(self):
#        wget('http://bugzilla.gnome.org/attachment.cgi?id=45158&action=view', #'http://bugzilla-attachments.gnome.org/attachment.cgi?id=53422',
#             '/tmp/asm.lang')
#        gksudo("mv /tmp/asm.lang %s" % self.file)
