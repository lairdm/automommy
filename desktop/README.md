# Magnet link integration

Following this howto on hooking magnet links in the browser to pushing torrents to Transmission:

https://blog.flo.cx/2012/08/opening-magnet-links-with-xdg-open-on-a-remote-transmission-daemon/

Create a directory, ~/magnet/ and copy MagnetLinkTransfer.sh to the directory (make sure it's executable)

Copy Automommy.desktop to /usr/share/applications/

Add the entries from mimeapps.list to ~/.local/share/applications/mimeapps.list

And run:

xdg-mime default Automommy.desktop x-scheme-handler/magnet

You can query the linkage with:

xdg-mime query default x-scheme-handler/magnet
