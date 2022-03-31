import os
import sys

DEBUG = False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ANALYSIS_OFFSET = 'Morphology\\Analysis\\'
MESH_PATH_OFFSET = os.path.join(ANALYSIS_OFFSET, 'Mesh\\ch1\\')
SURFACE_SEGMENT_PATH_OFFSET = os.path.join(ANALYSIS_OFFSET, 'SurfaceSegment\\ch1\\')
MOTIF_SEGMENT_PATH_OFFSET = os.path.join(ANALYSIS_OFFSET, 'MotifSegment\\')
REMOVAL_PATH_OFFSET = os.path.join(ANALYSIS_OFFSET, 'FiloTracker_Protrusion_Removal')


if DEBUG:
    PAIRING_WINDOW_BACKGROUND_PATH = "C:\\Users\\bsterling\\Pictures\\FiloTracker Logo.PNG"
    REMOVER_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    LOADING_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    PLUS_BUTTON_PATH = "C:\\Users\\bsterling\\Pictures\\plus_button.PNG"
    MINUS_BUTTON_PATH = "C:\\Users\\bsterling\\Pictures\\minus_button.PNG"
    NEXT_BUTTON_PATH = "C:\\Users\\bsterling\\Pictures\\next_button.PNG"
    ICON_PATH = "C:\\Users\\bsterling\\Pictures\\filotracker.ico"
else:
    PAIRING_WINDOW_BACKGROUND_PATH = resource_path('FiloTracker Logo.PNG')
    REMOVER_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    LOADING_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    PLUS_BUTTON_PATH = resource_path("plus_button.PNG")
    MINUS_BUTTON_PATH = resource_path("minus_button.PNG")
    NEXT_BUTTON_PATH = resource_path("next_button.PNG")
    ICON_PATH = resource_path("filotracker.ico")

VALID_USHAPE3D_DIR_ERROR_MSG = 'Please ensure all directories are valid u-shape3D directories (contains movieData.mat)'
MAX_PROTRUSIONS_INDEX = 1e8