#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
import time
import sys


class MineSweeper():
    def __init__(self, easy: bool):
        self.easy = easy
        self.windowlist = []
        self.running = True

        self.startwinfunc()
    
    def startwinfunc(self):
        startwin = tk.Tk()
        self.windowlist += [startwin]
        startwin.title('PyMines — Setup Window')
        startwin.protocol("WM_DELETE_WINDOW", self.stop)
        sizeLabel = tk.Label(startwin, text='Size:')
        sizeLabel.grid(row=0, column=0)
        sv = tk.StringVar()
        size = tk.Entry(startwin, width=5, textvariable=sv)
        size.grid(column=1, row=0)
        def go():
            s = int(size.get())
            self.windowlist.remove(startwin)
            startwin.destroy()
            self.start(s)
        submit = tk.Button(startwin, text='Start', command=go)
        submit.grid(column=2, row=0)

    def start(self, size):
        self.size = size
        self.time1 = time.time()
        self.master = tk.Tk()
        self.windowlist += [self.master]
        self.master.title(f'PyMines — Game Window')
        self.master.resizable(False, False)
        self.master.rowconfigure(tuple(range(size)), minsize=1, weight=1)
        self.master.columnconfigure(tuple(range(size)), minsize=1, weight=1)
        self.master.protocol("WM_DELETE_WINDOW", self.stop)

        
        self.flag = tk.PhotoImage(file="flag.png")
        self.empty = tk.PhotoImage(file="empty.png")
        self.numbers = [tk.PhotoImage(file=f"{i}.png") for i in range(9)]
        self.explode = tk.PhotoImage(file = "boom.png")
        self.bomb = tk.PhotoImage(file="bomb.png")
        self.flagbad = tk.PhotoImage(file="flagbad.png")

        

        self.cells = np.array(
            
            [[Cell(self, row, column) for row in range(size)]
             for column in range(size)])

        self.mines = np.array(
            [[random.choice((0, 0, 0, 0, 0, 1)) for i in range(size)]
             for i in range(size)])

        if self.easy:
            self.mines[0, 0], self.mines[size - 1, 0], self.mines[size - 1, size - 1], self.mines[0, size - 1] = 0, 0, 0, 0

        self.scoreboard = tk.Tk()
        self.scoreboard.title("Scoreboard - PyMines")
        self.windowlist += [self.scoreboard]
        self.scoreboard.protocol("WM_DELETE_WINDOW", self.stop)
        self.score = tk.Label(master=self.scoreboard, text=f'Time is: {int(np.floor(time.time() - self.time1))} seconds')
        self.score.grid(row=size, column=1, columnspan=size - 1)
        self.score.after(500, self.updateTime)
        self.quit_btn = tk.Button(self.scoreboard, text='Quit', command=self.byebye)
        self.quit_btn.grid(row=size, column=0, columnspan=3)

    #def Run(self):
        #self.master.mainloop()

    def handleEvent(self, cell, button, x=0, y=0):
        if button == 'R':
            if cell.flagged:
                cell.widget['image'] = self.empty
            else:
                cell.widget['image'] = self.flag
        if button == 'L':
            if self.handleLeftClick(cell, x, y):
                if self.running:
                    self.gameover(cell, False)

                return 'mine'
        if self.checkWin():
            if self.running:
                self.gameover(cell, True)

    def checkWin(self):
        unstepped = 0
        for y, row in enumerate(self.mines):
            for x, mine in enumerate(row):
                cell = self.cells[y, x]
                if cell.stepped and self.mines[y, x] == 1:
                    return False
                if cell.flagged and self.mines[y, x] == 0:
                    return False
                if not cell.flagged and not cell.stepped:
                    unstepped += 1
                if unstepped > 1:
                    return False
        return True

    def handleLeftClick(self, cell, y, x):
        if cell.flagged:
            return False
        cell.stepped = True
        count = np.sum(self.mines[max(y - 1, 0): y + 2,
                                  max(x - 1, 0): x + 2])
        
        for y1 in range(max(y - 1, 0), min(y + 2, self.size)):
            for x1 in range(max(x - 1, 0), min(x + 2, self.size)):
                if self.cells[y1, x1].stepped is False and count == 0:
                    print(x1, y1)
                    self.cells[y1, x1].LeftClick()
        old = """
        if count == 0:
            if y > 0:
                self.handleLeftClick(self.cells[y-1, x], y-1, x)
                if x > 0:
                    self.handleLeftClick(self.cells[y-1, x-1], y-1, x-1)
                if x < self.size - 1:
                    self.handleLeftClick(self.cells[y-1, x+1], y-1, x+1)

            self.handleLeftClick(self.cells[y, x], y, x)
            if x > 0:
                self.handleLeftClick(self.cells[y, x-1], y, x-1)
            if x < self.size - 1:
                self.handleLeftClick(self.cells[y, x+1], y, x+1)

            if y < self.size:
                self.handleLeftClick(self.cells[y+1, x], y+1, x)
                if x > 0:
                    self.handleLeftClick(self.cells[y+1, x-1], y+1, x-1)
                if x < self.size - 1:
                    self.handleLeftClick(self.cells[y+1, x+1], y+1, x+1)
        """
        if self.mines[y, x]:
            for row in self.cells:
                for i in row:
                    if i.stepped is False:
                        count = 1

            return True

        self.cells[y, x].widget['image'] = self.numbers[count]

        if count:
            return False


    def updateTime(self, *args):
        self.score['text'] = f'Time is: {int(np.floor(max(0, time.time() - self.time1)))} seconds'
        if self.running:
            self.score.after(500, self.updateTime)

    def stop(self):
        for window in self.windowlist:
            try:
                window.destroy()
            except Exception as e:
                print(e)
                continue
            #window.destroy()
            try:
                sys.exit()
            except SystemExit:
                pass

    def byebye(self, *args):
        confirmation = tk.Tk()
        self.windowlist += [confirmation]
        confirmation.protocol("WM_DELETE_WINDOW", self.stop)
        confirmation.title('Quit')
        confirmation.rowconfigure((0, 1), minsize=57, weight=1)
        confirmation.columnconfigure((0, 1), minsize=60)
        text = tk.Label(master=confirmation, text='Are you sure you want to quit? All progress will be lost.')
        text.grid(row=0, column=0, columnspan=2)
        def close():
            confirmation.destroy()
            self.windowlist.remove(confirmation)
        yes = tk.Button(master=confirmation, text='Yes', command=self.stop)
        no = tk.Button(master=confirmation, text='No', command=close)
        yes.grid(row=1, column=0)
        no.grid(row=1, column=1)

    def gameover(self, finalcell, won):
        if not won:
            finalcell.widget['image'] = self.explode
        else:
            print("you win")
        
                #print(cell)
        self.running = False
        print("gameover")
        #reveal
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if self.mines[y, x] == 1:
                    if not cell.flagged and not cell.flagged and not cell.stepped:
                        cell.widget['image'] = self.bomb
                if self.mines[y, x] == 0 and cell.flagged:
                    cell.widget['image'] = self.flagbad
                cell.stepped = True

        restart = tk.Tk()
        self.windowlist += [restart]
        restart.protocol("WM_DELETE_WINDOW", self.stop)
        restart.title('Restart')
        restart.rowconfigure((0, 1), minsize=57, weight=1)
        restart.columnconfigure((0, 1), minsize=60)
        text = tk.Label(master=restart, text='Do you want to restart?')
        text.grid(row=0, column=0, columnspan=2)
        def yes():
            self.stop()
            self.running = True
            self.startwinfunc()
        agree = tk.Button(master=restart, text='Yes', command=yes)
        deny  = tk.Button(master=restart, text='No',  command=self.stop)
        agree.grid(row=1, column=0)
        deny.grid(row=1, column=1)

