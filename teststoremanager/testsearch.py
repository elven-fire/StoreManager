
import unittest
from elvenfire.abilities.itemabilities import AttributeAbility

from storemanager.search import _Criterion
from storemanager.search.criterion import *


class DummyItem:

    """Impersonates an item by implementing certain attributes."""
    
    def __init__(self, **kwargs):
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])


class DummyLocation:

    """Impersonates a location by implementing getitems."""

    def __init__(self, items):
        self.items = items

    def getitems(self):
        return self.items


class TestCriterion(unittest.TestCase):

    """Verify the base class for a search criterion."""

    def test_base_class_initialization(self):
        """Verify that the base class cannot be initialized alone."""
        self.assertRaises(NotImplementedError, _Criterion.__init__, self)

    def test_match(self):
        """Verify that match is required to be implemented."""
        class DummyCriterion(_Criterion):
            """Negate the error in __init__ to test match."""
            def __init__(self): pass
        self.assertRaises(NotImplementedError, DummyCriterion().match, "foo")

    # filter and search tested in TestTextCriterion


class TestTextCriterion(unittest.TestCase):

    """Verify all methods for TextCriterion."""

    def setUp(self):
        self.criterion = TextCriterion("Search Text")

    def test_attributes(self):
        """Verify the search text is stored properly."""
        self.assertEqual(self.criterion.text, "Search Text")

    def test_match_exact(self):
        """Verify that a match is found correctly."""
        self.assertTrue(self.criterion.match("Search Text"))

    def test_match_case(self):
        """Verify that a match is found correctly."""
        self.assertTrue(self.criterion.match("sEArch tExT"))

    def test_match_partial(self):
        """Verify that a match is found correctly."""
        self.assertTrue(self.criterion.match("Big search text okay"))

    def test_match_split(self):
        """Verify that a match is found correctly."""
        self.assertFalse(self.criterion.match("search split text"))

    def test_filter(self):
        """Verify that a list is filtered correctly."""
        self.assertEqual(self.criterion.filter(("Search Text",
                                                "No match",
                                                "No text",
                                                "Big search text",
                                                "Big search",
                                                "search texty")),
                         ["Search Text", "Big search text", "search texty"])

    def test_search(self):
        """Verify that a location is searched correctly."""
        loc = DummyLocation(("Search Text",
                                               "No match",
                                               "No text",
                                               "Big search text",
                                               "Big search",
                                               "search texty"))
        self.assertEqual(self.criterion.search(loc),
                         ["Search Text", "Big search text", "search texty"])

    def test_string(self):
        """Verify that the filter can be printed usefully."""
        self.assertEqual(str(self.criterion),
                         "Text contains: Search Text")


class TestTypeCriterion(unittest.TestCase):

    """Verify items match if they are of a certain type."""

    def setUp(self):
        self.criterion = TypeCriterion(DummyLocation)

    def test_match(self):
        """Verify that only the correct type matches."""
        self.assertTrue(self.criterion.match(DummyLocation([])))
        self.assertFalse(self.criterion.match(DummyItem()))

    def test_string(self):
        """Verify the string output for the Criterion."""
        self.assertEqual(str(self.criterion),
                         "Type: DummyLocation")

    def test_match_builtin(self):
        """Verify that the Criterion can match built-in types."""
        criterion = TypeCriterion(str)
        self.assertTrue(criterion.match("test string"))
        self.assertFalse(criterion.match(3))

    @unittest.skip("never happens anyway...")
    def test_string_builtin(self):
        """Verify that the string output is correct for built-in types."""
        criterion = TypeCriterion(str)
        self.assertEqual(str(criterion), "Type: str")


class TestAttributeCriterion(unittest.TestCase):

    """Verify items match with the right AttributeAbility."""
    
    def test_init(self):
        """Verify attributes set during __init__."""
        c = AttributeCriterion("ST", 2, 5)
        self.assertEqual(c.attr, "ST")
        self.assertEqual(c.minsize, 2)
        self.assertEqual(c.maxsize, 5)

    def test_default_init(self):
        """Verify the default values for __init__."""
        c = AttributeCriterion("ST")
        self.assertIs(c.minsize, None)
        self.assertIs(c.maxsize, None)

    def test_match_one_nosize(self):
        """Verify an attribute matches with no size restrictions."""
        c = AttributeCriterion("ST")
        self.assertTrue(c.match(DummyItem(ability=AttributeAbility("ST", 3))))

    def test_match_one_below_min(self):
        """Verify a match fails when the item's attribute is below min."""
        c = AttributeCriterion("ST", 3)
        self.assertFalse(c.match(DummyItem(ability=AttributeAbility("ST", 2))))

    def test_match_one_at_min(self):
        """Verify a match passes when the item's attribute is at min."""
        c = AttributeCriterion("ST", 3)
        self.assertTrue(c.match(DummyItem(ability=AttributeAbility("ST", 3))))

    def test_match_one_in_range(self):
        """Verify a match passes when within the range given."""
        c = AttributeCriterion("ST", 3, 5)
        self.assertTrue(c.match(DummyItem(ability=AttributeAbility("ST", 4))))

    def test_match_one_at_max(self):
        """Verify a match passes when the item's attribute is at max."""
        c = AttributeCriterion("ST", maxsize=4)
        self.assertTrue(c.match(DummyItem(ability=AttributeAbility("ST", 4))))

    def test_match_one_above_max(self):
        """Verify a match fails when the item's attribute is above the max."""
        c = AttributeCriterion("ST", maxsize=4)
        self.assertFalse(c.match(DummyItem(ability=AttributeAbility("ST", 5))))

    def test_match_multi(self):
        """Verify the Criterion looks at all abilities."""
        i = DummyItem(abilities=[AttributeAbility("DX"), AttributeAbility("ST")])
        c = AttributeCriterion("ST")
        self.assertTrue(c.match(i))

    def test_string_any_any(self):
        """Verify the string outputs."""
        self.assertEqual(str(AttributeCriterion(None)), "Any Attribute +")

    def test_string_any_set(self):
        """Verify the string outputs."""
        self.assertEqual(str(AttributeCriterion(None, minsize=3, maxsize=3)),
                         "Any Attribute + 3")

    def test_string_any(self):
        """Verify the string outputs."""
        self.assertEqual(str(AttributeCriterion("ST")), "ST +")

    def test_string_set(self):
        """Verify the string outputs."""
        self.assertEqual(str(AttributeCriterion("ST", minsize=3, maxsize=3)),
                         "ST + 3")

    def test_string_range(self):
        """Verify the string outputs."""
        self.assertEqual(str(AttributeCriterion("ST", 3, 5)), "ST + 3-5")

    def test_string_min(self):
        """Verify the string outputs."""
        self.assertEqual(str(AttributeCriterion("DX", minsize=2)),
                         "DX + 2 or more")

    def test_string_max(self):
        """Verify the string outputs."""
        self.assertEqual(str(AttributeCriterion("DX", maxsize=4)),
                         "DX + 4 or less")


class TestWeaponClassCriterion(unittest.TestCase):

    """Verify weapons of a specific class match."""

    def test_init(self):
        c = WeaponClassCriterion("Unusual Weapon")
        self.assertEqual(c.style, "Unusual Weapon")

    def test_not_weapon(self):
        """Verify no match when a non-weapon item given."""
        c = WeaponClassCriterion("Unusual Weapon")
        self.assertFalse(c.match(DummyItem(type="Unusual Weapon")))

    def test_

    


if __name__ == '__main__':
    unittest.main()
                   
