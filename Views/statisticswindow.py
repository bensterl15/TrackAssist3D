import os
from tkinter import Button, Label, StringVar, Frame, Listbox, Scrollbar, messagebox
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk, Image

# Import the constants we need:
from Model.constants_and_paths import LOADING_WINDOW_BACKGROUND_PATH, \
    PLUS_BUTTON_PATH, MINUS_BUTTON_PATH, NEXT_BUTTON_PATH, TRACKING_PATH_OFFSET, REMOVAL_PATH_OFFSET

from Model.mesh import Mesh

import csv
import numpy as np

class StatisticsWindow:

    def __init__(self, win, view_manager):
        self.win = win
        self.view_manager = view_manager

        background_load = Image.open(LOADING_WINDOW_BACKGROUND_PATH)
        background_width = 800
        background_height = 300
        background_load = background_load.resize(
            (background_width, background_height), Image.ANTIALIAS)
        background_img = ImageTk.PhotoImage(background_load)

        self.background = Label(win, image=background_img)
        self.background.image = background_img
        self.background.place(
            x=(1200 - background_width)/2, y=50
        )

        generate_report_button = Button(win,
                                        text='Generate Report',
                                        command=self.generate_report)
        generate_report_button.place(x=600, y=500)

        back_button = Button(win, text='Back To Steps Screen', command=self.back_requested)
        back_button.place(x=100, y=100)

    def generate_report(self):
        f = asksaveasfile(mode='w', defaultextension='.csv')
        # If None, the user hit cancel:
        if f is not None:
            writer = csv.writer(f, lineterminator='\n')

            # Keep an internal list of the protrusion indices to report
            protrusion_indices = self._gather_unique_cell_indices()

            writer.writerow(['Filopodia Index:'] + protrusion_indices)

            for stat in self._gather_stats_keys():
                writer.writerow([stat + ':'])
                for cell_index in range(len(self.view_manager.base_dirs)):
                    stat_row = self._load_line_of_stats(stat, cell_index, protrusion_indices)
                    writer.writerow(['t = ' + str(cell_index)] + stat_row)
            f.close()

    def back_requested(self):
        self.view_manager.back_to_step()

    def _gather_unique_cell_indices(self):
        indices = []
        for index, cell_path in enumerate(self.view_manager.base_dirs):
            # Folder location:
            if index > 0:
                stats_path = os.path.join(cell_path, TRACKING_PATH_OFFSET)
            else:
                stats_path = os.path.join(cell_path, REMOVAL_PATH_OFFSET)
            # Add the file name:
            stats_path = os.path.join(stats_path, 'blebStats_1_1.mat')
            # The None is because we are using this as static method:
            stats_dict = Mesh.load_statistics(None, stats_path)
            for index in stats_dict['index']:
                indices.append(index)
        return list(np.unique(indices))

    def _gather_stats_keys(self):
        stats_path = os.path.join(self.view_manager.base_dirs[1], TRACKING_PATH_OFFSET)
        stats_path = os.path.join(stats_path, 'blebStats_1_1.mat')
        stats_dict = Mesh.load_statistics(None, stats_path)
        stats_list = list(stats_dict.keys())
        # Only interested in statistics that do not have "__" in the title:
        return [item for item in stats_list if '__' not in item and item != 'index']

    def _load_line_of_stats(self, stat_key, cell_num, protrusion_indices):
        current_cell_path= self.view_manager.base_dirs[cell_num]
        # Folder location:
        if cell_num > 0:
            stats_path = os.path.join(current_cell_path, TRACKING_PATH_OFFSET)
        else:
            stats_path = os.path.join(current_cell_path, REMOVAL_PATH_OFFSET)
        # Add the file name:
        stats_path = os.path.join(stats_path, 'blebStats_1_1.mat')
        # The None is because we are using this as static method:
        stats_dict = Mesh.load_statistics(None, stats_path)
        row = []
        # Iterate through the protrusions in the same order we plotted them:
        for p_index in protrusion_indices:
            # Try to read the statistic.. If it is not in the list, this means that protrusion p_index
            # IS NOT IN THE CURRENT CELL! (We expect this to happen quite often)
            try:
                dic_index = (list(stats_dict['index'])).index(p_index)
            except:
                dic_index = 'NA'
            if dic_index is not 'NA':
                row.append(stats_dict[stat_key][dic_index][0])
            else:
                row.append('NA')
        return row
