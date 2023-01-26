import os
import sys

DEBUG = True # False #


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


ANALYSIS_OFFSET = os.path.join('Morphology', 'Analysis')
MESH_PATH_OFFSET = os.path.join(ANALYSIS_OFFSET, os.path.join('Mesh', 'ch1'))
SURFACE_SEGMENT_PATH_OFFSET = os.path.join(ANALYSIS_OFFSET, os.path.join('SurfaceSegment', 'ch1'))
MOTIF_SEGMENT_PATH_OFFSET = os.path.join(ANALYSIS_OFFSET, 'MotifSegment')
REMOVAL_PATH_OFFSET = os.path.join(ANALYSIS_OFFSET, 'FiloTracker_Protrusion_Removal')
TRACKING_PATH_OFFSET = os.path.join(ANALYSIS_OFFSET, 'FiloTracker_Protrusion_Tracking')

VALID_USHAPE3D_DIR_ERROR_MSG = 'Please ensure all directories are valid u-shape3D directories (contains movieData.mat)'
MAX_PROTRUSIONS_INDEX = 1e8

ROOT_STR = ''

if DEBUG:
    ROOT_STR_ = '/Users/ben/Desktop/TrackAssist3D/'#"C:\\Users\\bsterling\\PycharmProjects\\FiloTracker\\"
    PAIRING_WINDOW_BACKGROUND_PATH = ROOT_STR_ + "TA3D_Logo.PNG"
    REMOVER_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    LOADING_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    PLUS_BUTTON_PATH = ROOT_STR_ + "plus_button.PNG"
    MINUS_BUTTON_PATH = ROOT_STR_ + "minus_button.PNG"
    NEXT_BUTTON_PATH = ROOT_STR_ + "next_button.PNG"
    ICON_PATH = ROOT_STR_ + "TA3D_Icon.ico"
else:
    PAIRING_WINDOW_BACKGROUND_PATH = resource_path('TA3D_Logo.PNG')
    REMOVER_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    LOADING_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    PLUS_BUTTON_PATH = resource_path("plus_button.PNG")
    MINUS_BUTTON_PATH = resource_path("minus_button.PNG")
    NEXT_BUTTON_PATH = resource_path("next_button.PNG")
    ICON_PATH = resource_path("TA3D_Icon.ico")
