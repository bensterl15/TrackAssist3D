import tkinter as tk
from tkinter import ttk

from Views.Frames.PreprocessFrame import PreprocessFrame
from Views.Frames.ProcessFrame import ProcessFrame
from Views.Frames.TestFrame import TestFrame
from Views.Frames.TrainingFrame import TrainingFrame


class SSGUILoadingWindow:

    def __init__(self, win, view_manager):
        self.win = win
        self.view_manager = view_manager
        self.current_view = "init"

        self.highLight = ttk.Style()
        self.highLight.configure("H.TLabel", background="#ccc")

        self.lowLight = ttk.Style()
        self.lowLight.configure("L.TLabel")

        self.completed = ttk.Style()
        self.completed.configure("C.TLabel", background="white")

        self.__create_widgets()



    def __create_widgets(self):
        self.processFrame = ProcessFrame(self.win)
        self.processFrame.place(x=300, y=50)

        self.trainFrame = TrainingFrame(self.win)
        self.testFrame = TestFrame(self.win)
        self.preprocessFrame = PreprocessFrame(self.win)

        self.label1 = ttk.Label(self.win, text='1. Process raw data', font=('Helvatical bold',15), style="H.TLabel")
        self.label1.place(x=50, y=50)

        self.label2 =  ttk.Label(self.win, text='2. Train', font=('Helvatical',15))
        self.label2.place(x=50, y=100)

        self.label3 =  ttk.Label(self.win, text='3. Test', font=('Helvatical',15))
        self.label3.place(x=50, y=150)

        self.label4 =  ttk.Label(self.win, text='4. Preprocess', font=('Helvatical',15))
        self.label4.place(x=50, y=200)

        self.prev_button = ttk.Button(self.win, text='Previous', command=self.previous)
        # self.prev_button.place(x=50, y=250)
        self.next_button = ttk.Button(self.win, text='Next', command=self.next)
        self.next_button.place(x=150, y=250)

        #TODO：Add a back to start button

    def next(self):
        if(self.current_view == "init"):
            self.label1.config(style="C.TLabel")
            self.label2.config(style="H.TLabel")

            self.processFrame.place_forget()
            self.prev_button.place(x=50, y=250)
            self.trainFrame.place(x=300, y=50)

            self.current_view = "train"
        elif(self.current_view == "train"):
            self.label2.config(style="C.TLabel")
            self.label3.config(style="H.TLabel")

            self.trainFrame.place_forget()
            self.testFrame.place(x=300, y=50)

            self.current_view = "test"
        elif (self.current_view == "test"):
            self.label3.config(style="C.TLabel")
            self.label4.config(style="H.TLabel")

            self.next_button.place_forget()
            self.testFrame.place_forget()
            self.preprocessFrame.place(x=300, y=50)

            self.current_view = "preprocess"


    def previous(self):

        if (self.current_view == "train"):
            self.label2.config(style="L.TLabel")
            self.label1.config(style="H.TLabel")

            self.prev_button.place_forget()
            self.trainFrame.place_forget()
            self.processFrame.place(x=300, y=50)

            self.current_view = "init"
        elif (self.current_view == "test"):
            self.label3.config(style="L.TLabel")
            self.label2.config(style="H.TLabel")

            self.testFrame.place_forget()
            self.trainFrame.place(x=300, y=50)

            self.current_view = "train"
        elif (self.current_view == "preprocess"):
            self.label4.config(style="L.TLabel")
            self.label3.config(style="H.TLabel")

            self.preprocessFrame.place_forget()
            self.testFrame.place(x=300, y=50)
            self.next_button.place(x=150, y=250)

            self.current_view = "test"


