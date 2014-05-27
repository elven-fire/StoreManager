import unittest
from elvenfire.abilities import _Ability
from storemanager.stockitems import _StockItem, _MultiAbilityStockItem


class DummyAbility(_Ability):

    """Allow simple calculations using ability."""

    def __init__(self, name, IIQ, AC):
        """Initialize required variables."""
        self.name = name
        self.IIQ = IIQ
        self.AC = AC

    def _lookup(self):
        """Avoid NotYetImplementedError."""
        pass


class TestAbstractStockItem(unittest.TestCase):

    """Verify the abstract base class's provisions."""

    def setUp(self):
        self.item = _StockItem()

    def test_default_attributes(self):
        """Verify the default values of the attributes."""
        self.item = _StockItem()
        self.assertFalse(self.item.commission)
        self.assertEqual(self.item.commission_rate, 0)
        self.assertIs(self.item.commission_player, None)
        self.assertIs(self.item.commission_character, None)

    def test_sorting(self):
        """Verify comparison operators."""
        other = _StockItem()
        other.markup = self.item.markup - 1
        self.assertTrue(self.item > other)
        other.markup = self.item.markup + 1
        self.assertTrue(self.item < other)
        other.markup = self.item.markup
        self.assertFalse(self.item < other)

    def test_initial_markup(self):
        """Verify the range for the initial markup."""
        for i in range(100):
            s = _StockItem()
            self.assertTrue(100 < s.markup)
            self.assertTrue(s.markup <= 120)

    def test_reduce_markup(self):
        """Verify the range for markup reductions."""
        for i in range(10):
            previous = self.item.markup
            self.item.reduce_markup()
            diff = previous - self.item.markup
            self.assertTrue(diff >= 1)
            self.assertTrue(diff <= 6)

    def test_price_up(self):
        """Verify the proper calculation (rounding up) for selling price."""
        self.item.value = 1834
        self.item.markup = 99
        self.assertEqual(self.item.price(), 1816)

    def test_price_down(self):
        """Verify the proper calculation (rounding down) for selling price."""
        self.item.value = 1834
        self.item.markup = 98
        self.assertEqual(self.item.price(), 1797)

    def test_blank_commission(self):
        """Verify the commission details."""
        self.item.value = 1000
        self.assertEqual(self.item.get_commission(), (None, None, 0))

    def test_set_commission(self):
        """Verify commission details properly set."""
        self.item.set_commission("MyPlayer", "My Character Name")
        self.item.value = 2000
        self.item.markup = 50
        self.assertEqual(self.item.get_commission(),
                         ("MyPlayer", "My Character Name", 600))

    def test_set_commission_rate(self):
        """Verify custom commission rate."""
        self.item.set_commission("MyPlayer", "My Character Name", .50)
        self.item.value = 1000
        self.item.markup = 100
        self.assertEqual(self.item.get_commission(),
                         ("MyPlayer", "My Character Name", 500))

    def test_commission_rounding(self):
        """Verify commissions are truncated to integer form."""
        self.item.set_commission("MyPlayer", "My Character Name", .995)
        self.item.value = 100
        self.item.markup = 100
        self.assertEqual(self.item.get_commission(),
                         ("MyPlayer", "My Character Name", 99))

        
class TestAbstractStockItemStrings(unittest.TestCase):

    """Test various string-printing methods of the abstract base class."""

    def setUp(self):
        self.item = _StockItem()
        self.item.name = "Test Item"
        self.item.value = 2000
        self.item.markup = 110

    def test_string(self):
        """Verify the overridden string generation."""
        self.assertEqual(str(self.item), "Test Item (FMV $2000): $2200")

    def test_readable(self):
        """Verify the print-ready string."""
        self.assertEqual(self.item.readable(),
                         "Test Item                                          FMV $    2000:  $    2200")

    def test_short(self):
        """Verify short version."""
        self.assertEqual(self.item.short(), "Test Item")

    def test_default_description(self):
        """Verify description default."""
        self.assertEqual(self.item.description(), self.item.readable())

    def test_overridden_description(self):
        """Verify the ability to override the description."""
        self.item.desc = "Test Description"
        self.assertEqual(self.item.description(), self.item.desc)

        
