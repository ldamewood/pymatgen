#!/usr/bin/python

import unittest
import sys

import numpy as np

from pymatgen.defects.point_defects import Vacancy, Interstitial
from pymatgen.core.structure import  Structure
from pymatgen.core.lattice import Lattice
from pymatgen.core.periodic_table import  Element
from pymatgen.symmetry.finder import SymmetryFinder 
from pymatgen.symmetry.spacegroup import Spacegroup

class VacancyTest(unittest.TestCase):
    def setUp(self):
        """
        Setup MgO rocksalt structure for testing Vacancy
        """
        mgo_latt = [[4.212, 0, 0], [0, 4.212, 0], [0, 0, 4.212]]
        mgo_specie = ["Mg"]*4 +  ["O"]*4
        mgo_frac_cord = [[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5],
                         [0.5, 0, 0], [0, 0.5, 0], [0, 0, 0.5], [0.5, 0.5, 0.5]]
        self._mgo_uc = Structure(mgo_latt, mgo_specie, mgo_frac_cord, True, True)
        self._mgo_vac = Vacancy(self._mgo_uc)
    
    def test_defectsite_count(self):
        self.assertTrue(self._mgo_vac.defectsite_count() == 2, 
                "Vacancy count wrong")

    def test_enumerate_defectsites(self):
        """
        The vacancy sites should be the lattice sites. 
        And there should be only two unique vacancy sites for MgO.
        """
        uniq_sites = []
        uniq_sites.append(self._mgo_uc.sites[3])
        uniq_sites.append(self._mgo_uc.sites[7])
        uniq_def_sites = self._mgo_vac.enumerate_defectsites()
        #Match uniq_sites iwth uniq_def_sites
        #self.assertTrue(len(uniq_def_sites) == 2, "Vacancy init failed")
        #mgo_spg = Spacegroup(int_number=225)
        #self.assertTrue(mgo_spg.are_symmetrically_equivalent(uniq_sites,
        #                uniq_def_sites),  "Vacancy init failed")

    def test_get_defectsite_index(self):
        for i in range(self._mgo_vac.defectsite_count()):
            self.assertTrue(self._mgo_vac.get_defectsite_index(i) < 
                    len(self._mgo_uc.sites), "Defect site index beyond range")

    def test_gt_defectsite_coordination_number(self):
        for i in range(self._mgo_vac.defectsite_count()):
            self.assertTrue(round(self._mgo_vac.get_defectsite_coordination_number(
                i))==6.0, "Wrong coordination number")

    def test_get_defectsite_coordinated_elements(self):
        for i in range(self._mgo_vac.defectsite_count()):
            site_index = self._mgo_vac.get_defectsite_index(i)
            site_el = self._mgo_uc[site_index].species_and_occu
            self.assertTrue(
                    site_el not in self._mgo_vac.get_coordinated_elements(
                        i), "Coordinated elements are wrong")

    def test_get_defectsite_effective_charge(self):
        for i in range(self._mgo_vac.defectsite_count()):
            site_index = self._mgo_vac.get_defectsite_index(i)
            site_el = self._mgo_uc[site_index].species_and_occu
            eff_charge = self._mgo_vac.get_defectsite_effective_charge(i)
            if site_el["Mg"] == 1:
                self.assertEqual(eff_charge, -2)
            if site_el["O"] == 1:
                self.assertEqual(eff_charge, 2)

    def test_get_coordinatedsites_min_max_charge(self):
        for i in range(self._mgo_vac.defectsite_count()):
            min_chrg, max_chrg = self._mgo_vac.get_coordsites_min_max_charge(i)
            self.assertEqual(min_chrg, max_chrg)

    def test_get_volume(self):
        for i in range(self._mgo_vac.defectsite_count()):
            vol = self._mgo_vac.get_volume(i)
            #Once the zeo++ is properly working, make sure vol is +ve
            self.assertIsInstance(vol, float)

    def test_get_surface_area(self):
        for i in range(self._mgo_vac.defectsite_count()):
            sa = self._mgo_vac.get_surface_area(i)
            #Once the zeo++ is properly working, make sure vol is +ve
            self.assertIsInstance(sa, float)
        
        
class InterstitialTest(unittest.TestCase):
    def setUp(self):
        """
        Setup MgO rocksalt structure for testing Interstitial
        """
        mgo_latt = [[4.212, 0, 0], [0, 4.212, 0], [0, 0, 4.212]]
        mgo_specie = ["Mg"]*4 +  ["O"]*4
        mgo_frac_cord = [[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5],
                         [0.5, 0, 0], [0, 0.5, 0], [0, 0, 0.5], [0.5, 0.5, 0.5]]
        self._mgo_uc = Structure(mgo_latt, mgo_specie, mgo_frac_cord, True, True)
        self._mgo_interstitial = Interstitial(self._mgo_uc)
    
    def test_enumerate_defectsites(self):
        """
        The interstitial sites should be within the lattice
        """
        uniq_def_sites = self._mgo_interstitial.enumerate_defectsites()
        self.assertTrue(len(uniq_def_sites) == 2, "Interstitial init failed")
        #mgo_spg = Spacegroup(int_number=225)
        #self.assertTrue(mgo_spg.are_symmetrically_equivalent(uniq_sites,
        #                uniq_def_sites),  "Vacancy init failed")

    def test_defectsite_count(self):
        self.assertTrue(self._mgo_interstitial.defectsite_count() == 2, 
                "Vacancy count wrong")
        
    def test_get_defectsite_coordination_number(self):
        for i in range(self._mgo_interstitial.defectsite_count()):
            print >>sys.stderr, self._mgo_interstitial.get_defectsite_coordination_number(i)

    def test_get_coordsites_charge_sum(self):
        for i in range(self._mgo_interstitial.defectsite_count()):
            print >>sys.stderr, self._mgo_interstitial.get_coordsites_charge_sum(i)

    def test_get_defectsite_coordinated_elements(self):
        struct_el = self._mgo_uc.composition.elements
        for i in range(self._mgo_interstitial.defectsite_count()):
            for el in self._mgo_interstitial.get_coordinated_elements(i):
                self.assertTrue(
                        Element(el) in struct_el, "Coordinated elements are wrong"
                        )

    def test_get_radius(self):
        for i in range(self._mgo_interstitial.defectsite_count()):
            rad = self._mgo_interstitial.get_radius(i)
            print >> sys.stderr, rad
            self.assertTrue(rad, float)

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(InterstitialTest)
    #suite = unittest.TestLoader().loadTestsFromTestCase(VacancyTest)
    unittest.TextTestRunner(verbosity=3).run(suite)
