import tkinter as tk
from tkinter import ttk


class StepFrame(ttk.Frame):
    def __init__(self, win, view_manager, current_view):
        super().__init__(win)
        self.win = win
        self.view_manager = view_manager
        self.current_view = current_view

        # setup the grid layout manager
        self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=3)

        self.__create_widgets()

    def __create_widgets(self):
        # Find what
        ttk.Label(self, text='Load data', font=('Helvatical bold',15)).grid(column=0, row=0, columnspan=2)
        ttk.Label(self, text='|').grid(column=0, row=1, columnspan=2)
        ttk.Label(self, text='Process', font=('Helvatical',15)).grid(column=0, row=2, columnspan=2)
        ttk.Label(self, text='|').grid(column=0, row=3, columnspan=2)
        ttk.Label(self, text='Process_expand', font=('Helvatical',15)).grid(column=0, row=4, columnspan=2)
        ttk.Label(self, text='|').grid(column=0, row=5, columnspan=2)
        ttk.Label(self, text='Train', font=('Helvatical',15)).grid(column=0, row=6, columnspan=2)
        ttk.Label(self, text='|').grid(column=0, row=7, columnspan=2)
        ttk.Label(self, text='Test', font=('Helvatical',15)).grid(column=0, row=8, columnspan=2)
        ttk.Label(self, text='|').grid(column=0, row=9, columnspan=2)
        ttk.Label(self, text='Preprocess', font=('Helvatical',15)).grid(column=0, row=10, columnspan=2)

        ttk.Label(self, text='   ', font=('Helvatical',15)).grid(column=0, row=11, columnspan=2)

        prev_button = ttk.Button(self, text='Previous', command=self.previous).grid(column=0, row=12)
        next_button = ttk.Button(self, text='Next', command=self.next).grid(column=1, row=12)

    def next(self):

        print("Go to next step")
        self.view_manager.change_view(self.current_view)

    def previous(self):

        print("Go to previous step")