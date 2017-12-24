

class Command(object):
    def handle(self, elevator):
        raise NotImplemented


class CallCommand(Command):
    def __init__(self, floor):
        self.floor = floor

    def handle(self, elevator):
        elevator.on_call_button(self.floor)


class GoCommand(Command):
    def __init__(self, floor):
        self.floor = floor

    def handle(self, elevator):
        elevator.on_cabin_button(self.floor)

