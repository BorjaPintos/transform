import sys


def main(arguments):

    input = arguments.get("inputStringHex")
    output = arguments.get("outputFile")

    if (len(input)) % 2 is not 0:
        raise Exception("invalid stringHexSize")

    with open(output, "wb") as f:
        binaryBytes = bytes.fromhex(input)
        f.write(binaryBytes)


def _getArguments(args):
    properties = ['inputStringHex', 'outputFile']
    i = 0
    arguments = {}
    for arg in args:
        arguments[properties[i]] = arg
        i+=1
    return arguments

if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        print("usage: " + sys.argv[0] + " <inputStringHex>" + " <outputFile>")
        sys.exit(1)

    main(_getArguments(sys.argv[1:]))
