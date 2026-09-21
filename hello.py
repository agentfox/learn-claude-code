import sys


def greeting(name="World"):
    return f"Hello, {name}!"


def main(argv):
    name = argv[1] if len(argv) > 1 else "World"
    print(greeting(name))


if __name__ == "__main__":
    main(sys.argv)
