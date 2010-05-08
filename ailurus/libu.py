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

def get_pixbuf(file, width, height):
    from lib import D
    import gtk
    try:
        return gtk.gdk.pixbuf_new_from_file_at_size(file, width, height)
    except:
        import traceback
        traceback.print_exc()
        return gtk.gdk.pixbuf_new_from_file_at_size(D + 'other_icons/blank.png', width, height)
    
def gray_bg(widget):
    import gtk
    if not isinstance(widget, gtk.Entry) and not isinstance(widget, gtk.TextView): raise TypeError
    
    def event(widget, e):
        if widget.base_color_changed==False:
            color = widget.style.bg[gtk.STATE_NORMAL]
            widget.modify_base(gtk.STATE_NORMAL, color)
            widget.base_color_changed = True
    widget.base_color_changed = False
    widget.connect('expose-event', event)
    widget.connect('map-event', event)

def image_stock_button(stock, text):
    import gtk
    box = gtk.HBox(False, 3)
    box.pack_start(gtk.image_new_from_stock(stock, gtk.ICON_SIZE_BUTTON), False, False)
    l = gtk.Label()
    l.set_text_with_mnemonic(text)
    box.pack_start(l, False, False)
    button = gtk.Button()
    button.add(box)
    return button

def image_file_button(label, image_file_name, size):
    import gtk
    pixbuf = get_pixbuf(image_file_name, size, size)
    image = gtk.Image()
    image.set_from_pixbuf(pixbuf)
    box = gtk.HBox(False, 3)
    box.pack_start(image, False, False)
    l = gtk.Label()
    l.set_text_with_mnemonic(label)
    box.pack_start(l, False, False)
    button = gtk.Button()
    button.add(box)
    return button

def stock_image_only_button(stock):
    import gtk
    image = gtk.image_new_from_stock(stock, gtk.ICON_SIZE_BUTTON)
    button = gtk.Button()
    button.add(image)
    return button

def image_stock_menuitem(image_stock, label):
    import gtk
    item = gtk.ImageMenuItem(stock_id=image_stock)
    item.get_child().set_text(label)
    return item

def image_file_menuitem(label, image_file_name, size):
    import gtk
    pixbuf = get_pixbuf(image_file_name, size, size)
    image = gtk.Image()
    image.set_from_pixbuf(pixbuf)
    item = gtk.ImageMenuItem(stock_id=gtk.STOCK_ABOUT)
    item.set_image(image)
    item.get_child().set_text(label)
    return item
    
def title_menuitem(string):
    import gtk
    l = gtk.Label()
    l.set_markup('<span size="large"><b>%s</b></span>'%string)
    box = gtk.HBox(False, 3)
    box.pack_start(l, False, False)
    item = gtk.MenuItem()
    item.add(box)
#    item.select()
    def dummy(*w):
        return True
    item.connect('enter-notify-event', dummy)
    item.connect('leave-notify-event', dummy)
    item.connect('button-press-event', dummy)
    item.connect('button-release-event', dummy)
    return item

def left_align(widget):
    import gtk
    align = gtk.Alignment(0, 0.5)
    align.add(widget)
    return align

def right_align(widget):
    import gtk
    align = gtk.Alignment(1, 0.5)
    align.add(widget)
    return align
    
def label_left_align(string):
    import gtk
    label = gtk.Label(string)
    return left_align(label)

def image_left_align(path):
    import gtk
    image = gtk.Image()
    image.set_from_file(path)
    return image

def add_expander(vbox, title):
    def __title(text):
        label = gtk.Label()
        label.set_markup('<b>%s</b>'%text)
        return label

    import gtk
    expander = gtk.Expander()
    expander.set_border_width(5)
    expander.set_label_widget( __title(title) )
    vbox.set_border_width(5)
    expander.add(vbox)
    expander.set_expanded(False)
    return expander
