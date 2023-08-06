#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber, get_silica_index

micro = 1e-6

__all__ = ['DCF1300S_20',
           'DCF1300S_33',
           'F2028M24',
           'F2028M21',
           'F2028M12',
           'F2058G1',
           'F2058L1',
           'SMF28',
           'HP630',
           'CustomFiber',
           'get_silica_index']


class CustomFiber(GenericFiber):
    def __init__(self, wavelength: float, na_list: list, radius_list: list, name_list: list = None, position: tuple = (0, 0)):
        self.structure_dictionary = {}
        self.wavelength = wavelength
        self.position = position

        if name_list is None:
            name_list = [f'layer_{n}' for n in range(len(na_list))]

        self.add_air()

        for n, (na, radius) in enumerate(zip(na_list, radius_list)):
            self.add_next_structure_with_NA(
                name=name_list[n],
                na=na,
                radius=radius,
            )


class GradientFiber(GenericFiber):
    # Fiber from https://www.nature.com/articles/s41598-018-27072-2

    def __init__(self, wavelength: float, core_radius: float, delta_n: float, position: tuple = (0, 0)):
        self.structure_dictionary = {}
        self._wavelength = wavelength
        self._position = position
        self.delta_n = delta_n
        self.core_radius = core_radius
        self.brand = "Unknown"
        self.model = "Unknown"

        self.initialize()

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=125 / 2 * micro
        )

        self.add_next_structure_with_gradient(
            name='core',
            structure_index=self.silica_index + self.delta_n,
            radius=self.core_radius * micro,
            graded_index_factor=self.delta_n
        )


class DCF1300S_20(GenericFiber):
    brand = "COPL"
    model = "DCF1300S_20"

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=125 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='inner-clad',
            na=0.11,
            radius=19.9 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='core',
            na=0.12,
            radius=9.2 / 2 * micro
        )


class DCF1300S_33(GenericFiber):
    brand = "COPL"
    model = "DCF1300S_33"

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=125 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='inner-clad',
            na=0.11,
            radius=33.0 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='core',
            na=0.125,
            radius=9.0 / 2 * micro
        )


class F2058L1(GenericFiber):
    brand = "COPL"
    model = "F2058L1"

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=125 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='inner-clad',
            na=0.117,
            radius=19.6 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='core',
            na=0.13,
            radius=9.0 / 2 * micro
        )


class F2058G1(GenericFiber):
    brand = "COPL"
    model = "F2058G1"

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=125 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='inner-clad',
            na=0.115,
            radius=32.3 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='core',
            na=0.124,
            radius=9.0 / 2 * micro
        )


class F2028M24(GenericFiber):
    model = "F2028M24"

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=125 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='inner-clad',
            na=0.19,
            radius=14.1 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='core',
            na=0.11,
            radius=2.3 / 2 * micro
        )


class F2028M21(GenericFiber):
    model = "F2028M21"

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=125 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='inner-clad',
            na=0.19,
            radius=17.6 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='core',
            na=0.11,
            radius=2.8 / 2 * micro
        )


class F2028M12(GenericFiber):
    model = "F2028M12"

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=125 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='inner-clad',
            na=0.19,
            radius=25.8 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='core',
            na=0.11,
            radius=4.1 / 2 * micro
        )


class SMF28(GenericFiber):
    brand = 'Corning'
    model = "SMF28"

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=125 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='core',
            na=0.12,
            radius=8.2 / 2 * micro
        )


class HP630(GenericFiber):
    brand = 'Thorlab'
    model = "HP630"

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=125 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='core',
            na=0.13,
            radius=3.5 / 2 * micro
        )


class FiberCoreA(GenericFiber):
    brand = 'FiberCore'
    model = 'PS1250/1500'
    note = "Boron Doped Photosensitive Fiber"

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=124.9 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='core',
            na=0.12,
            radius=8.8 / 2 * micro
        )


class FiberCoreB(GenericFiber):
    brand = 'FiberCore'
    model = 'SM1250'

    def initialize(self):
        self.add_air()

        self.add_next_structure_with_NA(
            name='outer-clad',
            na=self.pure_silica_na,
            radius=125 / 2 * micro
        )

        self.add_next_structure_with_NA(
            name='core',
            na=0.12,
            radius=9 / 2 * micro
        )

# -
