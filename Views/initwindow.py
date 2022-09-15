import tkinter as tk
from tkinter import ttk


class InitWindow:

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
        self.label0 = ttk.Label(self.win, text='Choose the tool', font=('Helvatical bold', 15), style="H.TLabel")
        self.label0.place(x=50, y=50)


        self.button1 = ttk.Button(self.win, text='Go to: ', command=self.goToFiloTracker)
        self.button1.place(x=50, y=100)
        self.label1 =  ttk.Label(self.win, text='FiloTracker', font=('Helvatical',15))
        self.label1.place(x=150, y=100)

        self.button2 = ttk.Button(self.win, text='Go to: ', command=self.goToSegmentationSkeloton)
        self.button2.place(x=50, y=150)
        self.label2 =  ttk.Label(self.win, text='SegmentationSkeloton', font=('Helvatical',15))
        self.label2.place(x=150, y=150)



    def goToFiloTracker(self):
        self.view_manager.back_to_start()

    def goToSegmentationSkeloton(self):
        self.view_manager.go_to_SegmentationSkelotonGUI()