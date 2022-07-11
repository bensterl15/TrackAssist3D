from tkinter import Button, Label, StringVar, Frame, Listbox, Scrollbar, messagebox, Checkbutton, BooleanVar
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
        background_height = 130
        background_load = background_load.resize(
            (background_width, background_height), Image.ANTIALIAS)
        background_img = ImageTk.PhotoImage(background_load)

        # Add and position background to window
        self.background = Label(win, image=background_img)
        self.background.image = background_img
        self.background.place(x=0, y=0)

        # Add and position welcome message and directions to window
        self.welcome_label = Label(win, text='Welcome to TrackAssist3D')
        self.welcome_label.config(font=("Times", 14, "bold italic"))
        self.welcome_label.place(x=170, y=135)

        self.namingConven_label = Label(win,
            text='Please name all u-shape3D project folders IN ORDER using the guide below\nbefore proceeding:'
                 '\nFor 2-9 folders: s1, s2, s3, etc.'
                 '\nFor 10-99 folders: s01, s02, s03, etc.'
                 '\nFor 100-999 folders: s001, s002, s003, etc.',
                                        justify='left',
                                        bg='#ff8a82',
                                        width=56,
                                        height=5)
        self.namingConven_label.config(font=('Times', 12))
        self.namingConven_label.place(x=20, y=158)

        self.boxDirections_label = Label(win, text='Indicate the location of the u-shape3D projects to be analyzed:')
        self.boxDirections_label.config(font=('Times', 12))
        self.boxDirections_label.place(x=20, y=260)

        self.description1_label = Label(win,
            text='If all u-shape3D project folders are in one directory, add it here.')
        self.description1_label.config(font=("Times", 12))
        self.description1_label.place(x=20, y=340)

        self.description2_label = Label(win,
            text='If u-shape3D project folders are in different directories, add them here.')
        self.description2_label.config(font=("Times", 12))
        self.description2_label.place(x=20, y=415)

        # Add checkboxes to indicate where to look for project folders.
        par_direct = BooleanVar()
        indiv_direct = BooleanVar()
        self.par_checkbox = Checkbutton(win, text='All u-shape3D project folders are in one directory.',
                                        variable=par_direct,
                                        onvalue=True,
                                        offvalue=False)
        self.indiv_checkbox = Checkbutton(win,
                                          text='One or more u-shape3D project folders are in different directories.',
                                          variable=indiv_direct,
                                          onvalue=True,
                                          offvalue=False)
        self.par_checkbox.place(x=20, y=285)
        self.indiv_checkbox.place(x=20, y=305)

        # Add and position buttons to window
        add_indiv_button = Button(win, text='Add Directory', command=self.add_indiv)
        delete_indiv_button = Button(win, text='Delete Directory', command=self.delete_indiv)
        add_super_button = Button(win, text='Add Super Directory', command=self.add_super)
        delete_super_button = Button(win, text='Delete Super Directory', command=self.delete_super)
        next_button = Button(win, text='Continue', command=self.next)

        add_indiv_button.place(x=20, y=555)
        delete_indiv_button.place(x=110, y=555)
        add_super_button.place(x=20, y=385)
        delete_super_button.place(x=145, y=385)
        next_button.place(x=475, y=560)

        # Create the list box for the super directory.
        self.parFolders_var = StringVar()
        self.par_frame = Frame(win, width=400, height=10)
        self.par_frame.place(x=20, y=360)
        self.listbox1 = Listbox(self.par_frame,
                                listvariable=self.parFolder_var,
                                width=80,
                                height=1,
                                selectmode='extended')
        self.listbox1.grid(column=0, row=0, sticky='nwes')

        # Create the list box for directories added individually.
        self.indivFolders_var = StringVar()
        self.lb_frame = Frame(win, width=400, height=40)
        self.lb_frame.place(x=20, y=445)
        self.listbox2 = Listbox(self.lb_frame,
                               listvariable=self.indivFolders_var,
                               width=80,
                               height=6,
                               selectmode='extended')
        self.listbox2.grid(column=0, row=0, sticky='nwes')
        scrollbar = Scrollbar(self.lb_frame, orient='vertical', command=self.listbox2.yview)
        self.listbox2['yscrollcommand'] = scrollbar.set
        scrollbar.grid(column=1, row=0, sticky='ns')

    # Add an individual directory.
    def add_indiv(self):
        path = askdirectory(title='Select Directory')
        self.listbox2.insert(self.listbox2.size(), path)

    # Add a super directory.
    def add_super(self):
        path = askdirectory(title='Select Super-Directory')
        self.listbox1.insert(self.listbox1.size(), path)
    # The user should be able to only add one parent directory (add to the checks in the next method).
    # The naming conventions should be dependent on the total number of projects:
        # If there are less than 9, s1, s2, s3, ...
        # If there are more than 10 but less than 100, s01, s02, s03, s04, ...
        # Add checks to examine folder names and correct mistakes automatically?

    # Delete an individual directory.
    def delete_indiv(self):
        num_deleted = 0
        for i in self.listbox2.curselection():
            self.listbox2.delete(i - num_deleted)
            num_deleted += 1

    # Delete a super directory.
    def delete_super(self):
        num_deleted = 0
        for i in self.listbox1.curselection():
            self.listbox1.delete(i-num_deleted)
            num_deleted += 1

    # Move on to the steps window if appropriate conditions are met.
    def next(self):
        directories = ()
        # Use nested if statements. Might be good to add a checkbox for the option used. If individual files, only
        # proceed if there are at least 2 directories. If parent directory, get all the folders and proceed if there
        # are at least 2. There should only be one parent directory added.

        #if self.par_checkbox.getboolean(self) == False and self.indiv_checkbox.getboolean(self) == False:
            #messagebox.showerror('Error', 'Folder selection method was not specified. Please select a box indicating
                #your folder selection method.')

        #elif self.par_checkbox.getboolean(self):
            #directories_var = self.parFolder_var.get()
            #for this path and below, process directories. Just for parent, find a way to access folders within the one entered.

        #elif self.indiv_checkbox.getBoolean(self):
            #directories_var = self.indivFolders_var.get()

        #elif self.par_checkbox.getboolean(self) and self.indiv_checkbox.getboolean(self):
            #messagebox.showerror('Error', 'Both directory options are checked. Please select one folder selection
                #method.')

        directories_var = self.indivFolders_var.get()
        b_proceed = True
        if len(directories_var) > 0:
            # Process the directories-list string
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
            messagebox.showerror('Error', 'Something happened. Fuck if I know.')
