import pickle
import tkinter as tk
from tkinter import ttk, Text, filedialog, messagebox

from Views.Frames.MainTextFrame import MainTextFrame


class TestFrame(ttk.Frame):

    def __init__(self, win):
        super().__init__(win)
        # setup the grid layout manager
        self.win = win;
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)

        self.model_checkpoint_path = ''
        self.use_default_model = tk.BooleanVar()

        self.__create_widgets()

    def __create_widgets(self):
        options = {'padx': 5, 'pady': 5}

        self.path_params = tk.StringVar()
        self.params_button = ttk.Entry(self, textvariable=self.path_params, width=35)
        self.params_button.grid(column=1, row=0, sticky='W', **options)
        self.params_button.focus()

        # convert button
        params_open_button = ttk.Button(
            self,
            text='Select model checkpoint',
            command=self.load_params
        )
        params_open_button.grid(column=1, row=0, sticky='E', **options)

        # Add a checkbox:
        ch_default = tk.Checkbutton(self,
                                    text='Use default model',
                                    variable=self.use_default_model,
                                    onvalue=True,
                                    offvalue=False)
        ch_default.grid(column=1, row=1)

        # convert button
        Test_button = ttk.Button(
            self,
            text='Test',
            command=self.process
        )
        Test_button.grid(column=1, row=2, sticky='W', **options)

        stop_button = ttk.Button(
            self,
            text='Stop',
            command=self.stop
        )
        stop_button.grid(column=1, row=2, **options)

        self.textFrame = MainTextFrame(self)
        self.textFrame.grid(column=1, row=3, sticky='W', **options)

    def process(self):
        self.textFrame.insert('Runing test.py ...')

        from SegmentationSkeloton.segmentation_processing._3DUnet import test

        test.test(self.model_checkpoint_path, self.use_default_model.get())

        self.textFrame.insert('Done')

    def load_params(self):
        self.model_checkpoint_path = filedialog.askopenfilename(title='Select model checkpoint')
                                                      # filetypes=(("Pickle Files","*.pickle"),))
        self.set_model_checkpoint_path(self.model_checkpoint_path)
        # try:
        #     #print(self.path_params)
        #     with open(self.path_params, 'rb') as f:
        #         self.pdict = pickle.load(f)
        # except:
        #     messagebox.showerror('Error', 'Couldnt load the model')

    def set_model_checkpoint_path(self, path):
        self.params_button.delete(0, 0)
        self.params_button.insert(0, path)

    def stop(self):
        exit()