import os
import sys

DEBUG = True


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

if DEBUG:
    ROOT_STR = "C:\\Users\\jewel\\Desktop\\Project Files\\FiloTracker\\"
    PAIRING_WINDOW_BACKGROUND_PATH = ROOT_STR + "TA3D_Logo.PNG"
    REMOVER_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    LOADING_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    ICON_PATH = ROOT_STR+"TA3D_Icon.ico"
else:
    PAIRING_WINDOW_BACKGROUND_PATH = resource_path('TA3D_Logo.PNG')
    REMOVER_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    LOADING_WINDOW_BACKGROUND_PATH = PAIRING_WINDOW_BACKGROUND_PATH
    ICON_PATH = resource_path("TA3D_Icon.ico")
