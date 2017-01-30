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

import subprocess

from gi.repository import GObject
from gi.repository import Peas


class Speaker(GObject.GObject, Peas.Activatable):
    __gtype_name__ = 'RepeaterPlugin'

    object = GObject.Property(type=GObject.Object)

    def do_activate(self):
        API = self.object
        API.app.connect("process-input", self.processInputCb)
        API.app.connect("start", self.startCb)
        API.app.connect("finish", self.finishCb)

    def do_deactivate(self):
        API = self.object
        API.app.disconnect_by_func(self.processInputCb)
        API.app.disconnect_by_func(self.startCb)
        API.app.disconnect_by_func(self.finishCb)

    def processInputCb(self, app, text):
        can_speak = self.speak(text)
        if not can_speak:
            print("There is an error in my throat.")

    def startCb(self, app):
        self.speak("welcome")

    def finishCb(self, app):
        self.speak("bye")

    def speak(self, text):
        st = subprocess.getstatusoutput("espeak '%s'" % text)
        if (st[0] != 0):
            st = subprocess.getstatusoutput("spd-say '%s'" % text)
        return st[0] == 0
