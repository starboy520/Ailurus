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

class VIM_and_VIMRC(_rpm_install) :
    __doc__ = _('Make VIM more suitable for programming')
    detail = _('Install VIM and make it more suitable for programming. '
       'The installation process is as follows. '
       '"yum install vim-enhanced" command is executed. '
       'Then these lines are appended into "$HOME/.vimrc" file: \n'
       '    syntax on\n    set autoindent\n    set number\n    set mouse=a')
    license = GPL
    category = 'dev'
    if FEDORA:
        pkgs = 'vim-enhanced'
        def __vimrc_installed(self):
            return file_contain ( self.vimrc, *self.lines )
        def __vimrc_install(self):
            file_append ( self.vimrc, *self.lines )
        def __init__(self):
            import os
            self.vimrc = os.path.expanduser("~/.vimrc")
            self.lines = [ 'syntax on', 'set autoindent', 'set number', 'set mouse=a' ]
        def install(self):
            _rpm_install.install(self)
            self.__vimrc_install()
        def installed(self):
            return _rpm_install.installed(self)
        def remove(self):
            _rpm_install.remove(self)
            file_remove ( self.vimrc, *self.lines )

if FEDORA:
    class CommonUsedProgrammingPackages(_rpm_install):
        __doc__ = _('Useful applications for programming')
        detail = _('The tools are:\n'
           '<i>'
           'gcc: GNU C compiler.\n'
           'gcc-c++: GNU C++ compiler.\n'
           'ctags: source code parser used in vi and emacs, which allow moving to the definition of a symbol.\n'
           'gmp-devel: GNU multiprecision arithmetic library.\n'
           'ncurses-devel: a library controlling writing to the console screen.\n'
           'qt3-devel: Trolltech Qt library, version 3.\n'
           'subversion: a version control system.\n'
           'git: a distributed version control system.'
           '</i>')
        category = 'dev'
        pkgs = ('gcc gcc-c++ ctags gmp-devel ncurses-devel '
                'qt3-devel subversion git')

