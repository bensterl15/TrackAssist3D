import tkinter as tk
from tkinter import ttk

class ExitFrame(ttk.Frame):

    def __init__(self, win):
        self.win = win

        exit_button = ttk.Button(
            self.win,
            text='Exit',
            command=self.quit
        )

        exit_button.pack(
            ipadx=5,
            ipady=5,
            expand=True
        )

    def quit(self):
        exit()