
import random

from storemanager import StoreMgrError


class StockItemError (StoreMgrError):
    pass


class _StockItem:

    """Abstract class: an item available for purchase from a store.

    Attributes:
      name     -- name/description of item
      desc     -- (optional) description of item
      value    -- fair market value of item
      markup   -- percentage used to calculate cost (100 == FMV)

      commission           -- boolean: does a commission exist for this item
      commission_rate      -- multiplier for commission (e.g. 0.60)
      commission_player    -- name of player owning commission
      commission_character -- name of character owning commission


    Printing options:
      str         -- normal string listing, with pricing information
      readable    -- long-hand listing, formatted with spaces for readability
      short       -- 30 characters or less, with minimum information
      description -- description of the item, with usage information

    Methods:
      reduce_markup  -- update for a new week
      price          -- return the current selling price
      set_commission -- establish a commission on this item
      get_commission -- return current commission details

    To implement, set name and value [and desc] before calling __init__.

    """

    commission = False           #: current commission on this item?
    commission_rate = 0          #: decimal percentage of sale price
    commission_player = None     #: name of the player selling the item
    commission_character = None  #: name of the character selling the item

    def __init__(self):
        """Determine the initial markup of the item."""
        self._setmarkup()

    def _setmarkup(self):
        """Set initial self.markup."""
        self.markup = random.randint(101, 120)

    def __lt__(self, other):
        """Sort by markup."""
        return self.markup < other.markup


    ## Print Formatting

    def __str__(self):
        return "%s (FMV $%s): $%s" % (self.name, self.value, self.price())

    def readable(self):
        """Return a longer, hopefully more readable listing."""
        return "%-50s FMV $%8s:  $%8s" % (self.name, self.value, self.price())

    def short(self):
        """Return a short version of the name, hopefully under 30 characters."""
        return self.name

    def description(self):
        """Return a long-hand description of the item."""
        if 'desc' in dir(self):
            return self.desc
        return self.readable()


    ## Default operation

    def reduce_markup(self):
        """Reduce self.markup by a random amount."""
        self.markup -= random.randint(1, 6)

    def price(self):
        """Return current selling price."""
        return round(self.value * self.markup / 100)

    def set_commission(self, player, character, rate=0.60):
        """Set a commission for the given player and character, at rate."""
        self.commission = True
        self.commission_player = player
        self.commission_character = character
        self.commission_rate = rate

    def get_commission(self):
        """Return (player, char, commission) if item sells today."""
        return (self.commission_player, self.commission_character, 
                int(self.price() * self.commission_rate))


class _MultiAbilityStockItem (_StockItem):

    """Extends _StockItem with better print methods for multi-ability items.

    Additional attributes:
      abilityname -- word to use for this type of ability, plural (default: "abilities")
      itemtype    -- name of the type of item containing this
      abilities   -- list of elvenfire.abilities._Ability subclass items

    To implement, set itemtype and abilities [and abilityname] during __init__.

    """

    abilityname = 'abilities'

    def short(self):
        """Return a short version of the name, hopefully under 30 characters."""
        if len(self.abilities) == 1:
            val = "%s of %s" % (self.itemtype, self.abilities[0])
        else:
            val = "%s of %s %s" % (self.itemtype, len(self.abilities),
                                   self.abilityname)
            minIIQ = 6
            maxIIQ = 0
            for ability in self.abilities:
                if 'IIQ' in dir(ability):
                    if ability.IIQ < minIIQ:
                        minIIQ = ability.IIQ
                    if ability.IIQ > maxIIQ:
                        maxIIQ = ability.IIQ
            if minIIQ < maxIIQ:
                val += " (IIQ %s to %s)" % (minIIQ, maxIIQ)
            elif minIIQ == maxIIQ:
                val += " (IIQ %s)" % minIIQ
        return val

    def description(self):
        """Return a concatenation of item abilities."""
        if 'desc' in dir(self):
            val = self.desc
            if len(self.abilities) <= 3:
                val += '\n\n'
                val += '\n\n'.join([a.description() for a in self.abilities])
            return val
        return self.readable()

    def readable(self):
        """Return a printer-friendly, detailed listing of the abilities."""
        val = "%-50s FMV $%8s:  $%8s" % (self.itemtype, self.value, self.price())
        for ability in self.abilities:
            val += "\n - %s" % ability
        return val


