#!/usr/bin/env python
from distutils.core import setup
from DistUtilsExtra.command import *
from glob import glob

f = open('version')
version = f.read().strip()
f.close()

setup(name = 'ailurus',
      version = version,
      maintainer = 'Homer Xing',
      maintainer_email = 'homer.xing@gmail.com',
      url = 'http://ailurus.googlecode.com/',
      license = 'GNU General Public License (GPL)',
      packages = ['ailurus', 'ailurus.common', 'ailurus.gnome', 'ailurus.fedora', 'ailurus.ubuntu'],
      data_files = [
        ('share/ailurus/data/appicons/', glob('data/appicons/*') ),
        ('share/ailurus/data/files/', glob('data/files/*') ),
        ('share/ailurus/data/nautilus_screenshot/', glob('data/nautilus_screenshot/*') ),
        ('share/ailurus/data/other_icons/', glob('data/other_icons/*') ),
        ('share/ailurus/data/suyun_icons/', glob('data/suyun_icons/*') ),
        ('share/ailurus/data/umut_icons/', glob('data/umut_icons/*') ),
        ('/usr/share/dbus-1/system-services', 'data/dbus/cn.ailurus.service'),
        ('/etc/dbus-1/system.d', 'data/dbus/cn.ailurus.conf'),
        ('/usr/share/PolicyKit/policy/', 'data/policykit0/cn.ailurus.policy'),
        ('/usr/share/polkit-1/actions/', 'data/policykit1/cn.ailurus.policy'),
        
      ],
      scripts = ['bin/ailurus', 'bin/ailurus-daemon'],
      cmdclass = { 'build' :  build_extra.build_extra,
                   'build_i18n' :  build_i18n.build_i18n,
                   'build_help' :  build_help.build_help,
                   'build_icons' :  build_icons.build_icons
                 }
      )