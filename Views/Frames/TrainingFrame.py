import tkinter as tk
from tkinter import ttk, Text, filedialog, messagebox
from Views.Frames.MainTextFrame import MainTextFrame
from SegmentationSkeloton.segmentation_processing._3DUnet import train

import pickle
import os
import subprocess
#from tensorboard import program
#from tensorboard import main as tb

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

        self.path_params = tk.StringVar()
        self.params_button = ttk.Entry(self, textvariable=self.path_params, width=20)
        self.params_button.grid(column=1, row=0, **options)
        self.params_button.focus()

        # convert button
        params_open_button = ttk.Button(
            self,
            text='Select raw data folder',
            command=self.load_params
        )
        params_open_button.grid(column=2, row=0, sticky='W', **options)

        # Add a checkbox:
        ch_default = tk.Checkbutton(self, text='Use default model params')
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

        '''
            Plan B: run the code directly, but can't show the information in the text box
        '''


        '''
        tb = program.TensorBoard()
        tb.configure(argv=[None, '--logdir', ' C:\\Users\\bsterling\\PycharmProjects\\FiloTracker\\output\\logs\\'])
        url = tb.launch()
        '''

        subprocess.Popen('tensorboard --logdir=\'C:\\Users\\bsterling\\PycharmProjects\\FiloTracker\\output\\logs\' --port=8009')

        #self.textFrame.insert(f'Tensorflow listening on {url}')

        train.train(self.pdict)

        self.textFrame.insert( 'Done')

    def load_params(self):
        self.path_params = filedialog.askopenfilename(title='Select saved model parameters',
                                                      filetypes=(("Pickle Files","*.pickle"),))
        try:
            #print(self.path_params)
            with open(self.path_params, 'rb') as f:
                self.pdict = pickle.load(f)
        except:
            messagebox.showerror('Error', 'Couldnt load the model')

    def stop(self):
        exit()