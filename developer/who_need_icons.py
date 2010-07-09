#!/usr/bin/env python

import os, sys
path = os.path.dirname(os.path.abspath(__file__)) + '/../ailurus'
sys.path.insert(0, path)
from loader import AppObjs
import common.apps
import fedora.apps
import gnome.apps
import ubuntu.apps

names = []
for module in [common.apps, fedora.apps, gnome.apps, ubuntu.apps]:
    names += AppObjs.all_installer_names_in_module(module)
names += AppObjs.all_installer_names_in_text_file()

for name in names:
    path, use_default_icon = AppObjs.get_icon_path(name)
    if use_default_icon:
        print name