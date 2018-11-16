import curses
import curses.textpad
import os
import sys

class Library:

        def _init_(self):
            self.files = os.listdir('./media')

        def showLibrary(self):
            x = 0
            print(x)
