from tkinter import Button, Label, StringVar, Frame, Listbox, Scrollbar, messagebox, Checkbutton, IntVar, Tk, END
from tkinter.filedialog import askdirectory
from PIL import ImageTk, Image
from os import listdir

import re

# Import the constants we need:
from Model.constants_and_paths import LOADING_WINDOW_BACKGROUND_PATH


class LoadingWindow:

    def __init__(self, win, view_manager):
        self.subdirectories = None
        self.win = win
        self.view_manager = view_manager

        # Initialize background variables
        background_load = Image.open(LOADING_WINDOW_BACKGROUND_PATH)
        background_width = 655
        background_height = 180
        background_load = background_load.resize(
            (background_width, background_height), Image.ANTIALIAS)
        background_img = ImageTk.PhotoImage(background_load)

        # Add and position background to window
        self.background = Label(win, image=background_img)
        self.background.image = background_img
        self.background.place(x=-5, y=0)

        # Add and position welcome message and directions to window
        self.welcome_label = Label(win, text='Welcome to TrackAssist3D')
        self.welcome_label.config(font=("Times", 14, "bold italic"))
        self.welcome_label.place(x=210, y=190)

        self.namingConven_label = Label(win,
                                        text='Please make sure all folders contain a frame number within their name.'
                                             '\nExample: The 10th frame could be named "surface10"',
                                        justify='center',
                                        bg='#ff8a82',
                                        width=67,
                                        height=5)
        self.namingConven_label.config(font=('Times', 12))
        self.namingConven_label.place(x=20, y=220)

        self.description1_label = Label(win,
                                        text='If all u-shape3D project folders are in one directory, add it here.')
        self.description1_label.config(font=("Times", 12))
        self.description1_label.place(x=20, y=335)

        self.description2_label = Label(win,
                                        text='If u-shape3D project folders are in separate directories, add them here.')
        self.description2_label.config(font=("Times", 12))
        self.description2_label.place(x=20, y=415)

        # Add and position buttons to window
        add_indiv_button = Button(win, text='Add Directory', command=self.add_indiv)
        delete_indiv_button = Button(win, text='Delete Directory', command=self.delete_indiv)
        add_super_button = Button(win, text='Add Super Directory', command=self.add_super)
        next_button = Button(win, text='Continue', command=self.next)

        add_indiv_button.place(x=20, y=555)
        delete_indiv_button.place(x=110, y=555)
        add_super_button.place(x=20, y=380)
        next_button.place(x=580, y=555)

        # Create the list box for the super directory.
        self.parFolders_var = StringVar()
        self.par_frame = Frame(win, width=400, height=10)
        self.par_frame.place(x=20, y=355)
        self.listbox1 = Listbox(self.par_frame,
                                listvariable=self.parFolders_var,
                                width=100,
                                height=1,
                                selectmode='extended')
        self.listbox1.grid(column=0, row=0, sticky='nwes')

        # Create the list box for directories added individually.
        self.indivFolders_var = StringVar()
        self.lb_frame = Frame(win, width=500, height=40)
        self.lb_frame.place(x=20, y=445)
        self.listbox2 = Listbox(self.lb_frame,
                                listvariable=self.indivFolders_var,
                                width=100,
                                height=6,
                                selectmode='extended')
        self.listbox2.grid(column=0, row=0, sticky='nwes')
        scrollbar = Scrollbar(self.lb_frame, orient='vertical', command=self.listbox2.yview)
        self.listbox2['yscrollcommand'] = scrollbar.set
        scrollbar.grid(column=1, row=0, sticky='ns')

    # Add a super directory, and add the subdirectories to the preview window listbox.
    def add_super(self):
        self.listbox1.delete(0, END)
        self.listbox2.delete(0, END)
        path = askdirectory(title='Select Super-Directory')
        self.listbox1.insert(self.listbox1.size(), path)

        # Show a list of the folders found in the super directory for confirmation.
        self.preview = Tk()
        self.preview.title('Subdirectories Preview')
        self.preview.geometry('650x300')

        # Directions to the user to check if all the desired files were found.
        self.preview.check_files_label = Label(self.preview,
                                               text='The following files were found in the super directory.\n'
                                                    'Click "Add to List" if the files below appear correct.',
                                               justify='center')
        self.preview.check_files_label.config(font=('Times', 14))
        self.preview.check_files_label.place(x=130, y=15)

        # Create a frame and listbox to display the subdirectories.
        self.preview.subFolders_var = StringVar()
        self.preview.sub_frame = Frame(self.preview, width='600', height='40')
        self.preview.sub_frame.place(x=15, y=80)
        self.preview.sub_listbox = Listbox(self.preview.sub_frame,
                                           listvariable=self.preview.subFolders_var,
                                           width=100,
                                           height=10,
                                           selectmode='extended')
        self.preview.sub_listbox.grid(column=0, row=0, sticky='nwes')
        sub_scrollbar = Scrollbar(self.preview.sub_frame, orient='vertical', command=self.preview.sub_listbox.yview)
        self.preview.sub_listbox['yscrollcommand'] = sub_scrollbar.set
        sub_scrollbar.grid(column=1, row=0, sticky='ns')

        # Add the subdirectories to the listbox.
        self.dirs_found_superdir = self.grab_subdirectories()
        for folder in self.dirs_found_superdir:
            self.preview.sub_listbox.insert(self.preview.sub_listbox.size(), folder)

        # Create and place buttons to continue or go back.
        continue_button = Button(self.preview, text='Add to List', command=self.add_subdirectories_to_grand_list)
        back_button = Button(self.preview, text='Return to Directory Selection', command=self.preview.destroy)
        continue_button.place(x=565, y=255)
        back_button.place(x=15, y=255)

    def add_subdirectories_to_grand_list(self):
        for dir in self.dirs_found_superdir:
            self.listbox2.insert(END, dir)

        # Programmatically close the addition screen:
        self.preview.destroy()

        # After all directories from the super list are transferred to the grand list, clear the variable:
        self.dirs_found_superdir = []

    # Grab subdirectories from the super directory and add them to the preview window.
    def grab_subdirectories(self):
        root = self.parFolders_var.get()[2:-3]
        sub_list = listdir(root)
        sort_list = [int(re.sub("[^0-9]", "", s)) for s in sub_list]
        sub_list = [x for _, x in sorted(zip(sort_list, sub_list))]

        for i in sub_list:
            sub_list[sub_list.index(i)] = root + '/' + sub_list[sub_list.index(i)]
        return sub_list

    # Add an individual directory, and add it to the individual directories listbox.
    def add_indiv(self):
        path = askdirectory(title='Select Directory')
        self.listbox2.insert(self.listbox2.size(), path)

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
            self.listbox1.delete(i - num_deleted)
            num_deleted += 1

    # Move on to the steps window if appropriate conditions are met.
    def next(self):
        dir_var = self.listbox2.get(0, END)

        if len(dir_var) == 0:
            messagebox.showerror('Error', 'No directories were found. If you are using a super directory, make sure '
                                          'the folder is not empty. If you are using individual directories, make sure '
                                          'all of them are present in the list before proceeding.')
        elif len(dir_var) < 2:
            messagebox.showerror('Error', 'At least 2 directories are needed to proceed. Less than 2 were found.')
        else:
            directories, good_check = self.process_and_continue(dir_var)
            if good_check:
                self.view_manager.change_to_step_view(directories)

    # Process the list of directories, check for illegal characters, and pass the directories to the next method.
    def process_and_continue(self, dir_var):
        directories = []
        illegal = [')', '(', '\\''']
        good_check = True
        for file in dir_var:
            for char in illegal:
                if file.find(char) != -1:
                    messagebox.showerror('Error', 'An illegal character was found in a directory. If any paths contain'
                                                  ' parentheses or backslashes, rename the necessary folders and try '
                                                  'again.')
                    good_check = False
                    break
            if good_check:
                directories.append(file)
            else:
                break
        directories = tuple(directories)
        return directories, good_check
