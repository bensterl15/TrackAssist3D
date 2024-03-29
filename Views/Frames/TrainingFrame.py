import tkinter as tk
from tkinter import ttk, Text, filedialog, messagebox
from Views.Frames.MainTextFrame import MainTextFrame
from SegmentationSkeloton.segmentation_processing._3DUnet import train

import pickle
import os
import subprocess
#from tensorboard import program
#from tensorboard import main as tb
import Model.constants_and_paths as mcp

class TrainingFrame(ttk.Frame):

    def __init__(self, win):
        super().__init__(win)
        # setup the grid layout manager
        self.win = win;
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)

        self.is_default_param = False

        self.__create_widgets()

    def __create_widgets(self):
        options = {'padx': 5, 'pady': 5}

        self.path_params = tk.StringVar()
        self.params_button = ttk.Entry(self, textvariable=self.path_params, width=35)
        self.params_button.grid(column=1, row=0, sticky='W',**options)
        self.params_button.focus()

        # convert button
        self.params_open_button = ttk.Button(
            self,
            text='Select model params',
            command=self.load_params
        )
        self.params_open_button.grid(column=1, row=0, sticky='E', **options)

        # Add a checkbox:
        ch_default = tk.Checkbutton(self,
                                    text='Use default model params',
                                    onvalue=True,
                                    offvalue=False,
                                    command=self.toggle_default_param)
        ch_default.grid(column=1, row=1)

        # convert button
        training_button = ttk.Button(
            self,
            text='Train',
            command=self.process
        )
        training_button.grid(column=1, row=2, sticky='W', **options)

        stop_button = ttk.Button(
            self,
            text='Stop',
            command=self.stop
        )
        stop_button.grid(column=1, row=2, **options)

        # self.text = Text(self, height=8, width= 50)
        # self.text.grid(column=1, row=1, sticky='W', **options)

        self.textFrame = MainTextFrame(self)
        self.textFrame.grid(column=1, row=3, sticky='W', **options)

    def process(self):
        self.textFrame.insert('Runing train.py ...')

        # Open a tensorboard instance on port 8090:
        subprocess.Popen(f'tensorboard --logdir={mcp.ROOT_STR}\\logs --port=8009')

        url = 'http://localhost:8009/'
        self.textFrame.insert(f'Tensorflow listening on {url}')

        if hasattr(self, 'pdict'):
            pdict = self.pdict
        else:
            pdict = None

        train.train(pdict, self.is_default_param)

        self.textFrame.insert('Done')

    def load_params(self):
        self.path_params = filedialog.askopenfilename(title='Select saved model parameters',
                                                      filetypes=(("Pickle Files", "*.pickle"),))
        try:
            #print(self.path_params)
            with open(self.path_params, 'rb') as f:
                self.pdict = pickle.load(f)
            self.set_params_path(self.path_params)
        except:
            messagebox.showerror('Error', 'Couldnt load the model')

    def set_params_path(self, path):
        self.params_button.delete(0, 0)
        self.params_button.insert(0, path)

    def stop(self):
        exit()

    def toggle_default_param(self):
        self.is_default_param = not self.is_default_param
        if self.is_default_param:
            self.params_open_button['state'] = 'disabled'
            self.params_button['state'] = 'disabled'
        else:
            self.params_open_button['state'] = 'normal'
            self.params_button['state'] = 'normal'