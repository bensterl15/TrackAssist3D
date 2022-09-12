import tkinter as tk
from tkinter import ttk, Text

from Views.Frames.MainTextFrame import MainTextFrame


class TestFrame(ttk.Frame):

    def __init__(self, win):
        super().__init__(win)
        # setup the grid layout manager
        self.win = win;
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        options = {'padx': 5, 'pady': 5}

        # convert button
        Test_button = ttk.Button(
            self,
            text='Test',
            command=self.process
        )
        Test_button.grid(column=1, row=0, sticky='W', **options)

        stop_button = ttk.Button(
            self,
            text='Stop',
            command=self.stop
        )
        stop_button.grid(column=1, row=0, **options)

        self.textFrame = MainTextFrame(self)
        self.textFrame.grid(column=1, row=1, sticky='W', **options)

    def process(self):
        self.textFrame.insert('Runing test.py ...')

        from SegmentationSkeloton.segmentation_processing._3DUnet import test

        self.textFrame.insert('Done')

    def stop(self):
        exit()