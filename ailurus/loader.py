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
from lib import *

categories=('tweak','repository','biology','internet','firefox', 'firefoxdev',
            'appearance','office','math','latex','dev','em', 'server',
            'geography','education','media','vm','game', 'statistics', 
            'eclipse', 'hardware', 'language', 'nautilus', 'embedded',)

class BrokenClass(Exception):
    pass

def check_class_members(app_class, default_category = 'tweak'):
    import types
    if type(app_class)!=types.ClassType: raise TypeError, app_class
    if type( getattr(app_class,'install',None) ) != types.MethodType: raise BrokenClass, app_class
    if type( getattr(app_class,'installed',None) ) != types.MethodType: raise BrokenClass, app_class
    if type( getattr(app_class,'remove',None) ) != types.MethodType: raise BrokenClass, app_class
    if not hasattr(app_class,'category'): app_class.category = default_category
    if type( getattr(app_class,'category','') ) != str: raise TypeError, app_class
    if not app_class.category in categories: raise ValueError, app_class.category
    if not hasattr(app_class, 'detail'): app_class.detail=''
    if type( getattr(app_class,'detail','') ) != str: app_class.detail = str( getattr(app_class,'detail','') ) 
    if app_class.__doc__ is None: app_class.__doc__ = app_class.__name__
    return app_class

def load_app_classes(common, desktop, distribution):
    import lib
    modules = []
    for module in [common, desktop, distribution]:
        import types
        assert module==None or isinstance(module, types.ModuleType)
        if module and hasattr(module, 'apps'):
            modules.append(module.apps)

    classes = []
    names = set()
    for module in modules:
        for symbol in dir(module):
            if symbol[0]=='_': continue
            if symbol in dir(lib): continue
            app_class = getattr(module,symbol)
            if type(app_class)!=types.ClassType: continue
            if symbol in names: continue
    
            try:
                check_class_members(app_class)
                app_class_obj = app_class()
                if hasattr(app_class, 'support'):
                    if app_class_obj.support()==False: continue
                if hasattr(app_class, 'Chinese'): 
                    if Config.is_Chinese_locale()==False: continue
                if hasattr(app_class, 'installation_command'):
                    if app_class.detail and not app_class.detail.endswith('\n'):
                        app_class.detail += '\n'
                    app_class.detail += app_class_obj.installation_command()
                app_class.cache_installed = app_class_obj.installed()
                if not isinstance(app_class.cache_installed, bool):
                    raise ValueError, 'Return type of installed() is not bool.'
                app_class.showed_in_toggle = app_class.cache_installed
                names.add(symbol)
            except:
                import sys, traceback
                print >>sys.stderr, _('Cannot load class %s')%symbol
                print >>sys.stderr, _('Traceback:')
                traceback.print_exc(file=sys.stderr)
            else:
                classes.append(app_class)

    return classes

def _load_app_classes_from_module(module):
    import types
    classobjs = []
    names = set()
    for symbol in dir(module):
        if symbol[0]=='_': continue
        import lib
        if symbol in dir(lib): continue
        obj = getattr(module,symbol)
        if type(obj)!=types.ClassType: continue
        if symbol in names: continue

        try:
            check_class_members(obj)
            if not obj.category in categories:
                raise ValueError, obj.category
            if hasattr(obj, 'support'):
                if obj().support()==False: continue
            if hasattr(obj, 'international'): 
                if Config.is_Chinese_locale(): continue
            if hasattr(obj, 'Chinese'): 
                if Config.is_Chinese_locale()==False: continue
            obj.cache_installed = obj().installed()
            if not isinstance(obj.cache_installed, bool):
                raise ValueError, 'Return type of installed() is not bool.'
            obj.showed_in_toggle = obj.cache_installed
            names.add(symbol)
        except:
            import sys, traceback
            print >>sys.stderr, _('Cannot load class %s')%symbol
            print >>sys.stderr, _('Traceback:')
            traceback.print_exc(file=sys.stderr)
        else:
            classobjs.append(obj)

    return classobjs

