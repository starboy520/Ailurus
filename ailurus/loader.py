#coding: utf8
#
# Ailurus - a simple application installer and GNOME tweaker
#
# Copyright (C) 2009-2010, Ailurus developers and Ailurus contributors
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
from libapp import N
import os, sys, glob, new, ConfigParser, types, gtk, gobject
import strings

class AppConfigParser(ConfigParser.RawConfigParser):
    def getAppDict(self):
        ret = {}
        appobjs = []
        for section_name in self.sections():
            try:
                dict = {}
                if not self.custom:
                    assert hasattr(strings, section_name+'_0'), section_name
                    assert hasattr(strings, section_name+'_1'), section_name
                    dict['__doc__'] = getattr(strings, section_name + '_0')
                    dict['detail'] = getattr(strings, section_name + '_1')

                for option_name in self.options(section_name):
                    value = self.get(section_name, option_name)
                    if option_name == DISTRIBUTION:
                        dict['pkgs'] = value
                    elif option_name == 'Chinese' or option_name == 'Poland':
                        dict[option_name] = True
                    elif option_name == 'license':
                        list = [globals()[e] for e in value.split()]
                        if len(list)==1: dict[option_name] = list[0]
                        elif len(list)==2: dict[option_name] = DUAL_LICENSE(list[0],list[1])
                        elif len(list)==3: dict[option_name] = TRI_LICENSE(list[0],list[1],list[2])
                    else:
                        dict[option_name] = value
                if not self.custom:
                    if 'pkgs' not in dict.keys(): continue
                ret[section_name] = dict
#                obj = new.classobj(section_name, (N,), {})()
#                for key in dict.keys():
#                    setattr(obj,key,dict[key])
#                obj.self_check()
#                obj.fill()
            except:
                print 'Cannot load obj %s from native_apps' % section_name
                print_traceback()
#            else:
#                
#                appobjs.append(obj)
        return ret
    
    def save(self):
        try:
            with open(self.filepath, 'w') as f:
                self.write(f)
        except:
            print_traceback()
     
    def removeAppObjByName(self,classname):
        if not self.custom:
            return
        if classname in self.sections():
            self.remove_section(classname)
        self.save()
        
    def addAppObjFromDict(self,dict):
        objdict = dict.copy()
        if not self.custom:
            return
        classname = objdict.pop('classname')
        if not classname in self.sections():
            self.add_section(classname)
        for key in objdict.keys():
            self.set(classname, str(key), str(objdict[key]))
        self.save()

    def __init__(self, filepath):
        assert isinstance(filepath,str)

        ConfigParser.RawConfigParser.__init__(self)
        self.optionxform = str # case sensitive in option_name
        self.filepath = filepath
        if filepath.endswith('native_apps'):
            self.custom = False
        else:
            self.custom = True
        
        if os.path.exists(filepath):
            self.read(filepath)
        else:
            if self.custom:
                return
            else:
                raise Exception('File %s does not exist' % filepath)

    
NATIVE_APPS = AppConfigParser(A+'/native_apps')
CUSTOM_APPS = AppConfigParser(Config.get_config_dir() + 'custom_apps')

