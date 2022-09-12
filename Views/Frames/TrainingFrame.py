import tkinter as tk
from tkinter import ttk, Text
from Views.Frames.MainTextFrame import MainTextFrame


class TrainingFrame(ttk.Frame):

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
        training_button = ttk.Button(
            self,
            text='Train',
            command=self.process
        )
        training_button.grid(column=1, row=0, sticky='W', **options)

        stop_button = ttk.Button(
            self,
            text='Stop',
            command=self.stop
        )
        stop_button.grid(column=1, row=0, **options)

        # self.text = Text(self, height=8, width= 50)
        # self.text.grid(column=1, row=1, sticky='W', **options)

        self.textFrame = MainTextFrame(self)
        self.textFrame.grid(column=1, row=1, sticky='W', **options)

    def process(self):
        self.textFrame.insert('Runing train.py ...')

        from SegmentationSkeloton.segmentation_processing._3DUnet import train

        self.textFrame.insert( 'Done')

    def stop(self):
        exit()