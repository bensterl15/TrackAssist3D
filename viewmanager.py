'''Import the necessary GUI modules:'''
import os.path
from tkinter import Tk, messagebox
from Views.removerwindow import RemoverWindow
from Views.pairingwindow import PairingWindow
from Views.loadingwindow import LoadingWindow
from Views.stepswindow import StepsWindow
from Views.statisticswindow import StatisticsWindow

from Model.constants_and_paths import VALID_USHAPE3D_DIR_ERROR_MSG, ICON_PATH, TRACKING_PATH_OFFSET

class ViewManager:
    """Class that manages the views (changes views etc etc)"""

    def __init__(self):
        self.active_window = Tk()
        self.active_window.iconbitmap(ICON_PATH)
        LoadingWindow(self.active_window, self)

        self.base_dirs = ()
        # Keep track of which cell we are currently removing protrusions from:
        self.active_cell = 0
        # Keep track of which cell-pair we are tracking currently:
        self.active_pair = 0
        # Keep track of a minimum index if we need to relabel protrusions:
        self.min_index = 0

        self.active_window.title('TrackAssist3D')
        self.active_window.geometry("550x500")
        self.active_window.mainloop()


    def change_view(self, current_view):
        """Destroy current window and create a new one:"""
        self.active_window.destroy()
        self.active_window = Tk()
        self.active_window.iconbitmap(ICON_PATH)

        # TODO: Get this screen working for more than 2 cells at a time:

        if current_view == 'start':
            LoadingWindow(self.active_window, self)
        elif current_view == 'step':
            StepsWindow(self.active_window, self)
        elif current_view == 'removal':
            RemoverWindow(self.active_window, self, base_directory=self.base_dirs[self.active_cell])
        elif current_view == 'tracking':
            PairingWindow(self.active_window, self, base_directory1=self.base_dirs[self.active_pair],
                          base_directory2=self.base_dirs[self.active_pair + 1])
        elif current_view == 'stats':
            incomplete_tracking_pairs = self.tracking_incomplete()
            if not incomplete_tracking_pairs:
                StatisticsWindow(self.active_window, self)
            else:
                incomplete_tracking_pairs = [f'from {i} to {i+1}' for i in incomplete_tracking_pairs]
                messagebox.\
                    showerror('Error',
                              'The following tracking has not been performed: '
                              + ', '.join(incomplete_tracking_pairs))
                StepsWindow(self.active_window, self)

        self.active_window.title('FiloTracker')
        self.active_window.geometry("1200x800+50+50")
        self.active_window.mainloop()

    def change_to_step_view(self, directories):
        """Change to the steps view:"""
        # Check if directories are valid u-shape3D directories:
        directories_are_valid = True
        for directory in directories:
            if not os.path.isfile(os.path.join(directory, 'movieData.mat')):
                directories_are_valid = False

        if directories_are_valid:
            self.base_dirs = directories
            self.change_view('step')
        else:
            messagebox.showerror('Error', VALID_USHAPE3D_DIR_ERROR_MSG)

    def change_to_removal_view(self, index):
        """Change to the protrusion removal view:"""
        self.active_cell = index
        self.change_view('removal')

    def change_to_tracking_view(self, index):
        """Change to the protrusion tracking view:"""
        self.active_pair = index
        self.change_view('tracking')

    def change_to_stats_view(self):
        """Change to the statistics-display view:"""
        self.change_view('stats')

    def back_to_start(self):
        """Change back to the starting view:"""
        self.change_view('start')

    def back_to_step(self):
        """Change to the steps view:"""
        self.change_view('step')

    def tracking_incomplete(self):
        """Job of this method is to check whether we are ready for results:"""
        incomplete_pairs = []
        for index, dir_ in enumerate(self.base_dirs):
            t_dir = os.path.join(dir_, TRACKING_PATH_OFFSET)
            # We expect that the first model does not have tracking data:
            if not os.path.exists(t_dir) and index > 0:
                incomplete_pairs.append(index)
        return incomplete_pairs
