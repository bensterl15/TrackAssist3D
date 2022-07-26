from tkinter import Button, Label, StringVar, Frame, Listbox, Scrollbar, messagebox, Checkbutton, IntVar, Tk
from tkinter.filedialog import askdirectory
from PIL import ImageTk, Image
from os import listdir

import re

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
                                        text='Please make sure your folders contain frame number inside of their name.'
                                        '\nFor example the 10th frame could be named: surface10',
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
                                        text='If u-shape3D project folders are in separate directories, add them here.')
        self.description2_label.config(font=("Times", 12))
        self.description2_label.place(x=20, y=415)

        # Add checkboxes to indicate where to look for project folders.
        self.par_direct = IntVar()
        self.indiv_direct = IntVar()
        self.par_checkbox = Checkbutton(win, text='All u-shape3D project folders are in one directory.',
                                        variable=self.par_direct)
        self.indiv_checkbox = Checkbutton(win,
                                          text='One or more u-shape3D project folders are in different directories.',
                                          variable=self.indiv_direct)
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
                                listvariable=self.parFolders_var,
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

    # Add an individual directory, and assign it to the directory variable.
    def add_indiv(self):
        path = askdirectory(title='Select Directory')
        self.listbox2.insert(self.listbox2.size(), path)

    # Add a super directory, and add the subdirectories to the directory variable.
    def add_super(self):
        path = askdirectory(title='Select Super-Directory')
        self.listbox1.insert(self.listbox1.size(), path)

        # Show a list of the folders found in the super directory for confirmation.
        preview = Tk()
        preview.title('Subdirectories Preview')
        preview.geometry('700x300')

        # Directions to the user to check if all the desired files were found.
        preview.check_files_label = Label(preview,
                                          text='The following files were found in the super directory.\n'
                                               'If all the files you wish to process are present, click Continue.')
        preview.check_files_label.config(font=('Times', 14))
        preview.check_files_label.place(x=20, y=15)

        # Create a frame and listbox to display the subdirectories.
        preview.subFolders_var = StringVar()
        preview.sub_frame = Frame(preview, width='600', height='40')
        preview.sub_frame.place(x=30, y=80)
        preview.sub_listbox = Listbox(preview.sub_frame,
                                      listvariable=preview.subFolders_var,
                                      width=100,
                                      height=10,
                                      selectmode='extended')
        preview.sub_listbox.grid(column=0, row=0, sticky='nwes')
        sub_scrollbar = Scrollbar(preview.sub_frame, orient='vertical', command=preview.sub_listbox.yview)
        preview.sub_listbox['yscrollcommand'] = sub_scrollbar.set
        sub_scrollbar.grid(column=1, row=0, sticky='ns')

        # Add the subdirectories to the listbox.
        self.dirs_found = self.grab_subdirectories()
        for folder in self.dirs_found:
            preview.sub_listbox.insert(preview.sub_listbox.size(), folder)

        # Create and place buttons to continue or go back.
        continue_button = Button(preview, text='Continue', command=self.next)
        back_button = Button(preview, text='Return to Directory Selection', command=preview.destroy)
        continue_button.place(x=410, y=255)
        back_button.place(x=30, y=255)

    # Grab subdirectories from the super directory and add them to the preview window.
    def grab_subdirectories(self):
        root = self.parFolders_var.get()[2:-3]
        sub_list = listdir(root)
        sort_list = [int(re.sub("[A-Za-z_]", "", s)) for s in sub_list]
        sub_list = [x for _, x in sorted(zip(sort_list, sub_list))]

        for i in sub_list:
            sub_list[sub_list.index(i)] = root + '/' + sub_list[sub_list.index(i)]
        return sub_list

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
        # Make window showing all the directories found in the super directory
        # Use that listbox to grab individual files
        # Use the same code for super and individual directories.
        choice_check = True  # Validates that only one checkbox was checked.
        dir_check = True

        if self.par_direct.get() == 0 and self.indiv_direct.get() == 0:
            choice_check = False
            messagebox.showerror('Error', 'Folder selection method was not specified. Please select a box indicating '
                                          'your folder selection method.')

        elif self.par_direct.get() == 1 and self.indiv_direct.get() == 0:
            dir_var = self.dirs_found

        elif self.indiv_direct.get() == 1 and self.par_direct.get() == 0:
            dir_var = self.indivFolders_var.get()
            if len(dir_var) < 2:
                messagebox.showerror('Error', 'At least 2 directories are needed to proceed. Less than 2 were found.')
                dir_check = False

        elif self.par_direct.get() == 1 and self.indiv_direct.get() == 1:
            choice_check = False
            messagebox.showerror('Error', 'Both directory options are checked. Please select one folder selection '
                                          'method.')
        if choice_check and dir_check:
            directories = self.process_and_continue(dir_var)
            self.view_manager.change_to_step_view(directories)

    # Process the list of directories and move onto the steps window.
    def process_and_continue(self, dir_var):  # THIS STILL AIN'T WORKING
        directories = []
        illegal = [')', '(', '\\''']
        for file in dir_var:
            for char in illegal:
                if file.find(char) != -1:
                    messagebox.showerror('Error', 'An illegal character was found in a directory. If any paths contain'
                                                  'parentheses or backslashes, rename the necessary folders and try '
                                                  'again.')
            directories.append(file)
        directories = tuple(directories)

        # directories = tuple(map(str, dir_var ...

        if len(directories) < 2:
            messagebox.showerror('Error', 'At least two directories are needed to proceed. Less than 2 were found.')
        else:
            return directories

    # Check the order of the directories.
    def order_directories(self, dir_list):
        curr = 1
        order = True
        for i in dir_list:
            if not i.endswith(str(curr)):
                order = False
                break
            else:
                curr += 1
        return order

    # Check for naming conventions (for this, just that the folder name is s###). Optimize.
    def meets_conventions(self, directory_list):
        self.conven_met = True
        if len(directory_list) < 10:
            for i in directory_list:
                check = i[-1:-3]
                if check[0] != 's' or not check[1].isnumeric():
                    self.conven_met = False
                    break
        elif 10 <= len(directory_list) < 100:
            for i in directory_list:
                check = i[-1:-4]
                for i in directory_list:
                    check = i[-1:-4]
                    if check[0] != 's' or not check[1:3].isnumeric():
                        self.conven_met = False
                        break
        elif len(directory_list) < 1000:
            for i in directory_list:
                check = i[-1:-5]
                for i in directory_list:
                    check = i[-1:-5]
                    if check[0] != 's' or not check[1:4].isnumeric():
                        self.conven_met = False
                        break
        return self.conven_met