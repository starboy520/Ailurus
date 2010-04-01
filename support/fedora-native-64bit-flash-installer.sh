#!/bin/bash
# Script  created by
# Romeo-Adrian Cioaba romeo.cioaba@spotonearth.com
# License: GPL

echo "Stopping any Firefox that might be running"
killall -9 firefox

echo "Removing any other flash plugin previously installed:"
yum remove -y flash-plugin gnash gnash-plugin swfdec swfdec-mozilla nspluginwrapper
rm -f /usr/lib/mozilla/plugins/*flash*
rm -f ~/.mozilla/plugins/*flash*
rm -f /usr/lib/firefox/plugins/*flash*
rm -f /usr/lib/firefox-addons/plugins/*flash*
rm -rfd /usr/lib/nspluginwrapper


echo "Installing Flash Player 10"
cd /tmp
wget http://download.macromedia.com/pub/labs/flashplayer10/libflashplayer-10.0.42.34.linux-x86_64.so.tar.gz
tar zxvf libflashplayer-10.0.42.34.linux-x86_64.so.tar.gz
cp libflashplayer.so /usr/lib/mozilla/plugins/ 

echo "Linking the libraries so Firefox and apps depending on XULRunner (vuze, liferea, rsswol) can find it."
ln -sf /usr/lib/mozilla/plugins/libflashplayer.so /usr/lib/firefox-addons/plugins/
ln -sf /usr/lib/mozilla/plugins/libflashplayer.so  /usr/lib/xulrunner-addons/plugins/

# now doing some cleaning up:
rm -rf libflashplayer.so 
rm -rf libflashplayer-10.0.32.18.linux-x86_64.so.tar.gz