class AppObjs:
    appobjs = []
    appobjs_names = []
    basic_modules = [] # used in load_from_basic_modules()
    extensions = []
    failed_extensions = []
    list_store = gtk.ListStore(gobject.TYPE_PYOBJECT)
    @classmethod
    def add_new_appobj(cls, dict):
        objdict = dict.copy()
        section_name = objdict.pop('classname')
        obj = new.classobj(section_name, (N,), {})()
        for key in objdict.keys():
            if key == DISTRIBUTION:
                obj.pkgs = objdict[key]
            else:
                setattr(obj,key,objdict[key])
        obj.self_check()
        obj.fill()
        icon_path, obj.use_default_icon = cls.get_icon_path(section_name)
        obj.logo_pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icon_path, 32, 32)
        obj.showed_in_toggle = obj.cache_installed = obj.installed()
        cls.appobjs.append(obj)
        cls.list_store.append([obj])
    @classmethod
    def save_installed_items_to_file(cls, save_to_this_path):
        with open(save_to_this_path, 'w') as f:
            for obj in cls.appobjs:
                if obj.cache_installed and not obj.__class__.__name__.startswith('C_'): #custom package's class name startswith C_  such as C_12
                    class_name = obj.__class__.__name__
                    f.write(class_name + '\n')
    @classmethod
    def load_selection_state_from_file(cls, load_from_this_path):
        with open(load_from_this_path) as f:
            lines = f.readlines()
        names = [line.strip() for line in lines]
        names = set(names)
        for obj in cls.appobjs:
            class_name = obj.__class__.__name__
            if class_name in names:
                obj.showed_in_toggle = True
    @classmethod
    def get_icon_path(cls, name):
        'return (icon path, whether it is default icon)'
        path = D + 'appicons/' + name + '.png'
        path_custom = Config.get_config_dir() + name + '.png'
        if os.path.exists(path_custom): return (path_custom, False)
        if os.path.exists(path): return (path, False)
        return (D + 'sora_icons/default_application_icon.png', True)
    @classmethod
    def all_objs_reload_icon(cls):
        for obj in cls.appobjs:
            name = obj.__class__.__name__
            icon_path, obj.use_default_icon = cls.get_icon_path(name)
            obj.logo_pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icon_path, 32, 32)
    @classmethod
    def all_objs_reset_status(cls):
        failed = []
        for obj in cls.appobjs:
            try:
                obj.showed_in_toggle = obj.cache_installed = obj.installed()
            except:
                print_traceback()
                failed.append(obj)
        for o in failed:
            cls.appobjs.remove(o)
            iter = cls.list_store.get_iter_first()
            while iter:
                if cls.list_store.get_value(iter, 0) == o:
                    cls.list_store.remove(iter)
                    break
                iter = cls.list_store.iter_next(iter)
    @classmethod
    def set_basic_modules(cls, common, desktop, distribution):
        cls.basic_modules = []
        for module in [common, desktop, distribution]:
            if module and hasattr(module, 'apps'):
                cls.basic_modules.append(module.apps)
    @classmethod
    def load_from_basic_modules(cls):
        assert cls.basic_modules
        for module in cls.basic_modules:
            cls.load_from(module)
    @classmethod
    def load_from(cls, module):
        for name in dir(module):
            if name in cls.appobjs_names: continue
            if name.startswith('_') or name=='I' or name=='N': continue
            app_class = getattr(module,name)
            if not isinstance(app_class, types.ClassType): continue
            if getattr(app_class, 'this_is_an_installer', False) == False: continue
            try:
                if not isinstance(app_class.category, str): raise TypeError, app_class
                if not isinstance(app_class.detail, (str, unicode)): raise TypeError, app_class
                if app_class.__doc__ is None: app_class.__doc__ = app_class.__name__
                obj = app_class()
                obj.self_check()
                obj.fill()
            except:
                print 'Cannot load class %s' % name
                print_traceback()
            else:
                cls.appobjs.append(obj)
                cls.list_store.append([obj])
                cls.appobjs_names.append(name)
    @classmethod
    def all_installer_names_in_module(cls, module):
        ret = set()
        for name in dir(module):
            if name.startswith('_') or name=='I' or name=='N': continue
            app_class = getattr(module,name)
            if not isinstance(app_class, types.ClassType): continue
            if getattr(app_class, 'this_is_an_installer', False) == False: continue
            ret.add(name)
        return list(ret)
    @classmethod
    def all_installer_names_in_text_file(cls):
        ret = set()
        for section_name in NATIVE_APPS.sections():
            ret.add(section_name)
        for section_name in CUSTOM_APPS.sections():
            ret.add(section_name)
        return list(ret)
    @classmethod
    def get_extension_path(cls):
        for path in [A+'/../unfree/', Config.get_config_dir()]:
            if os.path.exists(path): return path
        raise Exception
    @classmethod
    def load_from_extensions(cls):
        extension_path = cls.get_extension_path()
        sys.path.insert(0, extension_path)
        for py in glob.glob(extension_path+'/*.py'):
            filename = os.path.split(py)[1]
            basename = os.path.splitext(filename)[0]
            try:
                module = __import__(basename)
                cls.extensions.append(module)
                print '[+] Extension OK:', basename
            except:
                cls.failed_extensions.append(os.path.abspath(py))
                print '[x] Extension FAIL:', basename
