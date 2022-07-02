from tkinter import Button, Label, StringVar, Frame, Listbox, Scrollbar, messagebox
from tkinter.filedialog import askdirectory
from PIL import ImageTk, Image

# Import the constants we need:
from Model.constants_and_paths import LOADING_WINDOW_BACKGROUND_PATH


class LoadingWindow:

    def __init__(self, win, view_manager):
        self.win = win
        self.view_manager = view_manager

        # Initialize background variables
        background_load = Image.open(LOADING_WINDOW_BACKGROUND_PATH)
        background_width = 550
        background_height = 125
        background_load = background_load.resize(
            (background_width, background_height), Image.ANTIALIAS)
        background_img = ImageTk.PhotoImage(background_load)

        # Add and position background to window
        self.background = Label(win, image=background_img)
        self.background.image = background_img
        self.background.place(x=0, y=0)

        # Add and position welcome message to window
        self.welcome_label = Label(win, text='Welcome to TrackAssist3D')
        self.welcome_label.config(font=("Times", 14, "bold italic"))
        self.welcome_label.place(x=170, y=130)

        # Add and position directions to window
        self.description1_label = Label(win,
            text='If all u-shape3D project directories are in one folder, add the parent directory.')
        self.description1_label.config(font=("Times", 12))
        self.description1_label.place(x=20, y=160)

        self.description2_label = Label(win,
            text='If u-shape3D project directories are in different folders, add directories individually.')
        self.description2_label.config(font=("Times", 12))
        self.description2_label.place(x=20, y=310)

        # Add and position buttons to window
        add_button = Button(win, text='Add Directory', command=self.add)
        delete_button = Button(win, text='Delete Directory', command=self.delete)
        parent_button = Button(win, text='Add Parent Directory') # Needs a command!
        next_button = Button(win, text='Continue', command=self.next)

        add_button.place(x=20, y=450)
        delete_button.place(x=110, y=450)
        parent_button.place(x=20, y=280)
        next_button.place(x=475, y=460)

        self.folders_var = StringVar()
        self.lb_frame = Frame(win, width=400, height=40)
        self.lb_frame.place(x=20, y=340)
        self.listbox = Listbox(self.lb_frame,
                               listvariable=self.folders_var,
                               width=80,
                               height=6,
                               selectmode='extended')
        self.listbox.grid(column=0, row=0, sticky='nwes')
        scrollbar = Scrollbar(self.lb_frame, orient='vertical', command=self.listbox.yview)
        self.listbox['yscrollcommand'] = scrollbar.set
        scrollbar.grid(column=1, row=0, sticky='ns')

    def add(self):
        path = askdirectory(title='Select Directory')
        self.listbox.insert(self.listbox.size(), path)

    # TODO: How do I grab all the files in the folder and add them for processing?
    def add_parent(self):
        path = askdirectory(title='Select Parent Directory')
        self.listbox.insert(self.listbox.size(), path)

    def delete(self):
        num_deleted = 0
        for i in self.listbox.curselection():
            self.listbox.delete(i - num_deleted)
            num_deleted += 1

    def next(self):
        directories = ()
        directories_var = self.folders_var.get()
        b_proceed = True
        if len(directories_var) > 0:
            # Process the directories-list string... UGH
            directories = tuple(map(str, directories_var
                                    .replace('(', '')
                                    .replace(')', '')
                                    .replace('\'', '')
                                    .split(', ')))

            if len(directories) < 2:
                # If we have less than 2 directories, do not proceed:
                b_proceed = False
        else:
            # If the user does not enter anything, do not proceed:
            b_proceed = False

        if b_proceed:
            self.view_manager.change_to_step_view(directories)
        else:
            messagebox.showerror('Error', 'Need at least 2 elements to proceed:')
