import unittest

from storemanager.locations.store import *

class TestSpecificWeaponStore(unittest.TestCase):

    def test_valid(self):
        """Initialize a specific weapons store, validate no errors."""
        store = SpecificWeaponStore("Special Weapons", 5, "Sword")

    def test_invalid_style(self):
        """Provide an invalid style, validate error thrown."""
        self.assertRaises(StoreError, SpecificWeaponStore, "Special Weapons", 5, "Swordfish")


if __name__ == '__main__':
    unittest.main()
