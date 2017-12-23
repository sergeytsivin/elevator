import asyncio


class Elevator:
    def __init__(self, command_queue):
        self.command_queue = command_queue

    def on_call(self, floor):
        print("I'm called from floor {}".format(floor))

    def on_cabin_button(self, floor):
        print("Cabin button {} is pressed".format(floor))

    async def run(self):
        while True:
            command = await self.command_queue.get()
            command.handle(self)
