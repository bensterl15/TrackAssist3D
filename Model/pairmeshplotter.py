import sys
from tkinter import messagebox
import pyvistaqt as vista
import pyvista as pv
import numpy as np


class PairMeshPlotter:
    def __init__(self, mesh1, mesh2):
        self.mesh1 = mesh1
        self.mesh2 = mesh2
        self.plotter = vista.MultiPlotter(nrows=2, ncols=1)
        self.plotter[0, 0].app_window.signal_close.connect(self.plotter_closed)
        self.plotter[1, 0].app_window.signal_close.connect(self.plotter_closed)

        for i, region in enumerate(self.mesh1.regions):
            # Add each protrusion to the plot:
            self.plotter[0, 0].add_mesh(region,
                                        color=self.mesh1.protrusion_colors[i],
                                        show_edges=False)
        self.base_actor1 = self.plotter[0, 0].add_mesh(self.mesh1.base_cell)

        self.protrusion_actors = []
        for i, region in enumerate(self.mesh2.regions):
            # Save the protrusion actors, so we can change their colors later:
            self.protrusion_actors.append(self.plotter[1, 0].add_mesh(
                region, color=self.mesh2.protrusion_colors[i], show_edges=False))
        self.base_actor2 = self.plotter[1, 0].add_mesh(self.mesh2.base_cell)

        # Save the protrusion pairings:
        self.protrusion_pairings = {}

        self.__programmatically_closed = False

    # When a user checks buttons, update the mesh visualization internally:
    def update_mesh1(self, checked, index):
        # If checked, turn on the protrusion:
        if checked == 1:
            self.protrusion_actors[index] = self.plotter[0, 0].add_mesh(
                self.mesh1.regions[index],
                color=self.mesh1.protrusion_colors[index],
                show_edges=False
            )
            self.mesh1.removed_protrusions.remove(self.mesh1.segmentation_unique[index + 1])
        # Else, turn off the protrusion:
        else:
            self.plotter[0, 0].remove_actor(self.protrusion_actors[index])
            self.mesh1.removed_protrusions.append(self.mesh1.segmentation_unique[index + 1])

        # Update base segmentation:
        self.plotter[0, 0].remove_actor(self.base_actor1)

        base_segmentation = np.zeros((self.mesh1.segmentation.shape[0]), dtype=bool)

        for i in range(base_segmentation.shape[0]):
            base_segmentation[i] = \
                self.mesh1.segmentation[i] in self.mesh1.removed_protrusions \
                or self.mesh1.segmentation[i] == 0

        base_faces = self.mesh1.mesh_faces[base_segmentation]
        # Create a polydata to store the base cell:
        self.mesh1.base_cell = pv.PolyData(self.mesh1.mesh_vertices, base_faces)
        self.base_actor1 = self.plotter[0, 0].add_mesh(self.mesh1.base_cell)

    # When a user checks buttons, update the mesh visualization internally:
    def update_mesh2(self, protrusion_one, checked_option):
        # If we select a new protrusion:
        if checked_option.isnumeric():

            # If protrusion_one is already in our dictionary,
            # it must be an outdated value, so set the output
            # protrusion to default:
            if protrusion_one in self.protrusion_pairings:
                self.change_back_to_default(protrusion_one)

            # Subtract 1 because python is zero-based:
            protrusion_two = int(checked_option) - 1

            # Remove the protrusion to change color:
            self.plotter[1, 0].remove_actor(self.protrusion_actors[protrusion_two])

            # Add the protrusion back in with the updated color:
            self.protrusion_actors.insert(
                protrusion_two,
                self.plotter[1, 0].add_mesh(
                    self.mesh2.regions[protrusion_two],
                    color=self.mesh1.protrusion_colors[protrusion_one]
                )
            )

            self.protrusion_pairings[protrusion_one] = protrusion_two

        # If it is not numeric, the user selected that the protrusion disappears:
        else:
            self.change_back_to_default(protrusion_one)

    def change_back_to_default(self, protrusion_one):
        # Get the protrusion_two to change back to black and remove from dictionary simultaneously:
        protrusion_two = self.protrusion_pairings.pop(protrusion_one)

        # Remove the protrusion to change color:
        self.plotter[1, 0].remove_actor(self.protrusion_actors[protrusion_two])

        # Add the protrusion back in with the updated color:
        self.protrusion_actors.insert(
            protrusion_two,
            self.plotter[1, 0].add_mesh(
                self.mesh2.regions[protrusion_two], color=[0, 0, 0]
            )
        )

    def plotter_closed(self):
        # We do not want the user closing the plotter by themselves,
        # so force the application to a close to avoid confusion:
        if not self.__programmatically_closed:
            messagebox.showerror('Error',
                                 'Closing the plotter is not allowed. The program must close now.')
            sys.exit()

    def finalize(self):
        self.__programmatically_closed = True
        self.plotter.close()
