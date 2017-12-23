import asyncio


class Controller(object):
    def __init__(self, server_name, port, loop):
        self.server_name = server_name
        self.loop = loop
        self.server = loop.run_until_complete(asyncio.start_server(self.accept_connection, "", port, loop=loop))

    async def get_command(self, reader, writer):
        while True:
            writer.write("Enter a command ('help' for help): ".encode())
            data = (await reader.readline()).decode()
            if not data:
                return None
            return data.strip()

    async def accept_connection(self, reader, writer):
        writer.write("Welcome to {}\n".format(self.server_name).encode())
        while True:
            command = await self.get_command(reader, writer)
            if command:
                command, *args = command.split()
            if command is None:
                break
            elif command == "quit":
                writer.write("See you later!\n".encode())
                break
            elif command == "help":
                self.help(writer)
            elif command == "call":
                self.call(writer, *args)
            elif command == "go":
                self.go(writer, *args)
            else:
                writer.write("Command '{}' is not known\n".format(command).encode())
        await writer.drain()
        writer.close()

    def help(self, writer):
        writer.write((
            "Commands are:\n"
            "\thelp\t\tprints this help message\n"
            "\tquit\t\tdisconnects from the server\n"
            "\tcall <n>\tsimulates pressing the call button on the n-th floor\n"
            "\tgo <n>\t\tsimulates pressing the n-th floor button in the cabin\n"
        ).encode())

    def call(self, writer, *args):
        try:
            floor = int(args[0])
            writer.write("Calling elevator to floor {}\n".format(floor).encode())
        except (ValueError, IndexError):
            writer.write("Error: invalid or missing arguments: {}\n".format(','.join(args)).encode())

    def go(self, writer, *args):
        try:
            floor = int(args[0])
            writer.write("Cabin button {} is pressed\n".format(floor).encode())
        except (ValueError, IndexError):
            writer.write("Error: invalid or missing arguments: {}\n".format(','.join(args)).encode())
