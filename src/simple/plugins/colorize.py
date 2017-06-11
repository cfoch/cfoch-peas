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

import sys
sys.path.append('../')

import subprocess
from gi.repository import GObject
from gi.repository import Peas

from extensions import TextExtension


class bColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Colorize(GObject.GObject, TextExtension):
    __gtype_name__ = 'ColorizePlugin'

    def __init__(self):
        GObject.Object.__init__(self)
        print("INIT COLORIZE")

    def do_process(self, text):
        print("%s%s%s" % (bColors.WARNING, text, bColors.ENDC))
