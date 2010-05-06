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
import sys
import os
from lib import *

class CleanUpPane(gtk.VBox):
    name = _('Clean up')
    
    def __init__(self, main_view):
        gtk.VBox.__init__(self, False, 10)
        self.pack_start(self.clean_recently_used_document_button(),False)
        self.pack_start(ReclaimMemoryBox(),False)
        self.pack_start(self.clean_ailurus_cache_button(), False)
        if Config.is_Ubuntu() or Config.is_Mint():
            self.pack_start(self.clean_apt_cache_button(), False)
            self.pack_start(UbuntuCleanKernelBox(), False)
        elif Config.is_Fedora():
            self.pack_start(self.clean_rpm_cache_button(), False)

    def get_folder_size(self, folder_path):
        is_string_not_empty(folder_path)
        size = get_output('du -bsS ' + folder_path)
        import os
        fsize = os.stat(folder_path).st_size # Get folder size
        size = int(size.split('\t', 1)[0]) - fsize
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
            try: run_as_root('apt-get clean')
            except AccessDeniedError: pass
            label.set_text(self.get_button_text(_('APT cache'), '/var/cache/apt/archives'))
        button.connect('clicked', __clean_up, label)
        button.set_tooltip_text(_('Command: sudo apt-get clean'))
        return button
    
    def clean_rpm_cache_button(self):
        label = gtk.Label(self.get_button_text(_('RPM cache'), '/var/cache/yum/'))
        button = gtk.Button()
        button.add(label)
        def __clean_up(button, label):
            try: run_as_root("yum --enablerepo='*' clean all")
            except AccessDeniedError: pass
            label.set_text(self.get_button_text(_('RPM cache'), '/var/cache/yum/'))
        button.connect('clicked', __clean_up, label)
        button.set_tooltip_text(_("Command: yum --enablerepo='*' clean all"))
        return button
    
    def clean_ailurus_cache_button(self):
        label = gtk.Label(self.get_button_text(_('Ailurus cache'), '/var/cache/ailurus'))
        button = gtk.Button()
        button.add(label)
        def __clean_up(button, label):
            try: run_as_root('rm /var/cache/ailurus/* -rf')
            except AccessDeniedError: pass
            label.set_text(self.get_button_text(_('Ailurus cache'), '/var/cache/ailurus'))
        button.connect('clicked', __clean_up, label)
        button.set_tooltip_text(_('Command: sudo rm /var/cache/ailurus/* -rf'))
        return button
    
    def clean_recently_used_document_button(self):
        def clear(w):
            import os
            path = os.path.expanduser('~/.recently-used.xbel')
            if os.path.isfile(path):
                os.system("echo '' > ~/.recently-used.xbel")
            else: # is dir
                os.system("rm ~/.recently-used.xbel/* -rf")
            notify(' ', _('"Recent documents" list is empty now.'))
        button = gtk.Button(_('Clear "recent documents" list'))
        button.connect('clicked', clear)
        button.set_tooltip_text(_('Command: echo "" > ~/.recently-used.xbel'))
        return button

class ReclaimMemoryBox(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self, False, 10)
        button_free_memory = gtk.Button( _('Reclaim memory').center(30) )
        button_free_memory.set_tooltip_text(
                                            _('Reclaim memory which stores pagecache, dentries and inodes.\nThis operation is done by "echo 3 >/proc/sys/vm/drop_caches"') )
        button_free_memory.connect('clicked', self.free_memory)
    
        label_info = gtk.Label( _('No more than %s KB of memory can be reclaimed.') % 0 )
        import gobject
        gobject.timeout_add(5000, self.show_cached_memory_amount, label_info)
    
        self.pack_start(button_free_memory)
        self.pack_start(label_info, False)
        
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
        with open('/proc/meminfo') as f:
            for line in f:
                if not line.startswith('MemFree:'): continue
                return int(line.split()[1])
        
    def free_memory(self,*w):
        dest = '/proc/sys/vm/drop_caches'
        import os, tempfile
        if os.path.exists(dest):
            before = self.get_free_memory()
        
            src = tempfile.NamedTemporaryFile('w')
            src.write('3\n')
            src.flush()
            try: run_as_root('cp %s %s'%(src.name, dest) )
            except AccessDeniedError: pass
            after = self.get_free_memory()
            amount = max(0, after - before)
            notify( _('%s KB memory was reclaimed.')%amount, ' ')
            
class UbuntuCleanKernelBox(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self, False, 10)
        self.current_kernel_version = current_kernel_version = self.get_current_kernel_version()
        self.version_to_packages = {} # map version to package names
        self.__regenerate_version_to_packages() # regenerate self.version_to_packages
        
        check_buttons_box = self.check_buttons_box = gtk.VBox(False, 5) # put all check buttons in this box
        check_buttons_list = self.check_buttons_list = [] # all check buttons
        button_apply = self.button_apply = gtk.Button(_('Remove Linux kernels'))
        button_apply.set_sensitive(False)
        button_apply.connect('clicked', self.remove_kernel)
        label = gtk.Label(_('Current Linux kernel version is %s') % current_kernel_version)
        label.set_alignment(0, 0.5)
        label2 = gtk.Label(_('Not used Linux kernels are:'))
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
        delete_list = []
        for button in self.check_buttons_list:
            if button.get_active() == False:
                kernel_version = button.kernel_version
                pkgs = self.version_to_packages[kernel_version]
                if pkgs: 
                    remove_list.extend(pkgs)
                else:
                    delete_list.extend([
                            '/lib/modules/%s'%kernel_version, 
                            '/boot/System.map-%s'%kernel_version,
                            'config-%s'%kernel_version,
                            'initrd.img-%s'%kernel_version
                                        ])
        if remove_list:
            try:    APT.remove(*remove_list)
            except: pass
            self.__regenerate_version_to_packages()
            self.__regenerate_check_buttons()
        if delete_list:
            try:    run_as_root('rm -rf %s'%' '.join(delete_list))
            except AccessDeniedError: pass
            self.__regenerate_version_to_packages()
            self.__regenerate_check_buttons()
        button_apply.set_sensitive(False)

    def __regenerate_version_to_packages(self):
        import glob
        import re
        self.version_to_packages.clear()
        kernel_list = glob.glob('/boot/vmlinuz-*');
        pattern = r'vmlinuz-([0-9]+\.[0-9]+\.[0-9]+([-.])[0-9]+)'
        for p in kernel_list:
            match = re.search(pattern, p)
            if not match: continue
            version = match.group(1)
            if version == self.current_kernel_version:
                continue
            if match.group(2) == '-':
                pkgs = [
                        'linux-headers-%s'%version, 
                        'linux-headers-%s-generic'%version, 
                        'linux-image-%s-generic'%version, 
                        ]
            else:
                pkgs = None
            if self.version_to_packages.has_key(version):
                self.version_to_packages[version].extend(pkgs)
            else:
                self.version_to_packages[version] = pkgs

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
