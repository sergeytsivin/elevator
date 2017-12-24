import sys
import asyncio
import argparse

from controller import Controller
from elevator import Elevator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--floors",
        help="number of floors in the building",
        type=int, choices=range(5, 21), default=12
    )
    parser.add_argument(
        "-H", "--height",
        help="height of the floor in meters",
        type=float, default=2.65
    )
    parser.add_argument(
        "-v", "--velocity",
        help="velocity of the elevator cabin in meters per second",
        type=float, default=3.0
    )
    parser.add_argument(
        "-p", "--port",
        help="controller port",
        type=int, default=4455
    )
    args = parser.parse_args()

    print("Welcome to Elevator Simulator")
    print("Floors:\t\t{}\nHeight:\t\t{}\nVelocity:\t{}".format(args.floors, args.height, args.velocity))

    loop = asyncio.get_event_loop()
    controller = Controller('Elevator Controller', port=args.port, loop=loop)
    print("Elevator controller server is listening on port {}".format(args.port))

    elevator = Elevator(
        command_queue=controller.get_command_queue(),
        floors=args.floors,
        height=args.height,
        velocity=args.velocity
    )
    try:
        loop.run_until_complete(elevator.run())
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        loop.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
