from tkinter import Button, StringVar, OptionMenu
import numpy as np

class StepsWindow:

    def __init__(self, win, view_manager):
        self.view_manager = view_manager
        num_cells = len(self.view_manager.base_dirs)

        # Configure Protrusion removal controls:
        removal_ops = list(np.linspace(1, num_cells, num_cells, dtype=int))
        self.removal_box_var = StringVar()
        self.removal_box_var.set(removal_ops[0])
        removal_dropdown_menu = OptionMenu(win, self.removal_box_var, *removal_ops)
        removal_button = Button(win,
                                text='Excess Protrusion Removal',
                                command=self.removal_view_requested
                                )

        # Configure Protrusion tracking controls:
        tracking_ops = []
        for index in range(len(removal_ops) - 1):
            tracking_ops.append(str(index+1) + ' to ' + str(index + 2))
        self.tracking_box_var = StringVar()
        self.tracking_box_var.set(tracking_ops[0])
        tracking_dropdown_menu = OptionMenu(win, self.tracking_box_var, *tracking_ops)
        tracking_button = Button(win,
                                 text='Protrusion Pair Tracking',
                                 command=self.tracking_view_requested
                                 )

        # Configure statistics and back buttons:
        stats_button = Button(win, text='View statistics', command=self.stats_view_requested)
        back_button = Button(win, text='Back To Start Screen', command=self.start_view_requested)

        # Protrusion removal controls placement
        removal_dropdown_menu.place(x=600, y=200)
        removal_button.place(x=700, y=200)

        # Tracking controls placement:
        tracking_dropdown_menu.place(x=600, y=300)
        tracking_button.place(x=700, y=300)

        # Statistics and back-button placement:
        stats_button.place(x=600, y=400)
        back_button.place(x=600, y=500)

    def start_view_requested(self):
        self.view_manager.back_to_start()

    def removal_view_requested(self):
        removal_selection = self.removal_box_var.get()
        # -1 because index is zero-based:
        self.view_manager.change_to_removal_view(int(removal_selection) - 1)

    def tracking_view_requested(self):
        tracking_pair_number = self.tracking_box_var.get()
        tracking_pair_number = tracking_pair_number.split(' to ')[0]
        tracking_pair_number = int(tracking_pair_number)
        # -1 because index is zero-based:
        self.view_manager.change_to_tracking_view(tracking_pair_number - 1)

    def stats_view_requested(self):
        self.view_manager.change_to_stats_view()
