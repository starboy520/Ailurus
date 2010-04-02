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
        self.pack_start(self.clean_recently_used_document_button(),False)
        reclaim_memory = Reclaim_memory()
        self.pack_start(reclaim_memory,False)
        clean_kernel_box = CleanKernel()
        self.pack_start(clean_kernel_box, False)

    def get_folder_size(self, folder_path):
        is_string_not_empty(folder_path)
        size = get_output('du -bs ' + folder_path)
        size = int(size.split('\t', 1)[0]) - 4096 # The size of an empty folder is 4096.
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
    
    def clean_recently_used_document_button(self):
        def clear(w):
            import os
            path = os.path.expanduser('~/.recently-used.xbel')
            if os.path.isfile(path):
                os.system("echo '' > ~/.recently-used.xbel")
            else: # is dir
                os.system("rm ~/.recently-used.xbel/* -rf")
        button = gtk.Button(_('Clear "recent documents" list'))
        button.connect('clicked', clear)
        return button

class  Reclaim_memory(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self, False, 10)
#        self.set_border_width(10)
        box = gtk.HBox(False, 10)
        button_free_memory = gtk.Button( _('Reclaim memory').center(30) )
        button_free_memory.set_tooltip_text(
                                            _('Reclaim memory which stores pagecache, dentries and inodes.\nThis operation is done by "echo 3 >/proc/sys/vm/drop_caches"') )
        button_free_memory.connect('clicked', self.free_memory)
    
        label_info = gtk.Label()
        import gobject
        gobject.timeout_add(5000, self.show_cached_memory_amount, label_info)
    
        box.pack_start(button_free_memory, False)
        box.pack_start(label_info, False)
        self.pack_start(box, False, False)
        
    def show_cached_memory_amount(self,label):
        try:
            with open('/proc/meminfo') as f:
                for line in f:
                    if line.startswith('Cached:'): 
                        List = line.split()
                        value = int(List[1])
                        break
            label.set_text( _('No more than %s KB of memory can be reclaimed.') % value )
        except:
            import traceback
            traceback.print_exc()
    
        return True
        
    def get_free_memory(self):
        with open('/proc/meninfo') as f:
            for line in f:
                if not line.startswith('MemFree:'): continue
                List = line.split()
            return int(List[1])
        
    def free_memory(self,*w):
        dest = '/proc/sys/vm/drop_caches'
        import os, tempfile
        if os.path.exists(dest):
            before = self.get_free_memory()
        
            src = tempfile.NamedTemporaryFile('w')
            src.write('3\n')
            src.flush()
            gksudo('cp %s %s'%(src.name, dest) )
            after = self.get_free_memory()
            amount = max(0, after - before)
            notify( _('%s KB memory was reclaimed.')%amount, ' ')
            
class CleanKernel(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, False, 10)
        self.version_to_packages = {} # map version to package names
        self.__regenerate_version_to_packages() # regenerate self.version_to_packages
        
        check_buttons_box = self.check_buttons_box = gtk.VBox(False, 5) # put all check buttons in this box
        check_buttons_list = self.check_buttons_list = [] # all check buttons
        button_apply = self.button_apply = gtk.Button(_('Remove Linux kernels'))
        button_apply.set_sensitive(False)
        button_apply.connect('clicked', self.remove_kernel)
        current_kernel_version = self.get_current_kernel_version()
        label = gtk.Label(_('Current Linux kernel version is %s') % current_kernel_version)
        label.set_alignment(0, 0.5)
        label2 = gtk.Label(_('All installed Linux kernels are:'))
        label2.set_alignment(0, 0.5)
        self.pack_start(label, False)
        self.pack_start(label2, False)
        self.__regenerate_check_buttons()
        self.pack_start(check_buttons_box, False)
        hbox = gtk.HBox()
        hbox.pack_start(button_apply, False)
        self.pack_start(hbox, False)
        
    def remove_kernel(self, button_apply):
        remove_list = []
        for button in self.check_buttons_list:
            if button.get_active() == False:
                remove_list.extend(self.version_to_packages[button.kernel_version])
        if remove_list:
            try:    APT.remove(*remove_list)
            except: pass
            self.__regenerate_version_to_packages()
            self.__regenerate_check_buttons()
        button_apply.set_sensitive(False)

    def __regenerate_version_to_packages(self):
        import re
        self.version_to_packages.clear()
        all_pkgs = APT.get_installed_pkgs_set()
        kernel_pkgs = [p for p in all_pkgs if p.startswith('linux-headers-') or p.startswith('linux-image-')]
        pattern = r'linux-(headers|image)-([0-9.-]+)'
        for p in kernel_pkgs:
            match = re.search(pattern, p)
            if not match: continue
            version = match.group(2)
            if version.endswith('-'): version = version[:-1]
            if self.version_to_packages.has_key(version):
                self.version_to_packages[version].append(p)
            else:
                self.version_to_packages[version] = [p]

    def check_button_toggled(self, check_button, button_apply):
        if check_button.get_active():
            check_button.label.set_markup("%s" % check_button.kernel_version)
        else:
            check_button.label.set_markup("<s>%s</s>" % check_button.kernel_version)
        button_apply.set_sensitive(True)
    
    def __regenerate_check_buttons(self):
        for button in self.check_buttons_box.get_children():
            self.check_buttons_box.remove(button)
        self.check_buttons_list = []
        version_list = self.version_to_packages.keys()
        version_list.sort()
        for version in version_list:
            label = gtk.Label(version)
            check_button = gtk.CheckButton()
            check_button.kernel_version = version
            check_button.label = label
            check_button.add(label)
            check_button.set_active(True)
            check_button.connect('toggled', self.check_button_toggled, self.button_apply)
            self.check_buttons_list.append(check_button)
            self.check_buttons_box.pack_start(check_button, False)
        self.check_buttons_box.show_all()
    
    def get_current_kernel_version(self):
        import re
        version = os.uname()[2]
        pattern = r'[0-9.-]+'
        match = re.search(pattern, version)
        if match: 
            version = match.group(0)
            if version.endswith('-'): version = version[:-1]
            return version
        else: 
            raise Exception, os.uname()[2]