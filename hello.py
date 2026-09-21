import sys


def greeting(name="World"):
    return f"Hello, {name}!"


def main(argv):
    name = " ".join(argv[1:]) or "World"
    print(greeting(name))


if __name__ == "__main__":
    main(sys.argv)
