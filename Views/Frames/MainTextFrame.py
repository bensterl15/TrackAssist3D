import tkinter as tk
from tkinter import ttk, Text

class MainTextFrame(ttk.Frame):

    def __init__(self, win):
        super().__init__(win)
        # setup the grid layout manager
        self.win = win;
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        options = {'padx': 5, 'pady': 5}

        self.text = Text(self, height=8, width= 50)
        self.text.grid(column=1, row=1, sticky='W', **options)

    def insert(self, message):
        self.text.insert(tk.END,message+"\n")
        self.text.see(tk.END)
        self.text.update_idletasks()

    def see(self):
        self.text.see(tk.END)

    def update_idletasks(self):
        self.text.update_idletasks()