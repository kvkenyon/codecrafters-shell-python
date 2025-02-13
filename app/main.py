import sys
import os

SHELL_BUILTIN = lambda x: f"{x} is a shell builtin"  # noqa

BUILTINS = set(["echo", "exit", "type"])

CMDS = set(["echo", "type", "exit"])

PATH = os.environ["PATH"]


def main():
    paths = PATH.split(":")
    while True:
        sys.stdout.write("$ ")
        cmd_raw = input()
        cmd = cmd_raw.split(" ")
        if not cmd:
            return f"{cmd_raw}: command not found"
        cmd_name, args = cmd[0], cmd[1:]
        if cmd_name == "exit":
            sys.exit(0)
        elif cmd_name == "echo":
            print(" ".join(args))
        elif cmd_name == "type":
            found = False
            for path in paths:
                subcmd = path + "/" + args[0]
                if os.path.exists(subcmd):
                    print(f"{args[0]} is {subcmd}")
                    found = True
                    break
            if found:
                continue

            if args[0] not in BUILTINS:
                print(f"{args[0]}: not found")
                continue
            print(SHELL_BUILTIN(args[0]))

        else:
            print(f"{cmd_raw}: command not found")


if __name__ == "__main__":
    main()
