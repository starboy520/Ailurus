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
        if UBUNTU or MINT:
            self.pack_start(self.clean_apt_cache_button(), False)
            self.pack_start(UbuntuCleanKernelBox(), False)
        elif FEDORA:
            self.pack_start(self.clean_rpm_cache_button(), False)
        elif ARCHLINUX:
            self.pack_start(self.clean_pacman_cache_button(), False)

    def get_folder_size(self, folder_path, please_return_integer = False):
        is_string_not_empty(folder_path)
        if os.path.exists(folder_path):
            size = get_output('du -bsS ' + folder_path)
            fsize = os.stat(folder_path).st_size
            size = int(size.split('\t', 1)[0]) - fsize # get all file size in folder, not folder size
        else:
            size = 0
        if please_return_integer: return size
        else: return derive_size(size)

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
        button.set_sensitive(bool(self.get_folder_size('/var/cache/apt/archives',please_return_integer=True)))
        def __clean_up(button, label):
            notify(' ', 'apt-get clean')
            try: run_as_root_in_terminal('apt-get clean')
            except AccessDeniedError: pass
            label.set_text(self.get_button_text(_('APT cache'), '/var/cache/apt/archives'))
            button.set_sensitive(bool(self.get_folder_size('/var/cache/apt/archives',please_return_integer=True)))
        button.connect('clicked', __clean_up, label)
        button.set_tooltip_text(_('Command:') + ' sudo apt-get clean')
        return button
    
    def clean_rpm_cache_button(self):
        label = gtk.Label(self.get_button_text(_('RPM cache'), '/var/cache/yum/'))
        button = gtk.Button()
        button.add(label)
        button.set_sensitive(bool(self.get_folder_size('/var/cache/yum/',please_return_integer=True)))
        def __clean_up(button, label):
            notify(' ', "yum --enablerepo='*' clean all")
            try: run_as_root("yum --enablerepo='*' clean all")
            except AccessDeniedError: pass
            label.set_text(self.get_button_text(_('RPM cache'), '/var/cache/yum/'))
            button.set_sensitive(bool(self.get_folder_size('/var/cache/yum/',please_return_integer=True)))
        button.connect('clicked', __clean_up, label)
        button.set_tooltip_text(_("Command:") + " yum --enablerepo='*' clean all")
        return button
    
    def clean_ailurus_cache_button(self):
        label = gtk.Label(self.get_button_text(_('Ailurus cache'), '/var/cache/ailurus'))
        button = gtk.Button()
        button.add(label)
        button.set_sensitive(bool(self.get_folder_size('/var/cache/ailurus',please_return_integer=True)))
        def __clean_up(button, label):
            notify(' ', 'rm /var/cache/ailurus/* -rf')
            try: run_as_root('rm /var/cache/ailurus/* -rf')
            except AccessDeniedError: pass
            label.set_text(self.get_button_text(_('Ailurus cache'), '/var/cache/ailurus'))
            button.set_sensitive(bool(self.get_folder_size('/var/cache/ailurus',please_return_integer=True)))
        button.connect('clicked', __clean_up, label)
        button.set_tooltip_text(_('Command:') + ' sudo rm /var/cache/ailurus/* -rf')
        return button
    
    def clean_pacman_cache_button(self):
        label = gtk.Label(self.get_button_text(_('Pacman cache'), '/var/cache/pacman/pkg'))
        button = gtk.Button()
        button.add(label)
        button.set_sensitive(bool(self.get_folder_size('/var/cache/pacman/pkg',please_return_integer=True)))
        def __clean_up(button, label):
            notify(' ', 'rm -rf /var/cache/pacman/pkg/*')
            try: run_as_root('rm -rf /var/cache/pacman/pkg/*') #"pacman -Sc" does not work
            except AccessDeniedError: pass
            label.set_text(self.get_button_text(_('Pacman cache'), '/var/cache/pacman/pkg'))
            button.set_sensitive(bool(self.get_folder_size('/var/cache/pacman/pkg',please_return_integer=True)))
        button.connect('clicked', __clean_up, label)
        button.set_tooltip_text(_('Command:') + ' rm -rf /var/cache/pacman/pkg/*') #sudo pacman -Sc
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
        button.set_tooltip_text(_('Command:') + ' echo "" > ~/.recently-used.xbel')
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

class UbuntuCleanKernelBox(gtk.HBox):
    def version_of_current_kernel(self):
        return os.uname()[2]
    
    def refresh(self):
        self.unused_kernels = []
        import glob, re
        for file_name in glob.glob('/boot/vmlinuz-*'):
            match = re.search(r'vmlinuz-(.+(-[a-z]+)?)', file_name)
            if not match: continue
            version = match.group(1)
            if version == self.version_of_current_kernel(): continue
            self.unused_kernels.append(version)
        self.unused_kernels.sort()
    
        self.liststore.clear()
        for version in self.unused_kernels:
            self.liststore.append([True, version, self.get_size(version)])
        
        self.button_delete.set_sensitive(False)
        
    def get_size(self, version):
        import glob
        files = glob.glob('/boot/*%s*' % version) + glob.glob('/lib/modules/%s' % version)
        ret = 0
        for file in files:
            ret += os.stat(file).st_size
        return ret
    
    def text_data_func(self, column, cell, model, iter):
        keep = model.get_value(iter, 0)
        version = model.get_value(iter, 1)
        size = model.get_value(iter, 2)
        markup = '<b>%s</b>\n%s' % (version, derive_size(size))
        if not keep:
            markup += ' ' + _('will be removed')
        cell.set_property('markup', markup)
    
    def toggled(self, render_toggle, path):
        self.liststore[path][0] = not self.liststore[path][0]
        sensitive = False
        for row in self.liststore:
            keep = row[0]
            sensitive = sensitive or not keep
        self.button_delete.set_sensitive(sensitive)
    
    def delete_kernel(self):
        for row in self.liststore:
            keep = row[0]
            if keep: continue
            version = row[1]
            import re
            pure_version = re.match('[0-9.-]+', version).group(0)
            if pure_version.endswith('-'): pure_version = pure_version[:-1]
            to_remove = [p for p in APT.get_installed_pkgs_set() if pure_version in p]
            try:
                if to_remove:
                    APT.remove(*to_remove)
                run_as_root('rm -rf /boot/*%s*' % version)
                run_as_root('rm -rf /lib/modules/%s' % version)
            except:
                import traceback
                traceback.print_exc()
        self.refresh()
    
    def __init__(self):
        self.liststore = gtk.ListStore(bool, str, long) #keep?, version, disk space cost
        render_keep = gtk.CellRendererToggle()
        render_keep.connect('toggled', self.toggled)
        column_keep = gtk.TreeViewColumn()
        column_keep.pack_start(render_keep, False)
        column_keep.add_attribute(render_keep, 'active', 0)
        render_text = gtk.CellRendererText()
        column_text = gtk.TreeViewColumn(_('Unused Linux kernels'))
        column_text.pack_start(render_text, True)
        column_text.set_cell_data_func(render_text, self.text_data_func)
        self.view = view = gtk.TreeView(self.liststore)
        view.append_column(column_keep)
        view.append_column(column_text)
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_NEVER)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        scroll.add(view)
        
        self.button_delete = button_delete = gtk.Button(stock = gtk.STOCK_DELETE)
        button_delete.connect('clicked', lambda *w: self.delete_kernel())
        align = gtk.Alignment(0, 0.5)
        align.add(button_delete)

        gtk.HBox.__init__(self, False, 10)
        self.pack_start(scroll)
        self.pack_start(align, False)
        
        self.refresh()
