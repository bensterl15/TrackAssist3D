import tkinter as tk
from tkinter import ttk, Text, Label
import os
import subprocess
from tkinter.filedialog import askdirectory
import Model.constants_and_paths as mcp

import numpy as np
import tifffile
import os
import scipy
import imageio
import zarr
import nibabel as nib
import scipy.signal

import re

from Views.Frames.MainTextFrame import MainTextFrame
from Views.Frames.SelectFolderFrame import SelectFolderFrame


class ProcessFrame(ttk.Frame):
    my_text = "Proces.py running..."

    def __init__(self, win):
        super().__init__(win)
        # setup the grid layout manager
        self.win = win;

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        options = {'padx': 5, 'pady': 5}

        self.selectFolderframe = SelectFolderFrame(self)
        self.selectFolderframe.grid(column=0, row=0, sticky='W', **options)

        # convert button
        process_button = ttk.Button(
            self,
            text='Process',
            command=self._process
        )
        process_button.grid(column=0, row=1, sticky='W', **options)

        processExpand_button = ttk.Button(
            self,
            text='Process_Expand',
            command=self._process_expand
        )
        processExpand_button.grid(column=0, row=1,**options)

        self.textFrame = MainTextFrame(self)

        self.textFrame.grid(column=0, row=2, sticky='W', **options)

    def _process(self):

        self.textFrame.insert('Runing process.py ...')

        '''
        todo: how to show the print in the text frame by directly calling process
        '''
        # from SegmentationSkeloton import process

        self.execute_process()

        self.textFrame.insert('Task is Completed!')

    def _process_expand(self):
        self.textFrame.insert("runing process_expand.py")

        '''
        todo: how to show the print in the text frame by directly calling process_expand
        '''
        # from SegmentationSkeloton import process_expand

        self.execute_process_expand()

        self.textFrame.insert("Process_expand.py is done.")

    def save_to_container(self, arr, container, name):
        for i in range(arr.shape[0]):
            dataset = container.create_dataset(name + '/' + str(i), shape=arr[i].shape)
            dataset[:] = arr[i]

    '''
        Plan A: COPY CODE to here, and we can add the processing information in the text box
    '''
    def execute_process(self):

        rawDataPath = self.selectFolderframe.getRawDataPath()
        gtDataPath = self.selectFolderframe.getGtDataPath()
        thresholdsNpyPath = self.selectFolderframe.getThreholdsNpyPath()

        dataFolderPath = os.path.dirname(rawDataPath)#[:-3]

        print("rawDataPath:  "+rawDataPath)
        print("gtDataPath:  "+gtDataPath)
        print("thresholdsNpyPath:  "+thresholdsNpyPath)
        print("dataFolderPath:  "+dataFolderPath)

        zarr_container = zarr.open(dataFolderPath+'/output/3Dtraining.zarr', 'w')

        '''
        ***************************************test for only 1*********************************************************
        '''

        raw_list = os.listdir(rawDataPath)
        sort_tmp = [int(re.sub("[^0-9]", "", s)) for s in raw_list]
        raw_list = [x for _, x in sorted(zip(sort_tmp, raw_list))]

        gt_list = os.listdir(gtDataPath)
        sort_tmp = [int(re.sub("[^0-9]", "", s)) for s in gt_list]
        gt_list = [x for _, x in sorted(zip(sort_tmp, gt_list))]

        if len(raw_list) != len(gt_list):
            tk.messagebox.showerror('Error', 'Raw and ground truth contain different number of timepoints')
            return

        n_timepoints = len(raw_list)

        '''
        ***************************************test for only 1*********************************************************
        '''

        thresholds = np.load(thresholdsNpyPath)
        #thresholds = thresholds[::40]
        # We only recorded half for training, so repeat because ugh..
        #thresholds = thresholds.repeat(2)

        # Get shape information:
        dummy = 0
        try:
            dummy = tifffile.imread(os.path.join(rawDataPath, raw_list[0]))
        except:
            dummy = tifffile.imread(os.path.join(rawDataPath, raw_list[0]))
        (nZ, nX, nY) = dummy.shape

        raw = np.zeros((n_timepoints, nZ, nX, nY))
        gt = np.zeros((n_timepoints, nZ, nX, nY))

        for time_index in range(n_timepoints):
            raw_name = os.path.join(rawDataPath, raw_list[time_index])
            gt_name = os.path.join(gtDataPath, gt_list[time_index])

            '''
                Add the information in the text box
            '''
            self.textFrame.insert(f"Processing {raw_name} and {gt_name}... ")
            # self.textFrame.see()
            # self.textFrame.update_idletasks()

            raw_ = 0
            try:
                raw_ = tifffile.imread(raw_name)
            except:
                raw_ = tifffile.imread(raw_name)

            gt_ = 0
            try:
                gt_ = tifffile.imread(gt_name)
            except:
                gt_ = tifffile.imread(gt_name)

            # img = nib.Nifti1Image(raw[num_name], affine=np.eye(4))
            # nib.save(img, f'ugh{name}.nii')

            raw_[raw_ < thresholds[time_index]] = 0

            raw[time_index] = raw_
            gt[time_index] = gt_

            self.textFrame.insert(f"{time_index} step is done. ")

        self.save_to_container(raw, zarr_container, 'raw')
        self.save_to_container(gt, zarr_container, 'gt')


    def execute_process_expand(self):
        rawDataPath = self.selectFolderframe.getRawDataPath()
        dataFolderPath = rawDataPath[:-3]

        names = []

        zarr_container = zarr.open(dataFolderPath+'/output/3Dexpanded.zarr', 'w')

        '''
        ***************************************test for only 1*********************************************************
        '''

        '''
        ***************************************test for only 1*********************************************************
        '''

        raw_list = os.listdir(rawDataPath)
        sort_tmp = [int(re.sub("[^0-9]", "", s)) for s in raw_list]
        raw_list = [x for _, x in sorted(zip(sort_tmp, raw_list))]

        n_timesteps = len(raw_list)

        thresholdsNpyPath = self.selectFolderframe.getThreholdsNpyPath()
        thresholds = np.load(thresholdsNpyPath)
        #thresholds = thresholds[::40]
        # We only recorded half for training, so repeat because ugh..
        #thresholds = thresholds.repeat(2)

        # Get shape information:
        dummy = 0
        try:
            dummy = tifffile.imread(os.path.join(rawDataPath, raw_list[0]))
        except:
            dummy = tifffile.imread(os.path.join(rawDataPath, raw_list[0]))
        (nZ, nX, nY) = dummy.shape

        z_interp = 60

        raw = np.zeros((n_timesteps, z_interp, nX, nY))
        num_name = 0
        for time_index in range(n_timesteps):

            raw_name = os.path.join(rawDataPath, raw_list[time_index])
            self.textFrame.insert(f"Processing {raw_name}... ")

            raw_ = 0
            try:
                raw_ = tifffile.imread(raw_name)
            except:
                raw_ = tifffile.imread(raw_name)

            raw_ = scipy.signal.resample(raw_, z_interp - 20, axis=0)
            raw_ = raw_ / np.max(raw_)

            raw_[raw_ < thresholds[time_index]] = 0

            # We pad with ten layers of zeros on each side:
            raw[num_name, 10:(z_interp - 10)] = raw_

            #img = nib.Nifti1Image(raw[num_name, 10:(z_interp - 10)], affine=np.eye(4))
            #nib.save(img, f'ugh{name}.nii')

            # raw[raw < 0.2] = 0

            num_name = num_name + 1

        self.save_to_container(raw, zarr_container, 'raw')