import sys
import os
from pathlib import Path
from tkinter import messagebox, Label, Button, Frame, Scrollbar, \
    Text, IntVar, Checkbutton, StringVar, OptionMenu
import numpy as np
from scipy.io import savemat
from PIL import ImageTk, Image
from Model.mesh import Mesh
from Model.pairmeshplotter import PairMeshPlotter
from Model.constants_and_paths import MESH_PATH_OFFSET, PAIRING_WINDOW_BACKGROUND_PATH, \
    PLUS_BUTTON_PATH, MINUS_BUTTON_PATH, NEXT_BUTTON_PATH, REMOVAL_PATH_OFFSET, TRACKING_PATH_OFFSET

sys.path.append(os.path.abspath(os.path.join('..', 'Model')))

def rgb_to_hex(color_vector):
    red = f'{int(color_vector[0] * 255):02X}'
    green = f'{int(color_vector[1] * 255):02X}'
    blue = f'{int(color_vector[2] * 255):02X}'
    return '#' + red + green + blue

class PairingWindow:
    '''The view for finding protrusion trajectories between two timepoints:'''
    def __init__(self, win, view_manager, base_directory1, base_directory2):
        self.win = win
        self.view_manager = view_manager

        self.base_directory1 = base_directory1
        # Load paths of mesh and motif segmentations:
        path_mesh1 = os.path.join(base_directory1,
                                    os.path.join(
                                        MESH_PATH_OFFSET,
                                        'surface_1_1.mat'
                                    ))

        # We would like to use the previous tracking data,
        # but if it is the very first cell in the sequence, we need to load it from removal
        try:
            path_segmentation1 = os.path.join(base_directory1,
                                              os.path.join(
                                                  TRACKING_PATH_OFFSET,
                                                  'surfaceSegment_1_1.mat'
                                                           ))

            path_statistics1 = os.path.join(base_directory1,
                                             os.path.join(
                                                 TRACKING_PATH_OFFSET,
                                                 'blebStats_1_1.mat'
                                             ))
            # Set up the mesh here:
            self.mesh1 = Mesh(path_mesh1,
                              path_segmentation1,
                              path_statistics1,
                              default_base=False)
        except:
            path_segmentation1 = os.path.join(base_directory1,
                                              os.path.join(
                                                  REMOVAL_PATH_OFFSET,
                                                  'surfaceSegment_1_1.mat'
                                                           ))

            path_statistics1 = os.path.join(base_directory1,
                                             os.path.join(
                                                 REMOVAL_PATH_OFFSET,
                                                 'blebStats_1_1.mat'
                                             ))
            # Set up the first mesh here: Set default_base
            # to false because we want to see all protrusions at first:
            self.mesh1 = Mesh(path_mesh1,
                              path_segmentation1,
                              path_statistics1,
                              default_base=False)

        self.base_directory2 = base_directory2
        # Load paths of mesh and motif segmentations:
        path_mesh2 = os.path.join(base_directory2,
                        os.path.join(MESH_PATH_OFFSET, 'surface_1_1.mat'))

        path_segmentation2 = os.path.join(base_directory2,
                          os.path.join(REMOVAL_PATH_OFFSET, 'surfaceSegment_1_1.mat'))

        path_statistics2 = os.path.join(base_directory2,
                                         os.path.join(
                                             REMOVAL_PATH_OFFSET,
                                             'blebStats_1_1.mat'
                                         ))
        # The second mesh starts with all black protrusions
        # because we need to match them from mesh1:
        self.mesh2 = Mesh(path_mesh2,
                          path_segmentation2,
                          path_statistics2,
                          black_protrusions=True,
                          default_base=False)
        self.plotter = PairMeshPlotter(self.mesh1, self.mesh2)
        self._gui_setup()

    def checked(self, cb_index):
        # print('ID: ' + str(cb_index) + ' Checked: ' + str(self.checked_vars[cb_index].get() == 1))
        self.plotter.update_mesh1(self.checked_vars[cb_index].get(), cb_index)

    def back_fwd_button_pressed(self, button_index, is_backward):
        value = self.optionmenus[button_index].get()

        def cvt_to_int(string_variable):
            if string_variable.isnumeric():
                return int(string_variable) - 1
            return -1

        # We need to iterate until we find an output protrusion that is not already claimed:
        # (Python equivalent of do-while loop)
        while True:
            # Handle backward button pressed on row button_index:
            if is_backward:
                # If we are at element one:
                if value == self.default_op_text:
                    # If non-numeric, we go back to the end:
                    value = str(self.mesh2.segmentation_unique.shape[0] - 1)
                elif value == '1':
                    value = self.default_op_text
                else:
                    value = str(int(value) - 1)

            # Handle forward button pressed on row button_index:
            else:
                # If we are at element one:
                if value == self.default_op_text:
                    # If non-numeric, this is the default text:
                    value = '1'
                elif value == str(self.mesh2.segmentation_unique.shape[0] - 1):
                    # If we hit the maximum, loop back around:
                    value = self.default_op_text
                else:
                    # If we are in the middle, increase protrusion value by 1:
                    value = str(int(value) + 1)

            if cvt_to_int(value) not in self.plotter.protrusion_pairings.values():
                break

        # Update meshes and UI with new value:
        self.optionmenus[button_index].set(value)
        self.dropdown_selections[button_index] = value
        self.plotter.update_mesh2(button_index, value)

    def dropdown_changed(self, *_):
        '''Method called when one of the dropdowns on-screen changed:'''
        dropdown = 0
        value = ''
        detected_change = False
        # Dumb way to find out which dropdown the user selected:
        for i in range(self.mesh1.segmentation_unique.shape[0] - 1):
            if self.dropdown_selections[i] != self.optionmenus[i].get():
                dropdown = i
                value = self.optionmenus[i].get()
                detected_change = True
                self.dropdown_selections[i] = value

        if detected_change:
            print('Dropdown: ' + str(dropdown) + ' changed')
            print('Selected item: ' + value)
            self.plotter.update_mesh2(dropdown, value)

    def back_requested(self):
        self.plotter.finalize()
        self.view_manager.back_to_step()

    def next(self):
        if messagebox.askyesno(title='Confirmation',
                               message=
                               'Are you sure you would like to proceed? Project will be overwritten'
                               ):

            # We only need one directory at this step, because only mesh 2 needs to change:
            tracking_segment_dir = os.path.join(self.base_directory2, TRACKING_PATH_OFFSET)
            if not Path(tracking_segment_dir).is_dir():
                os.mkdir(tracking_segment_dir)

            tracking_segmentation = os.path.join(tracking_segment_dir, 'surfaceSegment_1_1.mat')
            tracking_statistics = os.path.join(tracking_segment_dir, 'blebStats_1_1.mat')

            # Finalize the second mesh here (update the min_index at the same time):
            self.view_manager.min_index = \
                self.mesh2.tracking_finalize(self.mesh1,
                                             self.plotter.protrusion_pairings,
                                             self.view_manager.min_index)

            # Overwrite the old surface segmentation:
            if Path(tracking_segmentation).is_file():
                os.remove(tracking_segmentation)

            # Overwrite the old statistics:
            if Path(tracking_statistics).is_file():
                os.remove(tracking_statistics)

            data_dict = {'surfaceSegment': self.mesh2.segmentation}

            savemat(tracking_segmentation, data_dict, oned_as='column')
            savemat(tracking_statistics, self.mesh2.statistics, oned_as='column')

            # Upon saving, would make sense to go back:
            self.back_requested()

    def _gui_setup(self):
        # Take care of all the GUI stuff:
        background_load = Image.open(PAIRING_WINDOW_BACKGROUND_PATH)
        background_width = 800
        background_height = 300
        background_load = background_load.resize(
            (background_width, background_height), Image.ANTIALIAS
        )
        background_img = ImageTk.PhotoImage(background_load)

        button_width = 50
        next_button_load = Image.open(NEXT_BUTTON_PATH)
        next_button_load = next_button_load.resize((button_width, button_width), Image.ANTIALIAS)
        next_button_img = ImageTk.PhotoImage(next_button_load)

        self.background = Label(self.win, image=background_img)
        self.background.image = background_img
        self.background.place(x=(1200 - background_width) / 2, y=50)

        self.description_label = Label(self.win, text='Select the best protrusion match:')
        self.description_label.config(font=("Courier", 24))
        self.description_label.place(x=(1200 - background_width) / 2, y=375)

        self.next_button = Button(self.win, text='Next', command=self.next, image=next_button_img)
        self.next_button.image = next_button_img
        self.next_button.place(x=1100, y=700)

        back_button = Button(self.win, text='Back To Steps Screen', command=self.back_requested)
        back_button.place(x=100, y=100)

        ### First Checkbox window:
        lb_frame = Frame(self.win, width=background_width, height=background_height)
        lb_frame.place(x=(1200 - background_width) / 2, y=500)

        vsb = Scrollbar(lb_frame, orient="vertical")
        vsb_text = Text(lb_frame, width=40, height=15, yscrollcommand=vsb.set)
        vsb.config(command=vsb_text.yview)
        vsb.pack(side="right", fill="y")
        vsb_text.pack(side="left", fill="both", expand=True)

        # Create one drop-down for each protrusion:
        self.optionmenus = []

        # Set the options for each drop-down (the number of protrusions in mesh2)
        size_ops = int(self.mesh2.segmentation_unique.shape[0] - 1)
        ops = list(np.linspace(1, size_ops, size_ops, dtype=int))
        self.default_op_text = 'D'
        ops.insert(0, self.default_op_text)

        # Create one checkbox for each protrusion:
        self.checked_vars = []

        self.dropdown_selections = {}

        # -1 because the first segmentation is the base:
        for i in range(self.mesh1.segmentation_unique.shape[0] - 1):
            # Add the checkbox:
            chk_var = IntVar()
            u_shape_3d_index = self.mesh1.statistics['index'][i][0]
            check_box = Checkbutton(lb_frame,
                                    text=f'{i + 1} (ID: {u_shape_3d_index})',
                                    variable=chk_var,
                                    bg=rgb_to_hex(self.mesh1.protrusion_colors[i]))
            check_box.select()
            check_box.configure(command=lambda ind=i: self.checked(ind))
            self.checked_vars.append(chk_var)
            vsb_text.window_create("end", window=check_box)

            # Add the dropdown menu:
            box_var = StringVar()
            box_var.set(self.default_op_text)
            dropdown_menu = OptionMenu(lb_frame, box_var, *ops, command=self.dropdown_changed)
            dropdown_menu.config(bg=rgb_to_hex(self.mesh1.protrusion_colors[i]))
            # Todo: Consider whether or not we want to change this:
            dropdown_menu.config(state='disabled')
            self.optionmenus.append(box_var)
            self.dropdown_selections[i] = self.default_op_text
            vsb_text.window_create("end", window=dropdown_menu)

            # Add the backward/forward buttons:
            backward_button = Button(lb_frame, text='<-', command=lambda ind=i, is_backward=True:
            self.back_fwd_button_pressed(button_index=ind, is_backward=is_backward))
            vsb_text.window_create("end", window=backward_button)

            forward_button = Button(lb_frame, text='->', command=lambda ind=i, is_backward=False:
            self.back_fwd_button_pressed(button_index=ind, is_backward=False))
            vsb_text.window_create("end", window=forward_button)

            # Go to the next line:
            vsb_text.insert("end", "\n")  # to force one checkbox per line
