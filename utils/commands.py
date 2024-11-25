commands = {
    # "command name": ("arg1 arg2 arg3")
    "process": ()
}


def matchCommand(commandStr, output):
    if not commandStr:
        output("Empty command", error=True)
        return False

    splitCmd = commandStr.split(' ')

    if splitCmd[0] not in commands:
        output(f"Unknown command '{splitCmd[0]}'", error=True)
        return False

    # No arguments
    if not commands[splitCmd[0]]:
        return True

    if splitCmd.len() - 1 < commands[splitCmd[0]][0].split(' ').len():
        output("Invalid number of arguments", error=True)
        return False
