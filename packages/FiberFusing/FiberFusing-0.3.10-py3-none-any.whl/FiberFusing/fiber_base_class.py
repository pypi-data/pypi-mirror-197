#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy
from FiberFusing import Circle
from FiberFusing import plot_style
from FiberFusing.axes import Axes
from FiberFusing.utils import get_rho_gradient
import pprint
import logging

# MPSPlots imports
import MPSPlots.CMAP
from MPSPlots.Render2D import Scene2D, Axis, Mesh, Polygon, ColorBar

pp = pprint.PrettyPrinter(indent=4, sort_dicts=False, compact=True, width=1)


def get_silica_index(wavelength: float):
    # From https://refractiveindex.info/?shelf=main&book=SiO2&page=Malitson

    wavelength *= 1e6  # Put into micro-meter scale

    A_numerator = 0.6961663
    A_denominator = 0.0684043

    B_numerator = 0.4079426
    B_denominator = 0.1162414

    C_numerator = 0.8974794
    C_denominator = 9.896161

    index = (A_numerator * wavelength**2) / (wavelength**2 - A_denominator**2)
    index += (B_numerator * wavelength**2) / (wavelength**2 - B_denominator**2)
    index += (C_numerator * wavelength**2) / (wavelength**2 - C_denominator**2)
    index += 1
    index = numpy.sqrt(index)

    return index


