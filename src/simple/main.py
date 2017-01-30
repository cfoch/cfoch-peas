# -*- coding: utf-8 -*-
# cfoch-peas
# Copyright (c) 2017, Fabian Orccon <cfoch.fabian@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA 02110-1301, USA.

import gi
gi.require_version('Peas', '1.0')

from gi.repository import Peas
from gi.repository import GObject


class API(GObject.GObject):
    def __init__(self, app):
        GObject.Object.__init__(self)
        self.app = app


class PluginManager:
    def __init__(self, app):
        self.app = app
        self.engine = Peas.Engine.get_default()
        self.engine.enable_loader("python3")
        self.engine.add_search_path("plugins")

        plugin_iface = API(self.app)
        value = GObject.Value()
        value.init(API)
        value.set_object(plugin_iface)

        self.extension_set = Peas.ExtensionSet.new_with_properties(self.engine, Peas.Activatable, ["object"], [plugin_iface])

        # Load plugins.
        for plugin in self.engine.get_plugin_list():
            self.engine.load_plugin(plugin)

        self.extension_set.connect("extension-removed", self.extensionRemovedCb)
        # extension_set.foreach(self.foreach)

    def foreach(self, extension_set, plugin_info, extension):
        extension.activate()

    def extensionRemovedCb(self, extension_set, plugin_info, extension):
        extension.deactivate()


class Application(GObject.Object):
    __gsignals__ = {
        "start": (GObject.SIGNAL_RUN_LAST, None, ()),
        "process-input": (GObject.SIGNAL_RUN_LAST, None, (str, )),
        "finish": (GObject.SIGNAL_RUN_LAST, None, ())
    }

    def __init__(self):
        GObject.Object.__init__(self)
        self.manager = PluginManager(self)

    def run(self):
        self.emit("start")
        print("INPUT q TO QUIT")
        self.show_plugin_help()
        self._loop()

    def do_process_input(self, text):
        plugins = self.manager.engine.get_plugin_list()
        # TODO
        # Maybe handle it with GSettings?
        try:
            # TODO
            # Handle it with regex, maybe?
            if text.startswith("activate"):
                i = int(text.split("activate")[1])
                self.manager.extension_set.get_extension(plugins[i]).activate()
            elif text.startswith("deactivate"):
                i = int(text.split("deactivate")[1])
                self.manager.extension_set.get_extension(plugins[i]).deactivate()
        except:
            pass

    def show_plugin_help(self):
        print("To activate a plugin, input 'activate <number>'")
        print("To activate a plugin, input 'deactivate <number>'")
        for i, plugin in enumerate(self.manager.engine.get_plugin_list()):
            print(i, " : ", plugin.get_name())

    def _loop(self):
        while True:
            print(">: ", end='')
            keyboard_input = input()
            if keyboard_input == "q":
                self.emit("finish")
                break;
            else:
                self.emit("process-input", keyboard_input)


if __name__ == "__main__":
    my_app = Application()
    my_app.run()
