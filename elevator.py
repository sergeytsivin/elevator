import asyncio
from datetime import datetime
from buttons import Buttons


def log(message):
    print("{}: {}".format(str(datetime.now()), message))


class State(object):
    async def run(self, elevator):
        raise NotImplemented


class Idle(State):
    async def run(self, elevator):
        log("Waiting on floor: {}. Turn lights OFF".format(elevator.current_floor))
        elevator.command.clear()
        await elevator.command.wait()
        log("Wake up. Turn lights ON")
        return State.active


class Active(State):
    async def open_doors(self, elevator):
        try:
            log("Opening doors")
            elevator.cabin_buttons.remove(elevator.current_floor)
            elevator.call_buttons.remove(elevator.current_floor)
            await asyncio.sleep(elevator.doors_delay)
        finally:
            log("Closing doors")

    async def moving_up(self, elevator, destination):
        log("Moving up")
        # While moving up, user can further clarify the destination by pressing cabin buttons
        # Call buttons are ignored because calling persons are likely to want to go down
        while elevator.current_floor < destination \
                or elevator.cabin_buttons.get_above(elevator.current_floor):
            await asyncio.sleep(elevator.time_to_next_floor)
            elevator.current_floor += 1
            log("Current floor is {}".format(elevator.current_floor))

            if elevator.current_floor == destination \
                    or elevator.current_floor in elevator.cabin_buttons:
                await self.open_doors(elevator)

    async def moving_down(self, elevator, destination):
        log("Moving down")
        # While moving down also stop on floors where call button is pressed
        while elevator.current_floor > destination \
                or elevator.cabin_buttons.get_below(elevator.current_floor):
            await asyncio.sleep(elevator.time_to_next_floor)
            elevator.current_floor -= 1
            log("Current floor is {}".format(elevator.current_floor))
            if elevator.current_floor == destination \
                    or elevator.current_floor in elevator.cabin_buttons \
                    or elevator.current_floor in elevator.call_buttons:
                await self.open_doors(elevator)

    async def run(self, elevator):
        while True:
            destination = None
            if elevator.cabin_buttons.pressed():
                # Check he cabin buttons first
                destination = elevator.cabin_buttons.get_closest(elevator.current_floor)
            elif elevator.call_buttons.pressed():
                destination = elevator.call_buttons.get_closest(elevator.current_floor)

            if destination is None:
                return State.idle

            if elevator.current_floor == destination:
                await self.open_doors(elevator)
                continue

            if destination > elevator.current_floor:
                await self.moving_up(elevator, destination)
            else:
                await self.moving_down(elevator, destination)


class DoorsOpen(State):
    async def run(self, elevator, *args, **kwargs):
        log("Opening doors")
        try:
            await asyncio.sleep(3)
        finally:
            log("Closing doors")
        return State.idle


State.idle = Idle()
State.active = Active()
State.doors_open = DoorsOpen()


class Elevator(object):
    def __init__(self, floors=12, height=2.65, velocity=3.0, doors_delay=3.0):
        self.floors = floors
        self.current_floor = 1
        self.time_to_next_floor = float(height) / velocity
        self.doors_delay = doors_delay
        self.current_state = State.idle
        self.cabin_buttons = Buttons()
        self.call_buttons = Buttons()
        self.command = asyncio.Event()

    def floor_is_valid(self, floor):
        return 1 <= floor <= self.floors

    def on_call_button(self, floor):
        if self.floor_is_valid(floor):
            log("Called from floor {}".format(floor))
            self.call_buttons.add(floor)
            self.command.set()
        else:
            log("Invalid floor: {}".format(floor))

    def on_cabin_button(self, floor):
        if self.floor_is_valid(floor):
            log("Cabin button {} pressed".format(floor))
            self.cabin_buttons.add(floor)
            self.command.set()
        else:
            log("Invalid floor: {}".format(floor))

    async def handle_commands(self, command_queue):
        while True:
            command = await command_queue.get()
            command.handle(self)

    async def run(self):
        log("Starting operations")
        try:
            while True:
                self.current_state = await self.current_state.run(self)
        except asyncio.CancelledError:
            log("Stopped operations")
            asyncio.get_event_loop().stop()
