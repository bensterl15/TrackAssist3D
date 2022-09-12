import tkinter as tk
from tkinter import ttk, Text, Label
import os
import subprocess
from tkinter.filedialog import askdirectory

import numpy as np
import tifffile
import os
import scipy
import imageio
import zarr
import nibabel as nib
import scipy.signal

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
        processExpand_button.grid(column=0, row=1, **options)

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


    def execute_process(self):

        rawDataPath = self.selectFolderframe.getRawDataPath()
        gtDataPath = self.selectFolderframe.getGtDataPath()
        thresholdsNpyPath = self.selectFolderframe.getThreholdsNpyPath()

        print("rawDataPath:  "+rawDataPath)
        print("gtDataPath:  "+gtDataPath)
        print("thresholdsNpyPath:  "+thresholdsNpyPath)

        names = []
        lst_order = [0, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5]

        zarr_container = zarr.open('./output/3Dtraining.zarr', 'w')

        '''
        ***************************************test for only 1*********************************************************
        '''
        for i in range(1):
        # for i in range(21):
            names.append('T' + str(i + 1))
        '''
        ***************************************test for only 1*********************************************************
        '''

        thresholds = np.load(thresholdsNpyPath)
        thresholds = thresholds[::40]
        # We only recorded half for training, so repeat because ugh..
        thresholds = thresholds.repeat(2)

        raw = np.zeros((21, 14, 256, 256))
        gt = np.zeros((21, 14, 256, 256))
        num_name = 0
        for name in names:

            self.textFrame.insert("Processing "+str(name)+"... ")
            # self.textFrame.see()
            # self.textFrame.update_idletasks()


            raw_ = 0
            gt_ = np.zeros((14, 512, 512))
            try:
                raw_ = tifffile.imread(os.path.join(rawDataPath, name, name + '.tiff'))
            except:
                raw_ = tifffile.imread(os.path.join(rawDataPath, name, name + '.tif'))

            lst_gt = os.listdir(os.path.join(gtDataPath, name))
            lst_gt.sort()
            for i in range(14):
                gt_[i] = imageio.imread(os.path.join(gtDataPath, name, lst_gt[lst_order[i]]))

            # raw_ = scipy.signal.resample(raw_, 40, axis = 0)
            raw_ = raw_ / np.max(raw_)

            mean_x = 0
            mean_y = 0
            for z_ind in range(14):
                for x_ind in range(512):
                    for y_ind in range(512):
                        mean_x += x_ind * raw_[z_ind, x_ind, y_ind]
                        mean_y += y_ind * raw_[z_ind, x_ind, y_ind]

            mean_x = int(mean_x)
            mean_y = int(mean_y)

            # gt_ = scipy.signal.resample(gt_, 40, axis = 0)
            gt_[gt_ <= 0.5] = 0
            gt_[gt_ > 0.5] = 1

            # Override for now.. UGH
            mean_x = 130
            mean_y = 315
            width = 128

            print(num_name)

            raw[num_name] = raw_[:, (mean_x - width):(mean_x + width), (mean_y - width):(mean_y + width)]
            gt[num_name] = gt_[:, (mean_x - width):(mean_x + width), (mean_y - width):(mean_y + width)]

            # img = nib.Nifti1Image(raw[num_name], affine=np.eye(4))
            # nib.save(img, f'ugh{name}.nii')

            raw[raw < thresholds[num_name]] = 0

            '''
            plt.subplot(311)
            plt.imshow(raw[num_name,7])
            plt.colorbar()

            #raw[gt == 0] = 0

            plt.subplot(312)
            plt.imshow(raw[num_name,7])
            plt.colorbar()

            plt.subplot(313)
            plt.imshow(gt[num_name,7])
            plt.show()
            '''

            num_name = num_name + 1


            self.textFrame.insert(str(name)+" is done. ")

        self.save_to_container(raw, zarr_container, 'raw')
        self.save_to_container(gt, zarr_container, 'gt')


    def execute_process_expand(self):
        rawDataPath = self.selectFolderframe.getRawDataPath()

        names = []

        zarr_container = zarr.open('./output/3Dexpanded.zarr', 'w')

        '''
        ***************************************test for only 1*********************************************************
        '''
        for i in range(1):
            # for i in range(21):
            names.append('T' + str(i + 1))
        '''
        ***************************************test for only 1*********************************************************
        '''

        raw = np.zeros((21, 60, 256, 256))
        num_name = 0
        for name in names:

            self.textFrame.insert("Processing " + str(name) + "... ")

            raw_ = 0
            try:
                raw_ = tifffile.imread(os.path.join(rawDataPath, name, name + '.tiff'))
            except:
                raw_ = tifffile.imread(os.path.join(rawDataPath, name, name + '.tif'))

            raw_ = scipy.signal.resample(raw_, 40, axis=0)
            raw_ = raw_ / np.max(raw_)

            mean_x = 0
            mean_y = 0
            for z_ind in range(14):
                for x_ind in range(512):
                    for y_ind in range(512):
                        mean_x += x_ind * raw_[z_ind, x_ind, y_ind]
                        mean_y += y_ind * raw_[z_ind, x_ind, y_ind]

            mean_x = int(mean_x)
            mean_y = int(mean_y)

            # Override for now.. UGH
            mean_x = 130
            mean_y = 315
            width = 128

            print(num_name)

            raw[num_name, 10:50] = raw_[:, (mean_x - width):(mean_x + width), (mean_y - width):(mean_y + width)]

            img = nib.Nifti1Image(raw[num_name, 10:50], affine=np.eye(4))
            nib.save(img, f'ugh{name}.nii')

            # raw[raw < 0.2] = 0

            num_name = num_name + 1

        self.save_to_container(raw, zarr_container, 'raw')

