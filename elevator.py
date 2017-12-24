import asyncio
from datetime import datetime


def log(message):
    print("{}: {}".format(str(datetime.now()), message))


class State(object):
    async def run(self, *args, **kwargs):
        raise NotImplemented


class Idle(State):
    async def run(self, elevator,  *args, **kwargs):
        log("Waiting on floor: {}".format(elevator.current_floor))
        command = await elevator.command_queue.get()
        command.handle(elevator)
        return State.moving, command.floor


class Moving(State):        
    async def run(self, elevator, *args, **kwargs):
        destination = kwargs.get('destination')

        if destination is None:
            return State.idle, None

        if elevator.current_floor == destination:
            return State.doors_open, destination

        moving_up = destination > elevator.current_floor
        log("Moving {} to floor {}".format('up' if moving_up else 'down', destination))
        while elevator.current_floor != destination:
            await asyncio.sleep(elevator.time_to_next_floor)
            elevator.current_floor += 1 if moving_up else -1
            log("Current floor is {}".format(elevator.current_floor))

        return State.doors_open, None


class DoorsOpen(State):
    async def run(self, elevator, *args, **kwargs):
        log("Opening doors")
        try:
            command = await asyncio.wait_for(elevator.command_queue.get(), timeout=3)
            command.handle(elevator)
            next_state, destination = State.moving, command.floor
        except asyncio.TimeoutError:
            next_state, destination = State.idle, None
        finally:
            log("Closing doors")
        return next_state, destination


State.idle = Idle()
State.moving = Moving()
State.doors_open = DoorsOpen()


class Elevator:
    def __init__(self, command_queue, floors=12, height=2.65, velocity=3.0):
        self.command_queue = command_queue
        self.floors = floors
        self.current_floor = 1
        self.time_to_next_floor = float(height) / velocity
        self.current_state = State.idle

    def floor_is_valid(self, floor):
        return 1 <= floor <= self.floors

    def on_call(self, floor):
        if self.floor_is_valid(floor):
            log("Called from floor {}".format(floor))

    def on_cabin_button(self, floor):
        if self.floor_is_valid(floor):
            log("Cabin button {} pressed".format(floor))

    async def run(self):
        log("Starting operations")
        destination = None
        while True:
            self.current_state, destination = await self.current_state.run(self, destination=destination)
