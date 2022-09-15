import tkinter as tk
from tkinter import ttk
from tkinter import *

from PIL import Image, ImageTk

import os
import re
import tifffile
import numpy as np

import matplotlib.pyplot as plt

class ThresholdsWindow:
    def __init__(self, win, selectFolderFrame):
        self.win = win
        self.selectFolderFrame = selectFolderFrame
        self.highLight = ttk.Style()
        self.highLight.configure("H.TLabel", background="#ccc")

        self.lowLight = ttk.Style()
        self.lowLight.configure("L.TLabel")

        self.completed = ttk.Style()
        self.completed.configure("C.TLabel", background="white")

        self.__create_widgets()

    def __create_widgets(self):
        window_width = 600
        window_height = 600

        # get the screen dimension
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.win.title('SegmentationSkeletonGUI')
        self.win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        rawDataPath = self.selectFolderFrame.getRawDataPath()

        raw_list = os.listdir(rawDataPath)
        sort_tmp = [int(re.sub("[^0-9]", "", s)) for s in raw_list]
        raw_list = [x for _, x in sorted(zip(sort_tmp, raw_list))]

        n_timepoints = len(raw_list)

        # Get shape information:
        dummy = 0
        try:
            dummy = tifffile.imread(os.path.join(rawDataPath, raw_list[0]))
        except:
            dummy = tifffile.imread(os.path.join(rawDataPath, raw_list[0]))
        (nZ, nX, nY) = dummy.shape

        self.raw = np.zeros((n_timepoints, nZ, nX, nY))

        for time_index in range(n_timepoints):
            raw_name = os.path.join(rawDataPath, raw_list[time_index])

            raw_ = 0
            try:
                raw_ = tifffile.imread(raw_name)
            except:
                raw_ = tifffile.imread(raw_name)

            self.raw[time_index] = raw_

        self.raw_display = self.raw.copy()

        self.selected_z = 0
        self.selected_t = 0

        self.saved_thresholds = np.zeros((n_timepoints))

        self.img = ImageTk.PhotoImage(master=self.win, image=Image.fromarray(self.raw_display[self.selected_t, self.selected_z]*256))

        self.canvas = Canvas(self.win, width=400, height=400)
        self.canvas.pack()
        self.image_container = self.canvas.create_image(20, 20, anchor="nw", image=self.img)

        lbl = Label(self.win, text='Select a different threshold for each time point:')
        lbl.place(x=150, y=275)

        t_lbl = Label(self.win, text='t')
        t_lbl.place(x=125, y=300)
        slider_t = Scale(self.win, from_=0, to=n_timepoints-1, orient=tk.HORIZONTAL, resolution = 1,
                       command=self.change_t)
        slider_t.place(x=150, y=300)

        z_lbl = Label(self.win, text='z')
        z_lbl.place(x=125, y=400)
        slider_z = Scale(self.win, from_=0, to=nZ-1, orient=tk.HORIZONTAL, resolution = 1,
                       command=self.change_z)
        slider_z.place(x=150, y=400)

        t_lbl = Label(self.win, text='threshold')
        t_lbl.place(x=75, y=450)
        self.slider_threshold = Scale(self.win, from_=0, to=1, orient=tk.HORIZONTAL, resolution = 0.001,
                         command=self.change_threshold)
        self.slider_threshold.place(x=150, y=450)

        doneButton = Button(self.win, text='Done', command=self.done_pressed)
        doneButton.place(x=400, y=450)

        self.win.mainloop()

    def refresh_image(self):
        current_threshold = self.saved_thresholds[self.selected_t]
        self.slider_threshold.set(current_threshold)
        self.raw_display = self.raw.copy()
        self.raw_display[self.raw_display < current_threshold*np.max(self.raw[self.selected_t, self.selected_z])] = 0
        self.img = ImageTk.PhotoImage(master=self.win, image=
        Image.fromarray(self.raw_display[self.selected_t, self.selected_z] * 256))

        self.canvas.itemconfig(self.image_container, image=self.img)

    def change_z(self, new_z):
        self.selected_z = int(new_z)
        self.refresh_image()

    def change_t(self, new_t):
        self.selected_t = int(new_t)
        self.refresh_image()

    def change_threshold(self, new_threshold):
        self.saved_thresholds[self.selected_t] = float(new_threshold)
        self.refresh_image()

    def done_pressed(self):
        print(os.getcwd())
        np.save('thresholds.npy', self.saved_thresholds)
        self.win.destroy()