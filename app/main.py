import sys


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
        else:
            print(f"{cmd_raw}: command not found")


if __name__ == "__main__":
    main()
