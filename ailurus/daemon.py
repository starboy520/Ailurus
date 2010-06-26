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
import dbus
import dbus.service
import dbus.glib
import gobject
import os
import subprocess
import ctypes
try:
    import apt, apt_pkg
except ImportError: # This is not Debian or Ubuntu
    pass

version = 5 # must be integer

class AccessDeniedError(dbus.DBusException):
    _dbus_error_name = 'cn.ailurus.AccessDeniedError'

class CommandFailError(dbus.DBusException):
    _dbus_error_name = 'cn.ailurus.CommandFailError'

class CannotLockAptCacheError(dbus.DBusException):
    _dbus_error_name = 'cn.ailurus.CannotLockAptCacheError'

class AptPackageNotExistError(dbus.DBusException):
    _dbus_error_name = 'cn.ailurus.AptPackageNotExistError'

class AilurusFulgens(dbus.service.Object):
    @dbus.service.method('cn.ailurus.Interface', 
                                          in_signature='sss', 
                                          out_signature='', 
                                          sender_keyword='sender')
    def run(self, command, env_string, secret_key, sender=None):
        if not secret_key in self.authorized_secret_key:
            self.check_permission(sender)
            self.authorized_secret_key.add(secret_key)
        command = command.encode('utf8')
        env_string = env_string.encode('utf8')
        env = self.__get_dict(env_string)
        os.chdir(env['PWD'])
        task = subprocess.Popen(command, shell=True, env=env)
        task.wait()
        if task.returncode:
            raise CommandFailError(command, task.returncode)

    @dbus.service.method('cn.ailurus.Interface', 
                                          in_signature='sss', 
                                          out_signature='i', 
                                          sender_keyword='sender')
    def spawn(self, command, env_string, secret_key, sender=None):
        if not secret_key in self.authorized_secret_key:
            self.check_permission(sender)
            self.authorized_secret_key.add(secret_key)
        command = command.encode('utf8')
        env_string = env_string.encode('utf8')
        env = self.__get_dict(env_string)
        os.chdir(env['PWD'])
        task = subprocess.Popen(command, shell=True, env=env)
        return task.pid

    @dbus.service.method('cn.ailurus.Interface', 
                                          in_signature='', 
                                          out_signature='i') 
    def get_check_permission_method(self):
        return self.check_permission_method

    @dbus.service.method('cn.ailurus.Interface', 
                                          in_signature='', 
                                          out_signature='i') 
    def get_version(self):
        return version

    @dbus.service.method('cn.ailurus.Interface', 
                                          in_signature='', 
                                          out_signature='',
                                          sender_keyword='sender')
    def exit(self, sender=None):
        self.check_permission(sender)
        self.mainloop.quit()

    def check_permission(self, sender):
        if self.check_permission_method == 0:
            self.__check_permission_0(sender)
        elif self.check_permission_method == 1:
            self.__check_permission_1(sender)

    def __init__(self, mainloop):
        self.mainloop = mainloop # use to terminate mainloop
        self.authorized_secret_key = set()
        bus_name = dbus.service.BusName('cn.ailurus', bus = dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, '/')
        
        self.check_permission_method = -1
        try:
            obj = dbus.SystemBus().get_object('org.freedesktop.PolicyKit1', '/org/freedesktop/PolicyKit1/Authority')
            obj = dbus.Interface(obj, 'org.freedesktop.PolicyKit1.Authority')
            self.check_permission_method = 1
        except dbus.DBusException:
            obj = dbus.SystemBus().get_object('org.freedesktop.PolicyKit', '/')
            obj = dbus.Interface(obj, 'org.freedesktop.PolicyKit')
            self.check_permission_method = 0
        if self.check_permission_method == -1: raise Exception

    def __check_permission_0(self, sender):
        if not sender: raise ValueError('sender == None')
        
        obj = dbus.SystemBus().get_object('org.freedesktop.PolicyKit', '/')
        obj = dbus.Interface(obj, 'org.freedesktop.PolicyKit')
        granted = obj.IsSystemBusNameAuthorized('cn.ailurus', sender, False)
        if 'yes' != granted:
            raise AccessDeniedError('Session is not authorized. Authorization method = 0')

    def __check_permission_1(self, sender):
        # This function is from project "gnome-lirc-properties". Thanks !
        if not sender: raise ValueError('sender == None')
        
        obj = dbus.SystemBus().get_object('org.freedesktop.PolicyKit1', '/org/freedesktop/PolicyKit1/Authority')
        obj = dbus.Interface(obj, 'org.freedesktop.PolicyKit1.Authority')
        (granted, _, details) = obj.CheckAuthorization(
                ('system-bus-name', {'name': sender}), 'cn.ailurus', {}, dbus.UInt32(1), '', timeout=600)
        if not granted:
            raise AccessDeniedError('Session is not authorized. Authorization method = 1')

    def __get_dict(self, string):
        assert string.endswith('\n')
        List = string.split('\n')
        Dict = {}
        for i in range(0, len(List)-1, 2):
            k = List[i]
            v = List[i+1]
            Dict[k] = v
        return Dict
    
    @dbus.service.method('cn.ailurus.Interface', 
                                    in_signature='s',
                                    out_signature='') 
    def drop_priviledge(self, secret_key):
        if secret_key in self.authorized_secret_key:
            self.authorized_secret_key.remove(secret_key)

    @dbus.service.method('cn.ailurus.Interface', in_signature='', out_signature='')
    def init_apt_cache(self):
        self._cache = None # an instance of apt.cache.Cache
        apt_pkg.init()
    
    def __lock_apt_cache(self): # will raise CannotLockAptCacheError
        # try the lock in /var/cache/apt/archive/lock first
        # this is because apt-get install will hold it all the time
        # while the dpkg lock is briefly given up before dpkg is
        # forked off. this can cause a race (LP: #437709)
        lockfile = apt_pkg.Config.FindDir("Dir::Cache::Archives") + "lock"
        lock = apt_pkg.GetLock(lockfile)
        if lock < 0: raise CannotLockAptCacheError
        os.close(lock)
        apt_pkg.PkgSystemLock()
    
    def __unlock_apt_cache(self):
        apt_pkg.PkgSystemUnLock()
    
    def __open_apt_cache(self):
        if self._cache: self._cache.open()
        else: self._cache = apt.cache.Cache()
        
    def __close_apt_cache(self):
        self._cache = None

    def begin_apt_transaction(self):
        self.__lock_apt_cache()
        self.__open_apt_cache()

    def end_apt_transaction(self):
        self.__close_apt_cache()
        self.__unlock_apt_cache()

    def install_apt_packages(self, package_names):
        '''package_names -- package names concatenated by comma (,)
        may raise apt.cache.FetchFailedException, apt.cache.FetchCancelledException, SystemError'''
        with self._cache.actiongroup():
            for pkg_name in package_names.split(','):
                if self._cache.has_key(pkg_name):
                    pkg = self._cache[pkg_name]
                else:
                    raise AptPackageNotExistError(pkg_name)
                pkg.mark_install()
        self._cache.commit()

    def remove_apt_packages(self, package_names):
        '''package_names -- package names concatenated by comma (,)'''
        with self._cache.actiongroup():
            for pkg_name in package_names.split(','):
                if self._cache.has_key(pkg_name):
                    pkg = self._cache[pkg_name]
                else:
                    raise AptPackageNotExistError(pkg_name)
                pkg.mark_delete()
        self._cache.commit()

def main(): # revoked by ailurus-daemon
    try:
        libc = ctypes.CDLL('libc.so.6')
        libc.prctl(15, 'policykit-ailurus', 0, 0, 0) # change_task_name
    except: pass
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    mainloop = gobject.MainLoop()
    AilurusFulgens(mainloop)
    mainloop.run()

if __name__ == '__main__':
    main()