class Buttons(object):
    """
    Simulate elevator buttons: both in the cabin and on the floor

    Keeps track which buttons has been pressed (added to the set).
    Button stays pressed until explicitly removed from the set.
    """
    def __init__(self):
        self.buttons = set()

    def get_closest(self, floor):
        """ Get the button that is closest to the specified floor """
        if self.buttons:
            return min(self.buttons, key=lambda x: abs(x - floor))
        else:
            return None

    def get_above(self, floor):
        """ Get buttons that are above the specified floor """
        return [button for button in self.buttons if button > floor]

    def get_below(self, floor):
        """ Get buttons that are below the specified floor """
        return [button for button in self.buttons if button < floor]

    def pressed(self):
        return bool(self.buttons)

    def __contains__(self, item):
        return self.buttons.__contains__(item)

    def reset(self):
        self.buttons.clear()

    def add(self, floor):
        self.buttons.add(floor)

    def remove(self, floor):
        if floor in self.buttons:
            self.buttons.remove(floor)
