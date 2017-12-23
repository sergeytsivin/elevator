import sys
import asyncio

from controller import Controller
from elevator import Elevator

port = 4455


def main():
    loop = asyncio.get_event_loop()
    controller = Controller('Elevator Controller', port, loop)
    print('Elevator controller server is listening on port {}'.format(port))

    elevator = Elevator(controller.get_command_queue())
    try:
        loop.run_until_complete(elevator.run())
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        loop.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
