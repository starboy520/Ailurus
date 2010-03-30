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

import gtk
import sys
import os
from lib import *

class CleanUpPane(gtk.VBox):
    name = _('Clean up')
    
    def __init__(self, main_view):
        gtk.VBox.__init__(self, False, 10)
        self.pack_start(self.clean_apt_cache_button(), False)
        self.pack_start(self.clean_ailurus_cache_button(), False)
        clean_kernel_box = CleanKernel()
        self.pack_start(clean_kernel_box, False)

    def get_folder_size(self, folder_path):
        is_string_not_empty(folder_path)
        size = get_output('du -bs ' + folder_path)
        size = int(size.split('\t', 1)[0])
        return derive_size(size)        

    def get_button_text(self, folder_name, folder_path):
        try:
            text = _('Clean %(folder_name)s. Free %(size)s disk space.') % {
                                   'folder_name' : folder_name,
                                   'size' : self.get_folder_size(folder_path) }
        except:
            text = _('Clean %s.' % folder_name)
        return text

    def clean_apt_cache_button(self):
        label = gtk.Label(self.get_button_text(_('APT cache'), '/var/cache/apt/archives'))
        button = gtk.Button()
        button.add(label)
        def __clean_up(button, label):
            gksudo('apt-get clean')
            label.set_text(self.get_button_text(_('APT cache'), '/var/cache/apt/archives'))
        button.connect('clicked', __clean_up, label)
        return button
    
    def clean_ailurus_cache_button(self):
        label = gtk.Label(self.get_button_text(_('Ailurus cache'), '/var/cache/ailurus'))
        button = gtk.Button()
        button.add(label)
        def __clean_up(button, label):
            gksudo('rm /var/cache/ailurus/* -rf')
            label.set_text(self.get_button_text(_('Ailurus cache'), '/var/cache/ailurus'))
        button.connect('clicked', __clean_up, label)
        return button

class CleanKernel(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, False, 10)
        self.current_kernel_version = self.get_current_kernel_version()
        self.version_to_packages = {} # map version to package names
        self.__regenerate_version_to_packages() # regenerate self.version_to_packages
        
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_NEVER)
        box = self.box = gtk.VBox(False, 10)
        check_button_list = self.check_button_list = []
        button_apply = self.button_apply = gtk.Button(_('Apply'))
        button_apply.set_sensitive(False)
        def apply(button_apply, check_button_list):
            remove_list = []
            for b in check_button_list:
                if b.get_active():
                    remove_list.extend(self.version_to_packages[b.kernel_version])
                    #b.destroy()
            if remove_list:
                APT.remove(*remove_list)
                self.__regenerate_version_to_packages()
                self.__refresh_gui()
            button_apply.set_sensitive(False)
        button_apply.connect('clicked', apply, check_button_list)
        self.__refresh_gui()
        scrolled_window.add_with_viewport(box)
        self.pack_start(scrolled_window)
        hbox = gtk.HBox()
        hbox.pack_end(button_apply, False)
        self.pack_start(hbox, False)
        
    def __regenerate_version_to_packages(self):
        import re
        
        self.version_to_packages.clear()
        pkgs = APT.get_installed_pkgs_set()
        kpkgs = [p for p in pkgs if p.startswith('linux-headers-') or p.startswith('linux-image-')]
        pattern = r'linux-(headers|image)-([0-9.-]+)'
        for p in kpkgs:
            match = re.search(pattern, p)
            if not match: continue
            version = match.group(2)
            if version.endswith('-'): version = version[:-1]
            if self.version_to_packages.has_key(version):
                self.version_to_packages[version].append(p)
            else:
                self.version_to_packages[version] = [p]
    
    def __refresh_gui(self):
        for b in self.check_button_list: b.destroy()
        def state_changed(check_button, button_apply):
            button_apply.set_sensitive(True)
        version_list = self.version_to_packages.keys()
        version_list.sort()
        for version in version_list:
            check_button = gtk.CheckButton(version)
            check_button.kernel_version = version
            self.box.pack_start(check_button, False)
            self.check_button_list.append(check_button)
            check_button.connect('toggled', state_changed, self.button_apply)
    
    def get_current_kernel_version(self):
        import re
        
        version = os.uname()[2]
        pattern = r'[0-9.-]+'
        match = re.search(pattern, version)
        if match: version = match.group(0)
        if version.endswith('-'): version = version[:-1]
        return version
        