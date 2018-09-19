#! /usr/bin/env python3

"""
Copyright (c) 2018 Lenz Grimmer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import sys


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Select Reviewers")

        grid = Gtk.Grid()
        names = ['']
        self.add(grid)

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        button_copy = Gtk.Button(label="Copy")
        button_copy.connect("clicked", self.copy_button_clicked)

        button_quit = Gtk.Button(label="Quit")
        button_quit.connect("clicked", Gtk.main_quit)

        namelist = Gtk.ListStore(str)
        for name in readnames():
            namelist.append([name])

        listview = Gtk.TreeView(model=namelist)
        column_1 = Gtk.TreeViewColumn('Name', Gtk.CellRendererText(), text=0)
        listview.append_column(column_1)
        select = listview.get_selection()
        select.set_mode(Gtk.SelectionMode.MULTIPLE)
        select.connect("changed", self.listview_selection_changed)

        grid.attach(listview, 0, 0, 2, 1)
        grid.attach(button_copy, 0, 1, 1, 1)
        grid.attach(button_quit, 1, 1, 1, 1)

    def copy_button_clicked(self, widget):
        clipboard = ''
        for name in self.names:
            clipboard = f'{clipboard}Reviewed-by: {name[0]}\n'
        self.clipboard.set_text(clipboard, -1)

    def listview_selection_changed(self, selection):
        model, treepaths = selection.get_selected_rows()
        self.names = ([list(model[path]) for path in treepaths])


def readnames():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'reviewers.txt'
    file = open(filename, 'r')
    names = [name.rstrip('\n') for name in file]
    return names

if __name__ == '__main__':
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
