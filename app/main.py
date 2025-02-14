import sys
import os
import subprocess
from typing import NamedTuple


class Command(NamedTuple):
    name: str
    args: list[str]
    parsed: list[str]


SHELL_BUILTIN = lambda x: f"{x} is a shell builtin"  # noqa

BUILTINS = set(["echo", "exit", "type", "pwd", "cd"])


PATH = os.environ["PATH"]
PATHS = PATH.split(":")


def find_exec_in_path(cmd: str):
    for path in PATHS:
        subcmd = f"{path}/{cmd}"
        if os.path.exists(subcmd):
            return subcmd
    return None


def pwd():
    print(os.getcwd())


def echo(*args):
    print(f"{" ".join(args)}")


def exit():
    sys.exit(0)


def cd(path: str) -> None:
    if path == "~":
        path = os.path.expanduser(path)
    if os.path.exists(path):
        os.chdir(path)
        return
    print(f"cd: {path}: No such file or directory")


def parser(cmd: str):
    import re

    identifier = r"[\w/~\.-]+"
    string = r"'[/\w\s~\.-\\\"]+'"
    dquote = r'"([/\w\s~.\'-]+|(\\.)|(\\))+"'
    dash_arg = r"-[A-Za-z0-9]+"
    dash_dash_arg = r"--[A-Za-z0-9]+"
    space = r"[ \t]+"
    escape = r"\\."
    regex_spec = [
        ("CMD", identifier),
        ("SQUOTE", string),
        ("DQUOTE", dquote),
        ("DASHARG", dash_arg),
        ("ESCAPE", escape),
        ("DDARG", dash_dash_arg),
        ("SPACE", space),
    ]
    parser = "|".join("(?P<%s>%s)" % pair for pair in regex_spec)
    name = ""
    args = []
    parsed = []
    for mo in re.finditer(parser, cmd):
        kind = mo.lastgroup
        value = mo.group()
        # print(mo.groupdict())
        if kind == "CMD" and not name:
            name = value
            parsed.append(name)
        elif kind == "DQUOTE":
            content = value[1:-1]
            processed = re.sub(r'\\(["$\\])', r"\1", content)
            args.append(processed)
            parsed.append(processed)

        elif kind == "SQUOTE":
            args.append(value[1:-1])
            parsed.append(value[1:-1])
        elif kind == "SPACE":
            parsed.append(" ")
        elif kind == "ESCAPE":
            parsed.append(value[-1])
        else:
            args.append(value)
            parsed.append(value)
    return Command(name, args, parsed)


def main():
    while True:
        sys.stdout.write("$ ")
        cmd_raw = input()
        cmd = parser(cmd_raw)
        if not cmd:
            return f"{cmd_raw}: command not found"
        cmd_name, args, parsed = cmd.name, cmd.args, cmd.parsed
        if cmd_name == "exit":
            sys.exit(0)
        elif cmd_name == "echo":
            print("".join(parsed[1:]).strip())
        elif cmd_name == "pwd":
            pwd()
        elif cmd_name == "cd":
            cd(args[0])
        elif cmd_name == "type":
            if args[0] in BUILTINS:
                print(SHELL_BUILTIN(args[0]))
            elif c := find_exec_in_path(args[0]):
                print(f"{args[0]} is {c}")
            else:
                print(f"{args[0]}: not found")
        else:
            if find_exec_in_path(cmd_name):
                subprocess.run([cmd_name, *args])
            else:
                print(f"{cmd_raw}: command not found")


if __name__ == "__main__":
    main()
