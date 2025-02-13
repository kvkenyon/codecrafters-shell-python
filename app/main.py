import sys
import os
import subprocess

SHELL_BUILTIN = lambda x: f"{x} is a shell builtin"  # noqa

BUILTINS = set(["echo", "exit", "type"])

CMDS = set(["echo", "type", "exit"])

PATH = os.environ["PATH"]
PATHS = PATH.split(":")


def find_exec_in_path(cmd: str):
    for path in PATHS:
        subcmd = f"{path}/{cmd}"
        if os.path.exists(subcmd):
            return subcmd
    return None


def main():
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
            if args[0] in BUILTINS:
                print(SHELL_BUILTIN(args[0]))
            elif c := find_exec_in_path(args[0]):
                print(f"{args[0]} is {c}")
            else:
                print(f"{args[0]}: not found")
        else:
            if find_exec_in_path(cmd_name):
                res = subprocess.run(cmd, capture_output=True, text=True)
                print(res.stdout)
            else:
                print(f"{cmd_raw}: command not found")


if __name__ == "__main__":
    main()
