"""Assignment 3: Classes and objects

You will implement a set of classes that model a restaurant menu.

Feel free to add data, methods, and constructors to these classes as
needed, what I provide here is just a skeleton which also describes
the API you need to implement. As long as the API is implemented I
don't care if you add things to the classes to support the API. Just
make sure you actually need what you add.

NOTE: `raise NotImplementedError()` is a standard way to mark methods
that still need to be implemented. Remove it along with the TODOs when
you have implemented the methods. Do not remove the doc strings.

"""


class Menu(object):
    """A menu of available items and some associated information.

    This class must have 2 class attributes drink_tax and food_tax
    that are used for the tax amount on drink and food. The value
    should be 0.18 (18%) for drink, and 0.10 (10%) for food.

    """

    # Menu class attributes
    drink_tax = 0.18
    food_tax = 0.10

    def __init__(self):
        """Constructor for Menu class.

        Instantiate a new Menu object that starts with an initially empty
        dictionary that map items to price
        """
        self._items = {}

    def add_item(self, item):
        """Add an item to this menu and set it's menu attribute to this menu.

        Items should not be allowed to be added to more than one menu
        so check if the item is already in another menu.

        Return: True if the item was added, and False if it was not
        (because it had already been assigned a menu).
        """
        # Must first see if the item belongs to a menu already
        if not item.menu:
            # Update the item's menu
            item.menu = self
            # Update our menu's dictionary
            self._items[item] = item.price
            return True
        return False

    # TODO: Is this a good attribute to add if items can only be set once?
    def remove_item(self, item):
        """Remove an item from this menu and unset the item's menu attribute.

        Removing an item that does not exist in the menu should not cause
        any harm.

        Return: True if the item was removed, and False if it was not
        (because it did not exist on the menu)
        """
        # Check if the item is in the menu
        if item in self._items:
            # Unset the item's menu attribute
            item.menu = None
            # Delete the item from the list
            del self._items[item]
            return True
        return False

    @property
    def items(self):
        """Give forth the set of all items on this menu.

        READ-ONLY. The menu should not be modified from a result of calling
        this function.

        Return an immutable COPY of the set of items in the menu

        """
        return frozenset(self._items.keys())


class Order(object):
    """A list of items that will be purchased together.

    This provides properties that compute prices with tax and tip for
    the whole order.

    """

    def __init__(self):
        """Constructor for Order class.

        Instantiates a new Order object that starts with an initially empty
        list to hold items of a given order.

        Should be a list to allow duplicate items.

        """
        self._selections = []

    @property
    def selections(self):
        """Getter for the selections list for this order object."""
        return self._selections

    def add_item(self, item):
        """Add an item to this order.

        Items are required to all be part of one menu. You will need
        to check for this.

        Return True if the item was added, False otherwise (mainly if
        it was not part of the same menu as previous items).

        """
        # Check if the there are any elements in the menu or if the item to be
        # added's menu matches the other items' menu in the order
        if not self._selections or item.menu is self._selections[0].menu:
            # Add the item to the order
            self._selections.append(item)
            return True
        return False

    def remove_item(self, item):
        """Remove item from this order.

        Return True if the item was removed, False if otherwise (if the item
        was not present in the order).
        """
        # Iterate through the Order selections
        found_elem = next(elem for elem in self._selections if elem is item)
        # If the item was found, remove it
        if found_elem:
            self._selections.remove(item)
            return True
        return False

    def price_plus_tax(self):
        """A function that returns the sum of all the item prices
        including their tax.

        """
        final_price = 0.0
        # Generate the item prices and sum them together
        return sum(item.price_plus_tax() for item in self._selections)

    def price_plus_tax_and_tip(self, amount):
        """A method returns the sum of all the item prices with
        tax and a specified tip.

        amount is given as a proportion of the cost including tax.

        """
        # Add the tip to calculated amount
        return self.price_plus_tax() * (1 + amount)


class GroupOrder(Order):
    """An order than is made by a large ground and forces the tip to be at least
    20% (0.20).

    If a price with a tip less than 20% is requested return a price with a 20%
    tip instead.

    """

    def __init__(self):
        """Constructor for the GroupOrder class."""
        super().__init__()

    def price_plus_tax_and_tip(self, amount):
        """Override the price_plus_tax_and_tip() from super class.

        Do not duplicate any code from super.
        Force a tip of AT LEAST 20% (0.20).

        Return the final price with tax and tip computed already.

        """
        # Make sure the tip is at least 20%
        tip = max(amount, 0.20)
        # Super class has implementation to compute the final price
        return super().price_plus_tax_and_tip(tip)


class Item(object):
    """An item that can be bought.

    It has a name and a price attribute, and can compute its price with
    tax. This also has a menu property that stores the menu this has
    been added to.

    """

    def __init__(self, name, price):
        self._name = name
        self._price = price
        self._menu = None

    @property
    def price(self):
        """Getter that returns the price attribute of this item."""
        return self._price

    @property
    def menu(self):
        """Getter that returns the menu this item is a part of."""
        return self._menu

    @menu.setter
    def menu(self, menu_obj):
        """Setter that changes the item's menu property to menu_obj

        Should only be possible to set once

        """
        # This item must not belong to other menus
        if self._menu is None:
            self._menu = menu_obj

    def price_plus_tax(self):
        """Return the price of this item with tax added.

        Make sure you could support additional Item types, other than
        what you have in this file (meaning isinstance checks will not
        work). Imagine that I might have a Dessert class that derives
        from Item in another file.

        """
        return self._price + (self._price * self._applicable_tax())

    def _applicable_tax(self):
        """Return the amount of tax applicable to this item as a proportion
        (eg. 0.2 if the tax is 20%).

        """
        # This is an abstract method. It should not be implemented in
        # this class.
        raise NotImplementedError()


# DO NOT change the classes below. Your code in Item should work with
# these implementations or others in other files.

class Food(Item):
    """An Item subclass which uses the food tax rate."""
    def _applicable_tax(self):
        return self.menu.food_tax


class Drink(Item):
    """An Item subclass which uses the drink tax rate."""
    def _applicable_tax(self):
        return self.menu.drink_tax
