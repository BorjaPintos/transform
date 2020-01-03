import sys


def main(file):
    with open(file, "rb") as f:
        print(f.read().hex())


if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        print("usage: " + sys.argv[0] + " <input>")
        sys.exit(1)

    main(sys.argv[1])
