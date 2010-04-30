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

class TeXLive2009(I):
    __doc__ = _('TeXLive 2009')
    detail = _('TeXLive is obtained from http://www.tug.org/texlive/')
    category = 'latex'
    license = ('all the material in TeX Live may be freely used, copied, '
               'modified, and redistributed, subject to the sources remaining freely available. '
               'See http://www.tug.org/texlive/copying.html')
    def install(self):
        import os
        #prepare xzdec
        if get_arch() == 32:
            xzdec = R(['http://www.tug.org/texlive/xz/xzdec.i386-linux'],
               69556, '974f3ddeae66d34c5e5de3c7cd9651f249e677e7').download()
        else:
            xzdec = R(['http://www.tug.org/texlive/xz/xzdec.x86_64-linux'],
               73856, '0272dce41fdf2d3da1eeda6574238a1ed18e05d6').download()
        import os, stat
        os.chmod(xzdec, stat.S_IRWXU)
        #download iso.xz
        isoxz = R([
'http://ftp.ctex.org/mirrors/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',
'ftp://ftp.comp.hkbu.edu.hk/pub/TeX/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',
'ftp://ftp.jaist.ac.jp/pub/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',
'ftp://ftp.fu-berlin.de/tex/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',
'ftp://ftp.chg.ru/pub/TeX/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',
'ftp://carroll.aset.psu.edu/pub/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',],
1481859808,
).download()
        #extract
        print _('Unpacking ... Please wait for a few minutes.')
        #do not use 'run' or 'gksudo'
        print '%s %s > /tmp/texlive.iso'%(xzdec, isoxz)
        assert os.system('%s %s > /tmp/texlive.iso'%(xzdec, isoxz) ) == 0
        #mount
        if not os.path.exists('/mnt/texlive'):
            run_as_root("mkdir /mnt/texlive")
        run_as_root("mount -o iocharset=utf8,loop /tmp/texlive.iso /mnt/texlive")
        #launch install-tl
        import tempfile
        temp = tempfile.NamedTemporaryFile(mode='w')
        temp.write("I\n") # Do not establish symbolic links in /usr/bin/ since TeXLive 
        temp.flush()
        
        run_as_root_in_terminal('/mnt/texlive/install-tl < %s\n' % temp.name)
        run_as_root("umount /mnt/texlive")
        run_as_root("rmdir /mnt/texlive", ignore_error=True)
        #setup environment variables
        env = ETCEnvironment()
        if get_arch()==32:
            binpath = "/usr/local/texlive/2009/bin/i386-linux"
        else:
            binpath = "/usr/local/texlive/2009/bin/x86_64-linux" 
        env.add('PATH', binpath)
        env.add('MANPATH', '/usr/local/texlive/2009/texmf/doc/man')
        env.add('INFOPATH', '/usr/local/texlive/2009/texmf/doc/info')
        env.save()
        notify(_('TeXLive is installed.'), _('TeXLive will not work until you restart the computer.'))
    def installed(self):
        import os
        return os.path.exists('/usr/local/texlive/2009/')
    def remove(self):
        run_as_root('rm -rf /usr/local/texlive/2009/')
        #remove environment variables
        env = ETCEnvironment()
        if get_arch()==32:
            binpath = "/usr/local/texlive/2009/bin/i386-linux"
        else:
            binpath = "/usr/local/texlive/2009/bin/x86_64-linux" 
        env.remove('PATH', binpath)
        env.remove('MANPATH', '/usr/local/texlive/2009/texmf/doc/man')
        env.remove('INFOPATH', '/usr/local/texlive/2009/texmf/doc/info')
        env.save()

class TsingHuaTeXTemplate(_download_one_file):
    __doc__ = _('LaTeX Thesis Templates by Tsing Hua University, China')
    import os
    detail = _('These templates include undergraduate dissertation template, master thesis template and PhD thesis template. '
       'They are developed by Tsing Hua University, China. Official website is http://thuthesis.sourceforge.net/\n'
       'After installation, a file "thuthesis.tgz" is placed in the folder "%s".')%os.environ['HOME']
    category = 'latex'
    Chinese = True
    license = 'GPL'
    def __init__(self):
        self.R = R(
['http://thuthesis.googlecode.com/files/thuthesis-4.5.1.tgz'],
9101319, '7f617b66479cafe7c01b7b104e0392a947a064ef')
        import os
        self.file = os.path.expandvars('$HOME/thuthesis.tgz')

