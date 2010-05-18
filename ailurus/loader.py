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

def check_class_members(app_class, default_category = 'tweak'):
    import types
    if type(app_class)!=types.ClassType: raise TypeError, app_class
    if not hasattr(app_class,'category'): app_class.category = default_category
    if type( getattr(app_class,'category','') ) != str: raise TypeError, app_class
    if not app_class.category in categories: raise ValueError, app_class.category
    if not hasattr(app_class, 'detail'): app_class.detail=''
    if type( getattr(app_class,'detail','') ) != str: app_class.detail = str( getattr(app_class,'detail','') ) 
    if app_class.__doc__ is None: app_class.__doc__ = app_class.__name__
    return app_class

def load_app_icon(name):
    import os
    for dir in [Config.get_config_dir(), 'other_icons/', 'appicons/', ]:
        path = D + dir + name + '.png'
        if os.path.exists(path): break
    else:
        path = D + 'velly_icons/software_default_icon.png'
    import gtk
    return gtk.gdk.pixbuf_new_from_file_at_size(path, 24, 24)

def load_app_objs(common, desktop, distribution):
    modules = []
    for module in [common, desktop, distribution]:
        import types
        assert module==None or isinstance(module, types.ModuleType)
        if module and hasattr(module, 'apps'):
            modules.append(module.apps)

    objs = []
    names = set()
    for module in modules:
        for name in dir(module):
            if name in names: continue
            if name[0]=='_' or name=='I' or name=='N': continue
            app_class = getattr(module,name)
            if not isinstance(app_class, types.ClassType) or not issubclass(app_class, I): continue
    
            try:
                check_class_members(app_class)
                app_class_obj = app_class()
                app_class_obj.self_check()
                if hasattr(app_class_obj, 'visible') and app_class_obj.visible()==False: continue
                if hasattr(app_class_obj, 'Chinese') and Config.is_Chinese_locale()==False: continue
                if hasattr(app_class_obj, 'installation_command'):
                    if app_class_obj.detail and not app_class_obj.detail.endswith('\n'):
                        app_class_obj.detail += '\n'
                    app_class_obj.detail += app_class_obj.installation_command()
                app_class_obj.cache_installed = app_class_obj.installed()
                if not isinstance(app_class_obj.cache_installed, bool):
                    raise ValueError, 'Return type of installed() is not bool.'
                app_class_obj.showed_in_toggle = app_class_obj.cache_installed
                app_class_obj.logo_pixbuf = load_app_icon(name)
                objs.append(app_class_obj)
                names.add(name)
            except:
                print 'Cannot load class %s' % name
                print_traceback()

    return objs

def load_app_objs_from_extension(extension):
    from ailurus.lib import I
    import types
    classobjs = []
    names = set()
    for name in dir(extension):
        if name[0]=='_' or name=='I' or name=='N': continue
        if name in names: continue
        app_class = getattr(extension,name)
        if not isinstance(app_class, types.ClassType) or not issubclass(app_class, I): continue

        try:
            check_class_members(app_class)
            app_class_obj = app_class()
            app_class_obj.self_check()
            if hasattr(app_class_obj, 'visible') and app_class_obj.visible()==False: continue
            if hasattr(app_class_obj, 'international') and Config.is_Chinese_locale(): continue
            if hasattr(app_class_obj, 'Chinese') and Config.is_Chinese_locale()==False: continue
            app_class_obj.cache_installed = app_class_obj.installed()
            if not isinstance(app_class_obj.cache_installed, bool):
                raise ValueError, 'Return type of installed() is not bool.'
            app_class_obj.logo_pixbuf = load_app_icon(name)
            app_class_obj.showed_in_toggle = app_class_obj.cache_installed
            names.add(name)
        except:
            print 'Cannot load class %s' % name
            print_traceback()
        else:
            classobjs.append(app_class_obj)

    return classobjs

def load_custom_app_classes():
    return_value = []
    # check whether the extension directory exist
    import os
    extension_path = Config.get_config_dir()
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
            return_value.extend( load_app_objs_from_extension(module) )
        except:
            print_traceback()
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

def load_study_linux_menu(common, desktop, distribution):
    import types
    for module in [common, desktop, distribution]:
        assert isinstance(module, types.ModuleType) or module == None
    
    ret = []
    for module in [common, desktop, distribution]:
        if module and hasattr(module, 'menu') and hasattr(module.menu, 'get_study_linux_menu'):
            ret.extend(module.menu.get_study_linux_menu())
    return __create_menu(ret)

def load_preferences_menu(common, desktop, distribution):
    import types
    for module in [common, desktop, distribution]:
        assert isinstance(module, types.ModuleType) or module == None
    
    ret = []
    for module in [common, desktop, distribution]:
        if module and hasattr(module, 'menu') and hasattr(module.menu, 'get_preferences_menu'):
            ret.extend(module.menu.get_preferences_menu())
    return __create_menu(ret)

def load_others_menu(common, desktop, distribution):
    import types
    for module in [common, desktop, distribution]:
        assert isinstance(module, types.ModuleType) or module == None
    
    ret = []
    for module in [distribution, common, desktop]: # not [common, desktop, distribution]. Because we show "quick setup" first.
        if module and hasattr(module, 'menu') and hasattr(module.menu, 'get_others_menu'):
            ret.extend(module.menu.get_others_menu())
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

def load_cure_objs(common, desktop, distribution):
    modules = []
    for module in [common, desktop, distribution]:
        import types
        assert module==None or isinstance(module, types.ModuleType)
        if module and hasattr(module, 'cure'):
            modules.append(module.cure)
    
    objs = []
    names = set()
    for module in modules:
        for name in dir(module):
            if name in names or name == 'C': continue
            cure_class = getattr(module,name)
            if not isinstance(cure_class, types.ClassType) or not issubclass(cure_class, C): continue
            try:
                objs.append(cure_class())
            except:
                print 'Cannot load class %s' % name
                print_traceback()
    
    return objs

if __name__ == '__main__':
    import common
    print load_cure_objs(common, None, None)