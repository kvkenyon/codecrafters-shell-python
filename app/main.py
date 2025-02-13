import sys


def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")

    valid_cmds = []

    # Wait for user input
    cmd = input()

    if cmd not in valid_cmds:
        print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
