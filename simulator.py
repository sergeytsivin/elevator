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
        help="height of the floor (meters)",
        type=float, default=2.65
    )
    parser.add_argument(
        "-v", "--velocity",
        help="velocity of the elevator cabin (meters per second)",
        type=float, default=3.0
    )
    parser.add_argument(
        "-d", "--doors_delay",
        help="time delay while cabin doors are open (seconds)",
        type=float, default=3.0
    )
    parser.add_argument(
        "-p", "--port",
        help="controller port",
        type=int, default=4455
    )
    args = parser.parse_args()

    print("Welcome to Elevator Simulator")
    print("Floors:\t\t{floors:>8}\nHeight:\t\t{height:>8}\nVelocity:\t{velocity:>8}\nDoors delay:{doors_delay:>8}"
          .format(**vars(args)))

    loop = asyncio.get_event_loop()
    controller = Controller('Elevator Controller', port=args.port, loop=loop)
    print("Elevator controller server is listening on port {}".format(args.port))

    elevator = Elevator(
        floors=args.floors,
        height=args.height,
        velocity=args.velocity,
        doors_delay=args.doors_delay
    )

    tasks = asyncio.gather(
        loop.create_task(elevator.handle_commands(controller.get_command_queue())),
        loop.create_task(elevator.run())
    )

    try:
        loop.run_until_complete(tasks)
    except KeyboardInterrupt:
        print("Shutdown requested")
        tasks.cancel()
        loop.run_forever()
    finally:
        loop.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
