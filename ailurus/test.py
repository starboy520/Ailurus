#!/usr/bin/env python

import gtk, pango

image_size = 20
font_size = 4

button = gtk.Button()
text = gtk.Label('Information')
text.modify_font(pango.FontDescription('Sans %s' % font_size))
text.set_ellipsize(pango.ELLIPSIZE_END)
pixbuf = gtk.gdk.pixbuf_new_from_file_at_size('../data/sora_icons/m_hardware.png', image_size, image_size)
image = gtk.Image()
image.set_from_pixbuf(pixbuf)
align = gtk.Alignment(0.5, 0.5)
align.add(image)
align.set_size_request(int(1.5*image_size), -1)
vbox = gtk.VBox(False, 0)
vbox.pack_start(align, False)
vbox.pack_start(text, False)
button.add(vbox)
align2 = gtk.Alignment(0,0)
align2.add(button)
window = gtk.Window()
window.add(align2)
window.show_all()
window.connect('destroy', gtk.main_quit)
gtk.main()