class GenericFiber():
    pure_silica_na = 1.0417297132615746

    def __init__(self, wavelength: float, position: tuple = (0, 0)):
        self.structure_dictionary = {}
        self._wavelength = wavelength
        self._position = position
        self.brand = "Unknown"
        self.model = "Unknown"

        self.initialize()

    @property
    def position(self):
        if self._position is None:
            raise Exception("Position has not be defined for the fiber.")
        return self._position

    @position.setter
    def position(self, value: tuple):
        self._position = value
        self.initialize()

    @property
    def wavelength(self):
        if self._wavelength is None:
            raise Exception("Wavelength has not be defined for the fiber.")
        return self._wavelength

    @wavelength.setter
    def wavelength(self, value: tuple):
        self._wavelength = value
        self.initialize()

    @property
    def silica_index(self):
        return get_silica_index(wavelength=self.wavelength)

    def NA_to_core_index(self, NA: float, index_clad: float):
        return numpy.sqrt(NA**2 + index_clad**2)

    def core_index_to_NA(self, interior_index: float, exterior_index: float):
        return numpy.sqrt(interior_index**2 - exterior_index**2)

    @property
    def polygones(self):
        if not self._polygones:
            self.initialize_polygones()
        return self._polygones

    @property
    def full_structure(self):
        return self.structure_dictionary

    @property
    def fiber_structure(self):
        return {k: v for k, v in self.full_structure.items() if k not in ['air']}

    @property
    def inner_structure(self):
        return {k: v for k, v in self.full_structure.items() if k not in ['air', 'outer-clad']}

    def add_air(self):
        self.structure_dictionary['air'] = {
            "na": None,
            "radius": None,
            "index": 1,
            "V": None,
            "polygon": None
        }

    def add_next_structure_with_NA(self,
                                   name: str,
                                   na: float,
                                   radius: float):

        previous_structure_name = [*self.structure_dictionary.keys()][-1]

        exterior_index = self.structure_dictionary[previous_structure_name]['index']

        structure_index = self.NA_to_core_index(na, exterior_index)

        V = 2 * numpy.pi / self.wavelength * numpy.sqrt(structure_index**2 - exterior_index**2) * radius

        polygon = Circle(
            position=self.position,
            radius=radius,
            index=structure_index
        )

        self.structure_dictionary[name] = {
            "na": na,
            "radius": radius,
            "index": structure_index,
            "V": V,
            "polygon": polygon
        }

    def add_next_structure_with_index(self,
                                      name: str,
                                      structure_index: float,
                                      radius: float):

        previous_structure_name = [*self.structure_dictionary.keys()][-1]

        exterior_index = self.structure_dictionary[previous_structure_name]['index']

        na = self.core_index_to_NA(interior_index=structure_index, exterior_index=exterior_index)

        V = 2 * numpy.pi / self.wavelength * numpy.sqrt(structure_index**2 - exterior_index**2) * radius

        polygon = Circle(
            position=self.position,
            radius=radius,
            index=structure_index
        )

        self.structure_dictionary[name] = {
            "na": na,
            "radius": radius,
            "index": structure_index,
            "V": V,
            "polygon": polygon,
        }

    def add_next_structure_with_gradient(self,
                                      name: str,
                                      structure_index: float,
                                      radius: float,
                                      graded_index_factor: float = 0):

        polygon = Circle(
            position=self.position,
            radius=radius,
            index=structure_index
        )

        self.structure_dictionary[name] = {
            "radius": radius,
            "index": structure_index,
            "polygon": polygon,
            "graded_index_factor": graded_index_factor
        }

    def __str__(self):
        ID = ""

        ID += f"brand: {self.brand:<20s}\n"
        ID += f"model: {self.model:<20s}\n"
        ID += "structure:\n"

        for name, structure in self.fiber_structure.items():
            ID += f"\t{name:<20s}"
            for key, value in structure.items():
                if key == 'polygon':
                    continue
                ID += f"{key}: {value:<20.3}"
            ID += "\n"

        return ID

    def __repr__(self):
        return self.__str__()

    def render_patch_on_ax(self, ax: Axis, coordinate_axis: Axes) -> None:
        """
        Add the patch representation of the geometry into the given ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """

        for name, structure in self.fiber_structure.items():
            artist = Polygon(
                x=coordinate_axis.x_vector,
                y=coordinate_axis.y_vector,
                instance=structure['polygon']._shapely_object
            )

            ax.add_artist(artist)

        ax.set_style(**plot_style.geometry)
        ax.title = 'Fiber structure'

    def render_structure_on_ax(self, ax: Axis, structure, coordinate_axis: Axes) -> None:

        boolean_raster = structure['polygon'].get_rasterized_mesh(coordinate_axis=coordinate_axis)

        artist = Mesh(
            x=coordinate_axis.x_vector,
            y=coordinate_axis.y_vector,
            scalar=boolean_raster,
            colormap='Blues'
        )

        ax.add_artist(artist)

    def render_mesh_on_ax(self, ax: Axis, coordinate_axis: Axes):
        """
        Add the rasterized representation of the geometry into the given ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """

        colorbar = ColorBar(
            discreet=False,
            position='right',
            numeric_format='%.4f'
        )

        raster = self.overlay_structures(coordinate_axis=coordinate_axis)

        artist = Mesh(
            x=coordinate_axis.x_vector,
            y=coordinate_axis.y_vector,
            scalar=raster,
            colormap='Blues'
        )

        ax.colorbar = colorbar
        ax.title = 'Rasterized mesh'
        ax.set_style(**plot_style.geometry)
        ax.add_artist(artist)

    def render_gradient_on_ax(self, ax: Axis, coordinate_axis: Axes) -> None:
        """
        Add the rasterized representation of the gradient of the geometrys into the give ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """
        raster = self.overlay_structures(coordinate_axis=coordinate_axis)

        rho_gradient = get_rho_gradient(mesh=raster, coordinate_axis=coordinate_axis)

        colorbar = ColorBar(
            log_norm=True,
            position='right',
            numeric_format='%.1e',
            symmetric=True
        )

        artist = Mesh(
            x=coordinate_axis.x_vector,
            y=coordinate_axis.y_vector,
            scalar=rho_gradient,
            colormap=MPSPlots.CMAP.BWR
        )

        ax.colorbar = colorbar
        ax.title = 'Refractive index gradient'
        ax.set_style(**plot_style.geometry)
        ax.add_artist(artist)

    def shift_coordinates(self, coordinate_axis: Axis, x_shift: float, y_shift: float) -> numpy.ndarray:
        """
        Return the same coordinate system but x-y shifted

        :param      coordinates:  The coordinates
        :type       coordinates:  numpy.ndarray
        :param      x_shift:      The x shift
        :type       x_shift:      float
        :param      y_shift:      The y shift
        :type       y_shift:      float

        :returns:   The shifted coordinate
        :rtype:     numpy.ndarray
        """
        shifted_coordinate = coordinate_axis.to_unstructured_coordinate()
        shifted_coordinate[:, 0] -= x_shift
        shifted_coordinate[:, 1] -= y_shift

        return shifted_coordinate

    def get_shifted_distance(self, coordinate_axis: Axis, x_shift: float, y_shift: float, into_mesh: bool = True) -> numpy.ndarray:
        shifted_coordinate = self.shift_coordinates(
            coordinate_axis=coordinate_axis,
            x_shift=x_shift,
            y_shift=y_shift
        )

        distance = numpy.sqrt(shifted_coordinate[:, 0]**2 + shifted_coordinate[:, 1]**2)

        if into_mesh:
            distance = distance.reshape(coordinate_axis.shape)

        return distance

    def get_graded_index(self, coordinate_axis: numpy.ndarray, polygon, delta_n: float) -> numpy.ndarray:
        shifted_distance_mesh = self.get_shifted_distance(
            coordinate_axis=coordinate_axis,
            x_shift=polygon.center.x,
            y_shift=polygon.center.y,
            into_mesh=True
        )

        boolean_raster = polygon.get_rasterized_mesh(coordinate_axis=coordinate_axis)

        shifted_distance_mesh = -boolean_raster * shifted_distance_mesh**2

        shifted_distance_mesh -= shifted_distance_mesh.min()

        if shifted_distance_mesh.max() != 0:
            shifted_distance_mesh /= shifted_distance_mesh.max()
        else:
            logging.warning("Cannot apply graded index factor correctly!")
            return shifted_distance_mesh

        shifted_distance_mesh *= delta_n

        shifted_distance_mesh -= delta_n

        return shifted_distance_mesh

    def overlay_structures(self, coordinate_axis: Axis) -> numpy.ndarray:
        """
        Return a mesh overlaying all the structures in the order they were defined.

        :param      coordinate_axis:  The coordinates axis
        :type       coordinate_axis:  Axis

        :returns:   The raster mesh of the structures.
        :rtype:     numpy.ndarray
        """
        mesh = numpy.zeros(coordinate_axis.shape)

        return self.overlay_fiber_structures_on_mesh(mesh=mesh, coordinate_axis=coordinate_axis)

    def overlay_fiber_structures_on_mesh(self, mesh: numpy.ndarray, coordinate_axis: Axis) -> numpy.ndarray:
        """
        Return a mesh overlaying all the structures in the order they were defined.

        :param      coordinate_axis:  The coordinates axis
        :type       coordinate_axis:  Axis

        :returns:   The raster mesh of the structures.
        :rtype:     numpy.ndarray
        """
        return self._overlay_structures_on_mesh_(
            structure_dictionnary=self.fiber_structure,
            mesh=mesh,
            coordinate_axis=coordinate_axis
        )

    def overlay_inner_structures_on_mesh(self, mesh: numpy.ndarray, coordinate_axis: Axis) -> numpy.ndarray:
        """
        Return a mesh overlaying all the structures in the order they were defined.

        :param      coordinate_axis:  The coordinates axis
        :type       coordinate_axis:  Axis

        :returns:   The raster mesh of the structures.
        :rtype:     numpy.ndarray
        """
        return self._overlay_structures_on_mesh_(
            structure_dictionnary=self.inner_structure,
            mesh=mesh,
            coordinate_axis=coordinate_axis
        )

    def _overlay_structures_on_mesh_(self, structure_dictionnary: dict, mesh: numpy.ndarray, coordinate_axis: Axis) -> numpy.ndarray:
        """
        Return a mesh overlaying all the structures in the order they were defined.

        :param      coordinate_axis:  The coordinates axis
        :type       coordinate_axis:  Axis

        :returns:   The raster mesh of the structures.
        :rtype:     numpy.ndarray
        """
        for name, structure in structure_dictionnary.items():
            polygon = structure['polygon']
            raster = polygon.get_rasterized_mesh(coordinate_axis=coordinate_axis)
            mesh[numpy.where(raster != 0)] = 0
            index = structure['index']

            if structure.get('graded_index_factor', None) is not None:
                index += self.get_graded_index(
                    coordinate_axis=coordinate_axis,
                    polygon=polygon,
                    delta_n=structure['graded_index_factor']
                )

            raster *= index

            mesh += raster

        return mesh

    def plot(self, resolution: int = 300) -> None:
        """
        Plot the different representations [patch, raster-mesh, raster-gradient]
        of the geometry.

        :param      resolution:  The resolution to raster the structures
        :type       resolution:  int
        """
        max_radius: float = self.get_structures_max_radius()

        coordinate_axis = Axes(
            x_bounds=(-max_radius, max_radius),
            y_bounds=(-max_radius, max_radius),
            nx=resolution,
            ny=resolution
        )
        coordinate_axis.centering(factor=1.2)

        figure = Scene2D(unit_size=(4, 4), tight_layout=True)

        ax0 = Axis(row=0, col=0)
        ax1 = Axis(row=0, col=1)
        ax2 = Axis(row=0, col=2)

        self.render_patch_on_ax(ax=ax0, coordinate_axis=coordinate_axis)
        self.render_mesh_on_ax(ax=ax1, coordinate_axis=coordinate_axis)
        self.render_gradient_on_ax(ax=ax2, coordinate_axis=coordinate_axis)

        figure.add_axes(ax0, ax1, ax2)

        return figure

    def get_structures_max_radius(self) -> float:
        """
        Get the largest radius of all the defined structures except for air of course.

        :returns:   The structures maximum radius.
        :rtype:     float
        """
        radii = [
            structure['radius'] for structure in self.structure_dictionary.values()
        ]

        radii = numpy.asarray(radii).astype(float)

        radii = radii[~numpy.isnan(radii)]

        return radii.max()