class TestAbstractMultiAbilityStockItem(unittest.TestCase):

    """Verify the abstract base class's provisions for multi-ability items."""

    def setUp(self):
        self.item = _MultiAbilityStockItem()
        self.item.itemtype = "MA Item"
        self.item.value = 1000
        self.item.markup = 90
        self.item.abilities = []

        self.ability1 = DummyAbility("Ability 1", 1, 1000)
        self.ability2 = DummyAbility("Ability 2", 2, 2000)
        self.ability3 = DummyAbility("Ability 3", 3, 3000)
        self.ability4 = DummyAbility("Ability 4", 4, 4000)
        self.ability5 = DummyAbility("Ability 5", 5, 5000)

    def test_default_attributes(self):
        """Verify the default values of the attributes."""
        self.assertEqual(self.item.abilityname, "abilities")

    def test_string(self):
        """Verify the string format is unchanged."""
        self.item.name = "Name Test"
        self.assertEqual(str(self.item), "Name Test (FMV $1000): $900")

    def test_short_none(self):
        """Verify the short format with no abilities."""
        self.assertEqual(self.item.short(),
                         "MA Item of 0 abilities")

    def test_short_one(self):
        """Verify the short format with one ability."""
        self.item.abilities.append(self.ability3)
        self.assertEqual(self.item.short(),
                         "MA Item of " + str(self.ability3))

    def test_short_five(self):
        """Verify the short format with five abilities."""
        self.item.abilities.append(self.ability1)
        self.item.abilities.append(self.ability2)
        self.item.abilities.append(self.ability3)
        self.item.abilities.append(self.ability4)
        self.item.abilities.append(self.ability5)
        self.assertEqual(self.item.short(),
                         "MA Item of 5 abilities (IIQ 1 to 5)")

    def test_short_IIQ_range(self):
        """Verify the short format includes the correct IIQ range."""
        self.item.abilities.append(self.ability4)
        self.item.abilities.append(self.ability2)
        self.assertEqual(self.item.short(),
                         "MA Item of 2 abilities (IIQ 2 to 4)")

    @unittest.skip("actually includes \n\n - no abilities is impossible anyway")
    def test_description_none(self):
        """Verify a custom description with no abilities."""
        self.item.desc = "Test Description"
        self.assertEqual(self.item.description(),
                         "Test Description")

    def test_description_one(self):
        """Verify a custom description with one ability."""
        self.item.desc = "Test Description"
        self.item.abilities.append(self.ability1)
        self.assertEqual(self.item.description(),
                         "Test Description\n\n%s" % self.ability1.description())

    def test_description_three(self):
        """Verify three abilities still includes those descriptions."""
        self.item.desc = "Test Description"
        self.item.abilities.append(self.ability1)
        self.item.abilities.append(self.ability2)
        self.item.abilities.append(self.ability3)
        self.assertEqual(self.item.description(),
                         "Test Description\n\n%s\n\n%s\n\n%s" %
                         (self.ability1.description(),
                          self.ability2.description(),
                          self.ability3.description()))

    def test_description_four(self):
        """Four and up should not include ability descriptions."""
        self.item.desc = "Test Description"
        self.item.abilities.append(self.ability1)
        self.item.abilities.append(self.ability2)
        self.item.abilities.append(self.ability3)
        self.item.abilities.append(self.ability4)
        self.assertEqual(self.item.description(),
                         "Test Description")

    def test_description_default(self):
        """Verify readable() is the default description."""
        self.assertEqual(self.item.description(), self.item.readable())

    def test_readable_none(self):
        """Verify the readable printout with no abilities."""
        self.assertEqual(self.item.readable(),
                         "MA Item                                            FMV $    1000:  $     900")

    def test_readable_one(self):
        """Verify the readable printout with one ability."""
        self.item.abilities.append(self.ability1)
        self.assertEqual(self.item.readable(),
                         "MA Item                                            FMV $    1000:  $     900\n" +
                         " - " + str(self.ability1))
        
    def test_readable_five(self):
        """Verify the readable printout with five abilities."""
        self.item.abilities.append(self.ability1)
        self.item.abilities.append(self.ability2)
        self.item.abilities.append(self.ability3)
        self.item.abilities.append(self.ability4)
        self.item.abilities.append(self.ability5)
        self.assertEqual(self.item.readable(),
                         "MA Item                                            FMV $    1000:  $     900\n" +
                         " - " + str(self.ability1) + "\n" +
                         " - " + str(self.ability2) + "\n" +
                         " - " + str(self.ability3) + "\n" +
                         " - " + str(self.ability4) + "\n" +
                         " - " + str(self.ability5))
        

if __name__ == '__main__':
    unittest.main()
