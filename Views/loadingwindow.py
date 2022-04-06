from tkinter import Button, Label, StringVar, Frame, Listbox, Scrollbar, messagebox
from tkinter.filedialog import askdirectory
from PIL import ImageTk, Image

# Import the constants we need:
from Model.constants_and_paths import LOADING_WINDOW_BACKGROUND_PATH, \
    PLUS_BUTTON_PATH, MINUS_BUTTON_PATH, NEXT_BUTTON_PATH


class LoadingWindow:

    def __init__(self, win, view_manager):
        self.win = win
        self.view_manager = view_manager

        background_load = Image.open(LOADING_WINDOW_BACKGROUND_PATH)
        background_width = 800
        background_height = 300
        background_load = background_load.resize(
            (background_width, background_height), Image.ANTIALIAS)
        background_img = ImageTk.PhotoImage(background_load)

        button_width = 50
        plus_button_load = Image.open(PLUS_BUTTON_PATH)
        delete_button_load = Image.open(MINUS_BUTTON_PATH)
        next_button_load = Image.open(NEXT_BUTTON_PATH)
        plus_button_load = plus_button_load.resize((button_width, button_width), Image.ANTIALIAS)
        delete_button_load = delete_button_load.resize(
            (button_width, button_width), Image.ANTIALIAS
        )
        next_button_load = next_button_load.resize((button_width, button_width), Image.ANTIALIAS)
        plus_button_img = ImageTk.PhotoImage(plus_button_load)
        delete_button_img = ImageTk.PhotoImage(delete_button_load)
        next_button_img = ImageTk.PhotoImage(next_button_load)

        self.background = Label(win, image=background_img)
        self.background.image = background_img
        self.background.place(
            x=(1200 - background_width) / 2, y=50
        )

        self.description_label = Label(win,
                                       text='Select the u-shape3D project directories IN ORDER:')
        self.description_label.config(font=("Courier", 12))
        self.description_label.place(x=(1200 - background_width) / 2, y=375)

        add_button = Button(win, text='+', command=self.add, image=plus_button_img)
        delete_button = Button(win, text='-', command=self.delete, image=delete_button_img)
        next_button = Button(win, text='Next', command=self.next, image=next_button_img)
        add_button.image = plus_button_img
        delete_button.image = delete_button_img
        next_button.image = next_button_img
        add_button.place(x=(1200 - background_width) / 2 + 650, y=500)
        delete_button.place(x=(1200 - background_width) / 2 + 705, y=500)
        next_button.place(x=1100, y=700)

        self.folders_var = StringVar()
        self.lb_frame = Frame(win, width=background_width, height=background_height)
        self.lb_frame.place(x=(1200 - background_width) / 2, y=500)
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
        path = askdirectory(title='Select Folder')
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