#                print_traceback()
            else:
                cls.load_from(module)
        sys.path.pop(0)
    @classmethod
    def load_from_text_file(cls):
        dict = NATIVE_APPS.getAppDict()
        dict2 = CUSTOM_APPS.getAppDict()
        for key in dict2.keys():
            if key in dict.keys():
                dict[key].update(dict2[key])
            else:
                dict[key] = dict2[key]
        for key in dict.keys():
            obj = new.classobj(key, (N,), {})()
            if 'hide' in dict[key].keys():
                continue
            for k in dict[key].keys():
                setattr(obj,k,dict[key][k])
            obj.self_check()
            obj.fill()
            cls.appobjs.append(obj)
            cls.list_store.append([obj])
    @classmethod
    def strip_invisible(cls):
        cls.appobjs = [obj for obj in cls.appobjs if obj.visible()]
        cls.list_store.clear()
        for obj in cls.appobjs:
            cls.list_store.append([obj])
    @classmethod
    def strip_wrong_locale(cls):
        changed = False
        if not Config.is_Chinese_locale():
            cls.appobjs = [obj for obj in cls.appobjs if not hasattr(obj, 'Chinese')]
            changed = True
        if not Config.is_Poland_locale():
            cls.appobjs = [obj for obj in cls.appobjs if not hasattr(obj, 'Poland')]
            changed = True
        if changed:
            cls.list_store.clear()
            for obj in cls.appobjs:
                cls.list_store.append([obj])

def load_R_objs():
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

def load_info():
    import types
    hardware_info = []
    os_info = []
    for module in [common, desktop, distribution]:
        if module:
            assert isinstance(module, types.ModuleType)
            if hasattr(module, 'hardwareinfo') and hasattr(module.hardwareinfo, 'get'):
                hardware_info.extend(module.hardwareinfo.get())
            if hasattr(module, 'osinfo') and hasattr(module.osinfo, 'get'):
                os_info.extend(module.osinfo.get())
    return hardware_info, os_info
    
def load_setting():
    import types
    ret = []
    for module in [distribution, desktop, common]:
        if module:
            assert isinstance(module, types.ModuleType)
            if hasattr(module, 'setting') and hasattr(module.setting, 'get'):
                ret.extend(module.setting.get())
    return ret

def load_study_linux_menuitems():
    import types
    for module in [common, desktop, distribution]:
        assert isinstance(module, types.ModuleType) or module == None
    
    ret = []
    for module in [common, desktop, distribution]:
        if module and hasattr(module, 'menu') and hasattr(module.menu, 'get_study_linux_menu'):
            ret.extend(module.menu.get_study_linux_menu())
    return ret

def load_preferences_menuitems():
    import types
    for module in [common, desktop, distribution]:
        assert isinstance(module, types.ModuleType) or module == None
    
    ret = []
    for module in [common, desktop, distribution]:
        if module and hasattr(module, 'menu') and hasattr(module.menu, 'get_preferences_menu'):
            ret.extend(module.menu.get_preferences_menu())
    return ret

def load_others_menuitems():
    import types
    ret = []
    for module in [common, desktop, distribution]:
        assert isinstance(module, types.ModuleType) or module == None
        if module and hasattr(module, 'menu') and hasattr(module.menu, 'get_others_menu'):
            ret.extend(module.menu.get_others_menu())
    return ret

def load_tips():
    import types
    ret = []
    for module in [common, desktop, distribution]:
        if module:
            assert isinstance(module, types.ModuleType)
            if hasattr(module, 'tips') and hasattr(module.tips, 'get'):
                ret.extend(module.tips.get())
    return ret

def load_cure_objs():
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

import common
try:
    desktop = __import__(DESKTOP)
except (ImportError, ValueError):
    print_traceback()
    desktop = None
try:
    distribution = __import__(DISTRIBUTION)
except (ImportError, ValueError):
    print_traceback()
    distribution = None

def load_app_objs():
    with TimeStat('load_app_objs'):
        AppObjs.set_basic_modules(common, desktop, distribution)
    
        with TimeStat('load_from_text_file'):
            AppObjs.load_from_text_file()
        
        with TimeStat('load_from_basic_modules'):
            AppObjs.load_from_basic_modules()
        
        with TimeStat('load_from_extensions'):
            AppObjs.load_from_extensions()
    
        with TimeStat('strip'):
            AppObjs.strip_invisible()
            AppObjs.strip_wrong_locale()
    
        with TimeStat('reload_icon'):
            AppObjs.all_objs_reload_icon()
        
        with TimeStat('reset_status'):
            AppObjs.all_objs_reset_status()