def load_custom_app_classes():
    return_value = []
    # check whether the extension directory exist
    import os
    extension_path = Config.get_config_dir() + 'extension'
    if not os.path.exists(extension_path):
        return []
    # add the extension directory to sys.path
    import sys
    sys.path.insert(0, extension_path)
    # try to load extensions
    import glob
    pys = glob.glob(extension_path+'/*.py')
    for py in pys:
        filename = os.path.split(py)[1]
        basename = os.path.splitext(filename)[0]
        try:
            module = __import__(basename)
            return_value.extend( _load_app_classes_from_module(module) )
        except:
            import traceback
            traceback.print_exc()
    # remove the extension directory from sys.path
    sys.path.pop(0)
    return return_value

def load_R_objs(common, desktop, distribution):
    paths = []
    import types
    import os, glob, re
    for module in [common, desktop, distribution]:
        if module:
            assert isinstance(module, types.ModuleType)
            path = module.__name__
            assert os.path.exists(path)
            paths.append(path)
    
    files = []
    for path in paths:
        files += glob.glob(path+'/app*.py')
    
    objs = []
    for file in files:
        f = open(file)
        content = f.read()
        R_strs = re.findall(r'R\([^)]*\)', content)
        for s in R_strs:
            if '#' in s: continue #skip comment
            objs.append( eval(s) )
    
    return objs

def load_hardwareinfo(common, desktop, distribution):
    import types
    ret = []
    for module in [common, desktop, distribution]:
        if module:
            assert isinstance(module, types.ModuleType)
            if hasattr(module, 'hardwareinfo') and hasattr(module.hardwareinfo, 'get'):
                ret.extend(module.hardwareinfo.get())
    return ret

def load_linuxinfo(common, desktop, distribution):
    import types
    ret = []
    for module in [common, desktop, distribution]:
        if module:
            assert isinstance(module, types.ModuleType)
            if hasattr(module, 'osinfo') and hasattr(module.osinfo, 'get'):
                ret.extend(module.osinfo.get())
    return ret

def load_setting(common, desktop, distribution):
    import types
    ret = []
    for module in [distribution, desktop, common]:
        if module:
            assert isinstance(module, types.ModuleType)
            if hasattr(module, 'setting') and hasattr(module.setting, 'get'):
                ret.extend(module.setting.get())
    return ret

def __create_menu(menuitems):
    import gtk
    menu = gtk.Menu()
    for item in menuitems:
        menu.append(item)
    menu.show_all()
    return menu

def load_study_linux_menu(common, desktop, distribution, main_view):
    import types
    for module in [common, desktop, distribution]:
        assert isinstance(module, types.ModuleType) or module == None
    
    ret = []
    for module in [common, desktop, distribution]:
        if module and hasattr(module, 'menu') and hasattr(module.menu, 'get_study_linux_menu'):
            ret.extend(module.menu.get_study_linux_menu(main_view))
    return __create_menu(ret)

def load_preferences_menu(common, desktop, distribution, main_view):
    import types
    for module in [common, desktop, distribution]:
        assert isinstance(module, types.ModuleType) or module == None
    
    ret = []
    for module in [common, desktop, distribution]:
        if module and hasattr(module, 'menu') and hasattr(module.menu, 'get_preferences_menu'):
            ret.extend(module.menu.get_preferences_menu(main_view))
    return __create_menu(ret)

def load_others_menu(common, desktop, distribution, main_view):
    import types
    for module in [common, desktop, distribution]:
        assert isinstance(module, types.ModuleType) or module == None
    
    ret = []
    for module in [distribution, common, desktop]: # not [common, desktop, distribution]. Because we show "quick setup" first.
        if module and hasattr(module, 'menu') and hasattr(module.menu, 'get_others_menu'):
            ret.extend(module.menu.get_others_menu(main_view))
    return __create_menu(ret)

def load_tips(common, desktop, distribution):
    import types
    ret = []
    for module in [common, desktop, distribution]:
        if module:
            assert isinstance(module, types.ModuleType)
            if hasattr(module, 'tips') and hasattr(module.tips, 'get'):
                ret.extend(module.tips.get())
    return ret