class Cell():
    def __init__(self, mineSweeper, row: int, column: int, *args, **kw):
        self.mineSweeper = mineSweeper
        self.stepped = False
        self.row = row
        self.column = column
        self.isMine = None
        self.flagged = False
        self.widget = tk.Label(mineSweeper.master, image=self.mineSweeper.empty, relief=tk.RAISED, *args, **kw)
        self.widget.grid(row=self.row, column=self.column)
        self.widget.bind('<Button-1>', self.LeftClick)
        self.widget.bind('<Button-3>', self.RightClick)

    def LeftClick(self, *args):
        if self.stepped:
            return
        self.widget.configure(relief=tk.SUNKEN)
        event = self.mineSweeper.handleEvent(self, 'L', self.column, self.row)  # Already sets stepped to True
        if event != 'mine':
            self.widget['text'] = event
        #else:
        #    self.widget['text'] = 'mine'
        #    #self.mineSweeper.gameover(self)

    def RightClick(self, *args):
        if self.stepped is False:
            self.mineSweeper.handleEvent(self, 'R')
            self.flagged = not self.flagged

    def updateText(self, newText: str):
        self.widget['text'] = newText


def Main():
    return MineSweeper(True)#.Run()


#if __name__ == '__main__':
#    Main()
ms = Main()
