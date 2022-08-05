import os
from tkinter import messagebox, Label, Button, Frame, Scrollbar, Text, IntVar, Checkbutton

from PIL import ImageTk, Image
from scipy.io import savemat
from pathlib import Path

from Model.mesh import Mesh
from Model.singlemeshplotter import SingleMeshPlotter

# Import the constants we need:
from Model.constants_and_paths import MESH_PATH_OFFSET, REMOVER_WINDOW_BACKGROUND_PATH, \
    MOTIF_SEGMENT_PATH_OFFSET, REMOVAL_PATH_OFFSET


def rgb_to_hex(color_vector):
    red = '{:X}'.format(int(color_vector[0] * 255))
    green = '{:X}'.format(int(color_vector[1] * 255))
    blue = '{:X}'.format(int(color_vector[2] * 255))

    if len(red) == 1:
        red = '0' + red
    if len(green) == 1:
        green = '0' + green
    if len(blue) == 1:
        blue = '0' + blue

    return '#' + red + green + blue


class RemoverWindow:
    def __init__(self, win, view_manager, base_directory):
        self.win = win
        self.view_manager = view_manager

        self.base_directory = base_directory

        # Load paths of mesh and motif segmentations:
        path_mesh = os.path.join(base_directory,
                                 os.path.join(
                                     MESH_PATH_OFFSET,
                                     'surface_1_1.mat'))

        path_segmentation = os.path.join(base_directory,
                                         os.path.join(
                                             MOTIF_SEGMENT_PATH_OFFSET,
                                             os.path.join('ch1', 'blebSegment_1_1.mat')))

        path_statistics = os.path.join(base_directory,
                                       os.path.join(
                                           MOTIF_SEGMENT_PATH_OFFSET,
                                           'blebSegmentStats.mat'))

        # Set up the mesh here:
        self.mesh = Mesh(path_mesh, path_segmentation, path_statistics)
        self.plotter = SingleMeshPlotter(self.mesh)

        # Take care of all the GUI stuff:
        background_load = Image.open(REMOVER_WINDOW_BACKGROUND_PATH)
        background_width = 405
        background_height = 120
        background_load = background_load.resize(
            (background_width, background_height), Image.ANTIALIAS)
        background_img = ImageTk.PhotoImage(background_load)

        self.background = Label(win, image=background_img)
        self.background.image = background_img
        self.background.place(x=-2, y=0)

        self.title_label = Label(win, text='Excess Protrusion Removal')
        self.title_label.config(font=("Times", 14, 'italic'))
        self.title_label.place(x=95, y=125)

        self.description_label = Label(win, text='Select the protrusions to keep below:')
        self.description_label.config(font=("Times", 14))
        self.description_label.place(x=35, y=170)

        self.next_button = Button(win, text='Next', command=self.next)
        self.next_button.place(x=335, y=460)

        back_button = Button(win, text='Return to Main Menu', command=self.back_requested)
        back_button.place(x=35, y=460)

        self.lb_frame = Frame(win, width=background_width, height=background_height)
        self.lb_frame.place(x=35, y=200)

        self.vsb = Scrollbar(self.lb_frame, orient="vertical")
        self.text = Text(self.lb_frame, width=40, height=15, yscrollcommand=self.vsb.set)
        self.vsb.config(command=self.text.yview)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        # Create one checkbox for each protrusion:
        self.checked_vars = []
        # -1 because the first segmentation is the base:
        for i in range(self.mesh.segmentation_unique.shape[0] - 1):
            chk_var = IntVar()
            check_box = Checkbutton(self.lb_frame, text=f'{i + 1}', variable=chk_var,
                                    bg=rgb_to_hex(self.mesh.protrusion_colors[i]))

            # Uncomment following line if we want it checked by default:
            # check_box.select()
            check_box.configure(command=lambda ind=i: self.checked(ind))
            self.checked_vars.append(chk_var)
            self.text.window_create("end", window=check_box)
            self.text.insert("end", "\n")  # to force one checkbox per line

    def checked(self, cb_index):
        # print('ID: ' + str(cb_index) + ' Checked: ' + str(self.checked_vars[cb_index].get() == 1))
        self.plotter.update(self.checked_vars[cb_index].get(), cb_index)

    def next(self):
        if messagebox.askyesno(
                title='Confirmation',
                message='Are you sure you would like to proceed? TrackAssist3D will overwrite'
                        ' any contents it ran for this cell.'):

            removal_segment_dir = os.path.join(self.base_directory, REMOVAL_PATH_OFFSET)
            if not Path(removal_segment_dir).is_dir():
                os.mkdir(removal_segment_dir)

            removal_segmentation = os.path.join(removal_segment_dir, 'surfaceSegment_1_1.mat')
            removal_statistics = os.path.join(removal_segment_dir, 'blebStats_1_1.mat')

            # The user wants to save the mesh here:
            self.mesh.removal_finalize()

            # Overwrite the old surface segmentation:
            if Path(removal_segmentation).is_file():
                os.remove(removal_segmentation)

            # Overwrite the old statistics:
            if Path(removal_statistics).is_file():
                os.remove(removal_statistics)

            data_dict = {'surfaceSegment': self.mesh.segmentation}

            savemat(removal_segmentation, data_dict, oned_as='column')
            savemat(removal_statistics, self.mesh.statistics, oned_as='column')

            # Upon saving, would make sense to go back:
            self.back_requested()

    def back_requested(self):
        self.plotter.finalize()
        self.view_manager.back_to_step()
