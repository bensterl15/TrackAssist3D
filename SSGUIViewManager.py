from tkinter import Tk

from Views.SSGUILoadingWindow import SSGUILoadingWindow


class ViewManager:

    def __init__(self):
        self.active_window = Tk()
        SSGUILoadingWindow(self.active_window, self)

        window_width = 800
        window_height = 400

        # get the screen dimension
        screen_width = self.active_window.winfo_screenwidth()
        screen_height = self.active_window.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.active_window.title('SegmentationSkeletonGUI')
        self.active_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.active_window.mainloop()


    # def change_view(self, current_view):
    #     """Destroy current window and create a new one:"""
    #     self.active_window.destroy()
    #     self.active_window = Tk()
    #     # self.active_window.iconbitmap(ICON_PATH)
    #
    #     # TODO: Get this screen working for more than 2 cells at a time:
    #
    #     if current_view == 'start':
    #         LoadingWindow(self.active_window, self)
    #     elif current_view == 'load':
    #         ProcessWindow(self.active_window, self)
    #     elif current_view == 'Process':
    #         ProcessExpandWindow(self.active_window, self)
    #     elif current_view == 'ProcessExpand':
    #         TrainingWindow(self.active_window, self)
    #     elif current_view == 'Training':
    #         TestWindow(self.active_window, self)
    #     elif current_view == 'Test':
    #         PreprocessWindow(self.active_window, self)
    #     else:
    #         ExitWindow(self.active_window,self)
    #
    #     self.active_window.title('SegmentationSkeletonGUI')
    #     self.active_window.geometry("600x400+50+50")
    #
    #
    #     self.active_window.mainloop()