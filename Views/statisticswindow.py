import json
import os
from pathlib import Path
from tkinter import Button, Label, StringVar, Frame, Listbox, Scrollbar, messagebox
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk, Image

# Import the constants we need:
from Model.constants_and_paths import LOADING_WINDOW_BACKGROUND_PATH, \
    PLUS_BUTTON_PATH, MINUS_BUTTON_PATH, NEXT_BUTTON_PATH, TRACKING_PATH_OFFSET, REMOVAL_PATH_OFFSET

from Model.mesh import Mesh
from Model.chain import Chain

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
            x=(1200 - background_width) / 2, y=50
        )

        generate_report_button = Button(win,
                                        text='Generate Report',
                                        command=self.generate_report)
        generate_report_button.place(x=600, y=500)

        back_button = Button(win, text='Back To Steps Screen', command=self.back_requested)
        back_button.place(x=100, y=100)

        self._init_chains()

        for chain in self.chains:
            chain.print_contents()

    def generate_report(self):
        f = asksaveasfile(mode='w', defaultextension='.csv')
        # If None, the user hit cancel:
        if f is not None:
            writer = csv.writer(f, lineterminator='\n')

            # Keep an internal list of the protrusion indices to report
            ids = []
            for i in range(len(self.chains)):
                ids.append(self.chains[i].unique_id)

            writer.writerow(['Filopodia Index:'] + ids)

            for stat in self._gather_stats_keys():
                writer.writerow([stat + ':'])
                for cell_index in range(len(self.view_manager.base_dirs)):
                    stat_row = self._load_line_of_stats(stat, cell_index)
                    writer.writerow(['t = ' + str(cell_index)] + stat_row)
            f.close()

    def back_requested(self):
        self.view_manager.back_to_step()

    def _gather_stats_keys(self):
        stats_path = os.path.join(self.view_manager.base_dirs[0], REMOVAL_PATH_OFFSET)
        stats_path = os.path.join(stats_path, 'blebStats_1_1.mat')
        stats_dict = Mesh.load_statistics(None, stats_path)
        stats_list = list(stats_dict.keys())
        # Only interested in statistics that do not have "__" in the title:
        return [item for item in stats_list if '__' not in item and item != 'index']

    def _load_line_of_stats(self, stat_key, cell_num):
        current_cell_path = self.view_manager.base_dirs[cell_num]
        # Folder location:
        stats_path = os.path.join(current_cell_path, REMOVAL_PATH_OFFSET)
        # Add the file name:
        stats_path = os.path.join(stats_path, 'blebStats_1_1.mat')
        # The None is because we are using this as static method:
        stats_dict = Mesh.load_statistics(None, stats_path)
        row = []

        for i in range(len(self.chains)):
            if cell_num < self.chains[i].starting_time or cell_num > self.chains[i].last_time:
                row.append('NA')
            else:
                p_index = self.chains[i].data[cell_num - self.chains[i].starting_time]
                dic_index = (list(stats_dict['index'])).index(p_index)
                row.append(stats_dict[stat_key][dic_index][0])
        '''
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
        '''
        return row

    def _init_chains(self):
        self.chains = []
        for cell_index in range(len(self.view_manager.base_dirs)):
            current_cell_path = self.view_manager.base_dirs[cell_index]

            # We need to load segmentation here:
            path_segmentation = os.path.join(current_cell_path,
                                             os.path.join(
                                                 REMOVAL_PATH_OFFSET,
                                                 'surfaceSegment_1_1.mat'))
            seg = None

            if Path(path_segmentation).is_file():
                seg = np.unique(Mesh.load_segmentation(None, path_segmentation))
                seg = seg.astype(int)
                # Do not want base:
                seg = seg[1:]
            else:
                messagebox.showerror('Error', 'Missing segmentation .mat file!!')
                break

            if cell_index == 0:
                for protrusion_index in seg:
                    self.chains.append(Chain(cell_index, protrusion_index))
            else:
                unused_ids = list(seg.copy())
                path_dictionary = os.path.join(current_cell_path,
                                               os.path.join(
                                                   TRACKING_PATH_OFFSET,
                                                   'protrusion_permutation.txt'))
                if Path(path_dictionary).is_file():
                    with open(path_dictionary) as file:
                        seg_dic = json.load(file)
                        for chain in self.chains:
                            # If last_time is not cell_index - 1, then the protrusion has already expired:
                            # Also, only add if seg_dic has defined key:
                            if chain.last_time == cell_index - 1 and str(chain.last_index) in seg_dic:
                                current_index = seg_dic[str(chain.last_index)]
                                chain.append(protrusion_id=current_index,
                                             current_time=cell_index)
                                unused_ids.remove(current_index)
                    for id_ in unused_ids:
                        self.chains.append(Chain(cell_index, id_))
                else:
                    messagebox.showerror('Error', 'Missing dictionary file!!')
                    break