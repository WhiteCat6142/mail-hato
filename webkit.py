#!/usr/bin/env python
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('WebKit', '6.0')
from gi.repository import Gtk
from gi.repository import WebKit
from gi.repository import GLib

#https://stackoverflow.com/questions/42174933/python-web-browser-disable-javascript
# Python Web Browser: Disable Javascript? - Stack Overflow
# https://wiki.gnome.org/Projects/Vala/WebKitSample
# Projects/Vala/WebKitSample - GNOME Wiki!
# https://github.com/ren-chon/PyGTK4-Tutorial
# ren-chon/PyGTK4-Tutorial: GTK4 + Python tutorial with code examples

class Browser(Gtk.Application):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self,app):
        self.much_window = Gtk.Window(application=app)
        self.much_window.connect('destroy', lambda w: Gtk.main_quit())
        self.much_window.set_default_size(1000, 700)

        self.so_navigation = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

#https://docs.gtk.org/gtk4/class.Button.html
        self.many_back = Gtk.Button.new_from_icon_name("go-previous")
        self.such_forward = Gtk.Button.new_from_icon_name("go-next")
        self.very_refresh = Gtk.Button.new_from_icon_name("view-refresh")
        self.wow_address_bar = Gtk.Entry.new()

        self.many_back.connect('clicked', self.go_back)
        self.such_forward.connect('clicked', self.go_forward)
        self.very_refresh.connect('clicked', self.refresh_page)
        self.wow_address_bar.connect('activate', self.load_page)

        self.so_navigation.append(self.many_back)
        self.so_navigation.append(self.such_forward)
        self.so_navigation.append(self.very_refresh)
        self.so_navigation.append(self.wow_address_bar)

# https://lazka.github.io/pgi-docs/WebKit2-4.0/mapping.html
        self.settings = WebKit.Settings.new()
        WebKit.Settings.set_enable_javascript (self.settings, False)
        WebKit.Settings.set_enable_media (self.settings, False)
        WebKit.Settings.set_enable_mock_capture_devices(self.settings, False)
        WebKit.Settings.set_enable_dns_prefetching (self.settings, False)
        WebKit.Settings.set_enable_webaudio (self.settings, False)
        WebKit.Settings.set_enable_hyperlink_auditing (self.settings, False)


        self.very_view = Gtk.Frame()
        self.such_webview = WebKit.WebView()
        self.such_webview.set_settings(self.settings)
        
        # https://gabmus.org/posts/block_ads_in_webkitgtk/
        # Block ads in WebKitGtk – GabMus's Dev Log
        # https://github.com/streaksu/mantissa/blob/master/source/engine/customview.d
        # mantissa/source/engine/customview.d
        # https://webkitgtk.org/reference/webkit2gtk/stable/method.UserContentFilterStore.save.html
        my_filter_store = WebKit.UserContentFilterStore.new('./path2')
        
        content_manager = self.such_webview.get_user_content_manager()

        def save_blocklist_cb(caller, res, *args):
         try:
            filter = my_filter_store.save_finish(res)
            content_manager.add_filter(filter)
         except GLib.Error:
            print('Error saving blocklist')

        #    save_blocklist_cb '[{"trigger": {"url-filter": "http://"},"action": {"type": "block"}}]'
        # https://webkit.org/blog/3476/content-blockers-first-look/
        # Introduction to WebKit Content Blockers | WebKit
        my_filter_store.save('blocklist', GLib.Bytes.new_take('[{"trigger": {"url-filter": ".*","load-type":["third-party"]},"action": {"type": "block"}}]'.encode()), None,save_blocklist_cb)

        self.such_webview.load_uri('https://bbs.shingetsu.info/')
        self.such_webview.connect('load-changed', self.change_url)
        self.very_view.set_child(self.such_webview)
        self.very_view.set_vexpand(True)

        self.wow_container = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.wow_container.append(self.so_navigation)
        self.wow_container.append(self.very_view)

        self.much_window.set_child(self.wow_container)
        self.much_window.show()

    def load_page(self, widget):
        so_add = self.wow_address_bar.get_text()
        if so_add.startswith('http://') or so_add.startswith('https://') or so_add.startswith('file://'):
            self.such_webview.load_uri(so_add)
        else:
            so_add = 'http://' + so_add
            self.wow_address_bar.set_text(so_add)
            self.such_webview.load_uri(so_add)

    def change_title(self, widget):
        self.much_window.set_title('Wow ' + str(self.such_webview.get_title()))

    def change_url(self, widget, event):
        if event != 3:
         return
        uri = self.such_webview.get_uri()
        self.wow_address_bar.set_text(uri)
        self.change_title(widget)

    def go_back(self, widget):
        self.such_webview.go_back()

    def go_forward(self, widget):
        self.such_webview.go_forward()

    def refresh_page(self, widget):
        self.such_webview.reload()

app = Browser()
app.run(None)
