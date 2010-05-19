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
import sys, os
from lib import *
from libapp import *

class DisableGetty(I):
    __doc__ = _('Deactivate Getty ( Ctrl+Alt+F2 ... F6 ), Ctrl+Alt+F1 is still activated')
    detail = _('Speed up Linux start up process. Free 2.5 MBytes memory. ')
    def installed(self):
        with Chdir('/etc/event.d/') as o:
            for i in range(2,7):
                with open('tty%s'%i) as f:
                    content = f.read()
                if 'exec /sbin/' in content: return False
            return True
    def install(self):
        with Chdir('/etc/event.d/') as o:
            for i in range(2,7):
                filename = 'tty%s'%i
                with open(filename) as f:
                    contents = f.readlines()
                for j, line in enumerate(contents):
                    if line.startswith('exec /sbin/'):
                        contents[j] = '#' + line[1:]
                with TempOwn(filename) as o:
                    with open(filename, 'w') as f:
                        f.writelines(contents)
    def remove(self):
        with Chdir('/etc/event.d/') as o:
            for i in range(2,7):
                filename = 'tty%s'%i
                with open(filename) as f:
                    contents = f.readlines()
                for j, line in enumerate(contents):
                    if line.startswith('#xec /sbin/'):
                        contents[j] = 'e' + line[1:]
                with TempOwn(filename) as o:
                    with open(filename, 'w') as f:
                        f.writelines(contents)
    def visible(self):
        return os.path.exists('/etc/event.d/')

class Disable_SELinux(I):
    __doc__ = _('Put Selinux in permissive mode, instead of enforcing mode.')
    def installed(self):
        with open('/etc/sysconfig/selinux') as f:
            c = f.read()
        if 'SELINUX=enforcing' in c: return False
        with open('/etc/selinux/config') as f:
            c = f.read()
        if 'SELINUX=enforcing' in c: return False
        return True
    def install(self):
        run_as_root_in_terminal('/usr/sbin/setenforce 0')
        for path in ['/etc/sysconfig/selinux', '/etc/selinux/config']:
            with TempOwn(path) as o:
                with open(path) as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    if 'SELINUX=enforcing' in line: lines[i] = 'SELINUX=permissive\n'
                with open(path, 'w') as f:
                    f.writelines(lines)
    def remove(self):
        run_as_root_in_terminal('/usr/sbin/setenforce 0')
        for path in ['/etc/sysconfig/selinux', '/etc/selinux/config']:
            with TempOwn(path) as o:
                with open(path) as f:
                    lines = f.readlines()
                for i, line in enumerate(lines):
                    if 'SELINUX=permissive' in line: lines[i] = 'SELINUX=enforcing\n'
                with open(path, 'w') as f:
                    f.writelines(lines)
        run_as_root_in_terminal('/usr/sbin/setenforce 1')

class Disable_Sudo(I):
    __doc__ = _('Disable "sudo". Prevent yourself from using "sudo".')
    def installed(self):
        return False
    def install(self):
        run_as_root_in_terminal(D+'../support/disable_sudo.py')
    def remove(self):
        pass

class Enable_Sudo(I):
    __doc__ = _('Enable "sudo"')
    detail = _('If you enabled "sudo" and you want to execute commands as root, '
               'you can type command "sudo COMMAND" instead of complicated command "su -c \'COMMAND\'". '
               '<span color="red">Due to restriction on filesystem permission, '
               'Ailurus cannot detect whether "sudo" is enabled.</span> ')
    def installed(self):
        return False
    def install(self):
        run_as_root_in_terminal(D+'../support/enable_sudo.py')
    def remove(self):
        pass

class Generic_Genome_Browser(I):
    __doc__ = _('Generic Genome Browser')
    detail = _('Generic Genome Browser is a combination of database and interactive web page '
               'for manipulating and displaying annotations on genomes.\n'
               '<span color="red">Due to the limitation of the authors\' programming ability, '
               '"Generic Genome Browser" cannot be detected or removed by Ailurus.</span>')
    license = AL
    category='biology'
    def install(self):
        for package in ['perl-libwww-perl', 'perl-CPAN']:
            if not RPM.installed(package):
                RPM.install(package)
        
        f = R('http://gmod.svn.sourceforge.net/viewvc/gmod/Generic-Genome-Browser/trunk/bin/gbrowse_netinstall.pl').download()
        run_as_root_in_terminal('perl ' + f)
    def installed(self):
        return False
    def remove(self):
        raise NotImplementedError
