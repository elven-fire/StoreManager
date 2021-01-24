import unittest

from storemanager.locations.store import *

class TestSpecificWeaponStore(unittest.TestCase):

    def test_valid(self):
        """Initialize a specific weapons store, validate all items are of the correct style."""
        store = SpecificWeaponStore("Special Weapons", 5, "Sword")
        self.assertTrue(all([item.style == "Sword" for item in store.inventory]))

    def test_invalid_style(self):
        """Provide an invalid style, validate error thrown."""
        self.assertRaises(StoreError, SpecificWeaponStore, "Special Weapons", 5, "Swordfish")


if __name__ == '__main__':
    unittest.main()
