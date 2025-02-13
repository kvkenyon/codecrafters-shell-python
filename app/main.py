import sys


def main():
    # Uncomment this block to pass the first stage

    valid_cmds = []

    while True:
        # Wait for user input
        sys.stdout.write("$ ")
        cmd = input()
        if cmd == "exit 0":
            sys.exit(0)
        if cmd not in valid_cmds:
            print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
