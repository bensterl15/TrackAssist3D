import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.filedialog import askdirectory, askopenfile
from tkinter.messagebox import showinfo
import os

from Views.thresholdsWindow import ThresholdsWindow
import Model.constants_and_paths as mcp

class SelectFolderFrame(ttk.Frame):

    def __init__(self, win):
        super().__init__(win)
        # setup the grid layout manager
        self.win = win;
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)

        self.rawDataPath = ""
        self.gtDataPath = ""
        self.thresholdsNpyPath = ""

        self.__create_widgets()

    def __create_widgets(self):
        options = {'padx': 5, 'pady': 5}

        path = tk.StringVar()
        self.rawData_path_entry = ttk.Entry(self, textvariable=path, width=30)
        self.rawData_path_entry.grid(column=1, row=0, **options)
        self.rawData_path_entry.focus()

        # convert button
        open_button = ttk.Button(
            self,
            text='Select raw data folder',
            command=self.select_raw_data_path
        )
        open_button.grid(column=2, row=0, sticky='W', **options)

        path2 = tk.StringVar()
        self.gtData_path_entry = ttk.Entry(self, textvariable=path2, width=30)
        self.gtData_path_entry.grid(column=1, row=1, **options)
        self.gtData_path_entry.focus()

        # convert button
        open_button = ttk.Button(
            self,
            text='Select gt data folder',
            command=self.select_gt_data_path
        )
        open_button.grid(column=2, row=1, sticky='W', **options)

        path3 = tk.StringVar()
        self.thresholds_npy_path_entry = ttk.Entry(self, textvariable=path3, width=30)
        self.thresholds_npy_path_entry.grid(column=1, row=2, **options)
        self.thresholds_npy_path_entry.focus()

        # convert button
        open_button = ttk.Button(
            self,
            text='Select thresholds.npy',
            command=self.select_thresholds_npy_path
        )
        open_button.grid(column=2, row=2, sticky='W', **options)

        # Button to generate the thresholds.py:
        open_button = ttk.Button(
            self,
            text='Generate thresholds.npy',
            command=self.generate_thresholds_npy_path
        )
        open_button.grid(column=3, row=2, sticky='W', **options)



    def select_raw_data_path(self):
        path = askdirectory(title='Select raw data folder')

        self.rawDataPath = path
        self.set_raw_data_path(path)

        dataFolderPath = os.path.dirname(path)  # [:-3]
        self.recordDataDirPath(dataFolderPath)

        return

    def select_gt_data_path(self):
        path = askdirectory(title='Select gt data Folder')
        self.gtDataPath = path
        self.set_gt_data_path(path)

        return

    def select_thresholds_npy_path(self):
        file = askopenfile(title='Select thresholds.npy', mode='r', filetypes=[('npy Files', '*.npy')])
        if file is not None:
            path = os.path.abspath(file.name)
            self.thresholdsNpyPath = path
            self.set_thresholds_npy_path(path)

    def set_raw_data_path(self, path):
        self.rawData_path_entry.delete(0, 0)
        self.rawData_path_entry.insert(0, path)

    def set_gt_data_path(self, path):
        self.gtData_path_entry.delete(0, 0)
        self.gtData_path_entry.insert(0, path)

    def set_thresholds_npy_path(self, path):
        self.thresholds_npy_path_entry.delete(0, 0)
        self.thresholds_npy_path_entry.insert(0, path)

    def getRawDataPath(self):
        return self.rawDataPath

    def getGtDataPath(self):
        return self.gtDataPath

    def getThreholdsNpyPath(self):
        return self.thresholdsNpyPath

    # Creates a dialog to create a thresholds.npy file:
    def generate_thresholds_npy_path(self):
        window = tk.Tk()
        ThresholdsWindow(window, self)
        #window.mainloop()

    def recordDataDirPath(self, DataDirPath):
        mcp.ROOT_STR = DataDirPath
