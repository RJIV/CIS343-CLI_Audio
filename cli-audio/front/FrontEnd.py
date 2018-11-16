import curses
import curses.textpad
import sys
import os
from cliExceptions.CLI_Audio_Exception import CLI_Audio_File_Exception
from cliExceptions.CLI_Audio_Exception import CLI_Audio_Screen_Size_Exception

class FrontEnd:

    def __init__(self, player, library):
        self.player = player
        self.library = library
        self.directory = "./media/playlist1/"
        self.playlist = []
        self.player.play('./media/playlist1/HeartsOnFire.wav')
        curses.wrapper(self.menu)

    def menu(self, args):
        self.stdscr = curses.initscr()
        self.stdscr.border()
        height,width = self.stdscr.getmaxyx()
        if (height < 25):
            raise CLI_Audio_Screen_Size_Exception("Please increase screen height","")
        if (width < 90):
            raise CLI_Audio_Screen_Size_Exception("Please increase screen width","")
        self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
        self.stdscr.addstr(5,10, "c - Change current song")
        self.stdscr.addstr(6,10, "p - Play/Pause")
        self.stdscr.addstr(7,10, "l - Library")
        self.stdscr.addstr(9,10, "ESC - Quit")
        self.stdscr.addstr(14,10, "Available Songs: ")
        self.updateSong()
        self.stdscr.refresh()
        self.setPlaylist()
        self.displayPlaylist()
        while True:
            self.stdscr.addstr(13,10, "Current Directory: " + self.directory)
            c = self.stdscr.getch()
            if c == 27:
                self.quit()
            elif c == ord('p'):
                self.player.pause()
            elif c == ord('c'):
                self.changeSong()
                self.updateSong()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            elif c == ord('l'):
                self.library.showLibrary(self)
    
    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    def changeSong(self):
        changeWindow = curses.newwin(5, 40, 5, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.player.stop()
        self.player.play(path.decode(encoding="utf-8"))
        
        try:
            if (int(path) > len(self.playlist)):
                self.stdscr.addstr(2,15, "Song not Found!")
                raise CLI_Audio_File_Exception("The song requested is not available "
                    "in the playlist","CLI_AudioFileException!")

        except CLI_Audio_File_Exception:
            # print("Song not available")
            return
        except:
            return
        
        self.stdscr.addstr(2,15, "                            ")
        index = self.playlist[int(path)-1]
        songs = os.listdir(self.directory)
        song = self.directory + index
        self.player.play(song)

    def displayPlaylist(self):

        x = 1
        for song in self.playlist:
            self.stdscr.addstr(15 + x,10, str(x) + ": "+ song)
            x = x + 1

    def setDirectory(self,dir):
        self.directory = dir

    def setPlaylist(self):
        self.playlist = []
        songs = os.listdir(self.directory)
        i = 0
        for song in songs:
            self.playlist.append(song)
            i = i + 1

    def quit(self):
        self.player.stop()
        exit()
