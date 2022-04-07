from random import randint
import numpy as np

import pyvista as pv
import mat73
from scipy.io import loadmat

from Model.constants_and_paths import MAX_PROTRUSIONS_INDEX


class Mesh:

    def __init__(self, path_mesh, path_segmentation, path_statistics, black_protrusions=False, default_base=True):
        # Load the segmentation:
        self.segmentation = self.load_segmentation(path_segmentation)
        # We mostly care about the unique segmentation
        self.segmentation_unique = np.unique(self.segmentation)

        # Load the mesh statistics:
        self.statistics = self.load_statistics(path_statistics)

        mesh_dict = mat73.loadmat(path_mesh)
        # Load numpy arrays of the vertices and faces:
        mesh_vertices = mesh_dict['surface']['vertices']
        mesh_faces = mesh_dict['surface']['faces']

        # Cast faces to int.. Subtract 1 to change from MATLAB 1-indexed:
        mesh_faces = mesh_faces.astype(int) - 1
        # We need to put 3's in front of each face to indicate it is a triangle:
        mesh_faces = np.hstack((3 * np.ones((mesh_faces.shape[0], 1), dtype=int), mesh_faces))

        # Will need these later:
        self.mesh_faces = mesh_faces
        self.mesh_vertices = mesh_vertices

        # Prepare base segmentation
        if default_base:
            base_faces = mesh_faces
        else:
            base_faces = mesh_faces[self.segmentation == 0]
        # Create a polydata to store the base cell:
        self.base_cell = pv.PolyData(mesh_vertices, base_faces)

        self.regions = []
        for i in range(1, self.segmentation_unique.shape[0]):
            region_faces = mesh_faces[self.segmentation == self.segmentation_unique[i]]
            # Create a polydata to store the base cell:
            region = pv.PolyData(mesh_vertices, region_faces)
            self.regions.append(region)

        # Generate black protrusions:
        if black_protrusions:
            self.protrusion_colors = np.zeros((self.segmentation_unique.shape[0] - 1, 3))
        # Generate ordered colors:
        else:
            # Weight the colors, because we do not want anything too close to black or white:
            self.protrusion_colors = np.random.uniform(size=(self.segmentation_unique.shape[0] - 1, 3)) * 0.3 + 0.3

        self.removed_protrusions = []

    # When the user saves after removal section, finalize the mesh:
    def removal_finalize(self):
        # Set all the segmentation indices we removed to zero:
        for i in range(self.segmentation.shape[0]):
            if self.segmentation[i] in self.removed_protrusions:
                self.segmentation[i] = 0

        # Recalculate unique segmentation as we removed a few:
        self.segmentation_unique = np.unique(self.segmentation)

        # Gather the indices of the statistics we wish to remove:
        indices_to_remove = []
        # -1 because we do not count the base:
        for i in range(np.shape(self.statistics['index'])[0]):
            if self.statistics['index'][i] in self.removed_protrusions:
                indices_to_remove.append(i)

        # Finally, remove all the entries that came from removed protrusions:
        for key in self.statistics:
            self.statistics[key] = np.delete(self.statistics[key], np.array(indices_to_remove), 0)

        azimuth = []
        inclination = []
        for protrusion in self.segmentation_unique:
            # If zero, then we have the cell-base which is not what we are interested in:
            if protrusion != 0:
                angles = self._calculate_spherical_angles(protrusion=protrusion)
                azimuth.append(angles[0])
                inclination.append(angles[1])

        self.statistics['azimuth'] = np.array(azimuth)
        self.statistics['inclination'] = np.array(inclination)

    # When the user saves progress of tracking, finalize the SECOND MESH ONLY:
    def tracking_finalize(self, previous_mesh, pairings):
        # [1:] because we ignore the base of zero:
        p1_indices = previous_mesh.segmentation_unique[1:]
        p2_indices = self.segmentation_unique[1:]

        index_permutation = {}

        # Save all protrusion permutation's so that tracking can be
        # performed upon statistic compilation:
        for protrusion_one_index in pairings:
            index_permutation[
                int(p1_indices[protrusion_one_index])
            ] = int(p2_indices[pairings[protrusion_one_index]])

        return index_permutation

    def _calculate_spherical_angles(self, protrusion):
        # First load the list of faces:
        faces = self.mesh_faces[self.segmentation == protrusion]
        # We only care about the unique vertices that are in the list:
        faces = np.unique(faces.flatten())
        vertices_unique = self.mesh_vertices[faces]
        mean = np.mean(vertices_unique, axis=0)
        vertices_centered = vertices_unique - mean
        # This is like an estimation of multi-dimensional normal covariance matrix estimator:
        cov_hat = np.matmul(np.transpose(vertices_centered), vertices_centered) / (np.shape(vertices_centered)[0] - 1)
        L, Q = np.linalg.eig(cov_hat)
        greatest_eval_index = np.argmax(L)
        principal_direction = Q[:, greatest_eval_index]

        # x^z + y^2 + z^2 = 1, because eig produces unitary Q
        x = principal_direction[0]
        y = principal_direction[1]
        z = principal_direction[2]

        azimuth = 0
        # Need to break up cases to make calculation numerically stable:
        if x > 0:
            azimuth = np.arctan(y / x)
        elif x < 0 and y >= 0:
            azimuth = np.arctan(y / x) + np.pi
        elif x < 0 and y < 0:
            azimuth = np.arctan(y / x) - np.pi
        elif x == 0 and y > 0:
            azimuth = np.pi / 2
        elif x == 0 and y < 0:
            azimuth = -np.pi / 2
        # Do not address x=0,y=0 as this angle is undefined and
        # occurs with probability zero, hopefully:
        inclination = np.arccos(z)

        # Report in degrees:
        azimuth = np.degrees(azimuth)
        inclination = np.degrees(inclination)

        azimuth = (azimuth + 36000) % 360
        inclination = (inclination + 36000) % 360

        return (azimuth, inclination)


    # Don't know how, but this should be STATIC METHOD:
    # (We will use it again later in the statistics step:)
    def load_statistics(self, path_statistics):
        # mat file is either new or old version:
        try:
            stats_dict = mat73.loadmat(path_statistics)
        except:
            stats_dict = loadmat(path_statistics)

        try:
            stats_dict = stats_dict['blebStats']
            # 3 surface area, 11 volume:
            converted_stats_dict = {'index': stats_dict[0][0][0][0][0],
                                    'volume': stats_dict[0][0][0][0][11],
                                    'surface_area': stats_dict[0][0][0][0][3]}
        except:
            # If we get an exception, it is because we are loading at the tracking step:
            converted_stats_dict = stats_dict

        return converted_stats_dict

    def load_segmentation(self, path_segmentation):
        # mat file is either new or old version:
        try:
            segment_dict = mat73.loadmat(path_segmentation)
        except:
            segment_dict = loadmat(path_segmentation)

        # Mat file contains either blebSegment variable or surfaceSegment variable:
        try:
            segmentation = segment_dict['blebSegment']
        except:
            segmentation = segment_dict['surfaceSegment']
            segmentation = np.squeeze(segmentation)
        return segmentation