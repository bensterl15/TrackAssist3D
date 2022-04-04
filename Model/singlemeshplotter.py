import sys
from tkinter import messagebox
import numpy as np
import pyvistaqt as pvqt
import pyvista as pv


class SingleMeshPlotter:
    def __init__(self, mesh):
        self.mesh = mesh
        self.plotter = pvqt.BackgroundPlotter()
        self.plotter.app_window.signal_close.connect(self.plotter_closed)
        self.protrusion_actors = {}
        self.programmatically_closed = False

        '''
        for i, region in enumerate(self.mesh.regions):
            # Save the protrusion actors so we can hide them later:
            self.protrusion_actors.append(
                self.plotter.add_mesh(region,
                                      color=self.mesh.protrusion_colors[i],
                                      show_edges=False))
        '''
        for i, _ in enumerate(self.mesh.regions):
            self.mesh.removed_protrusions.append(self.mesh.segmentation_unique[i + 1])
        self.base_actor = self.plotter.add_mesh(self.mesh.base_cell)

    # When a user checks buttons, update the mesh visualization internally:
    def update(self, checked, index):
        print(index)
        # If checked, turn on the protrusion:
        if checked == 1:
            self.protrusion_actors[index] = self.plotter.add_mesh(
                self.mesh.regions[index],
                color=self.mesh.protrusion_colors[index],
                show_edges=False)
            self.mesh.removed_protrusions.remove(self.mesh.segmentation_unique[index + 1])
        # Else, turn off the protrusion:
        else:
            self.plotter.remove_actor(self.protrusion_actors[index])
            self.mesh.removed_protrusions.append(self.mesh.segmentation_unique[index + 1])

        # Update base segmentation:
        self.plotter.remove_actor(self.base_actor)

        base_segmentation = np.zeros((self.mesh.segmentation.shape[0]), dtype=bool)

        for i in range(base_segmentation.shape[0]):
            base_segmentation[i] = \
                self.mesh.segmentation[i] in self.mesh.removed_protrusions \
                or self.mesh.segmentation[i] == 0

        base_faces = self.mesh.mesh_faces[base_segmentation]
        # Create a polydata to store the base cell:
        self.mesh.base_cell = pv.PolyData(self.mesh.mesh_vertices, base_faces)
        self.base_actor = self.plotter.add_mesh(self.mesh.base_cell)

    def plotter_closed(self):
        # We do not want the user closing the plotter by themselves,
        # so force the application to a close to avoid confusion:
        if not self.programmatically_closed:
            messagebox.showerror('Error',
                                 'Closing the plotter is not allowed. The program must close now.')
            sys.exit()

    def finalize(self):
        self.programmatically_closed = True
        self.plotter.close()
