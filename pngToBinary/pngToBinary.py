from PIL import Image
import sys



def main(arguments):


    output = arguments.get("output", "binary")
    parts = arguments.get("parts")

    
    with open(output, "wb+") as f:
        byteArray = []
        for part in parts:
            byteArray.extend(_readImage(part))

        byteArray = _cleanEndNulls(byteArray)
        for intByte in byteArray:
            f.write(bytes([intByte]))   



def _cleanEndNulls(byteArray):
    totalIndex = len(byteArray)-1
    for i in range(totalIndex,0, -1):
        if byteArray[i] == 0:
            del byteArray[i]
        else:
            break
    return byteArray

def _readImage(name):
    byteArray = []
    x=0
    y=0
    position = 0

    img = Image.open(name)
    pix = img.load()
    sizeX = img.size[0]
    sizeY = img.size[1]
    while True:
        intByte = pix[x,y][position]
        byteArray.append(intByte)
        position+=1
        if position == 3:
            position=0
            x = x+1
        if x==sizeX:
            x=0
            y=y+1
        if y==sizeY:
            return byteArray



def _getArguments(args):
    arguments = {}
    arguments["output"] = args[0]
    parts = []
    for part in args[1:]:
        parts.append(part)
    arguments["parts"] = parts
    return arguments

if __name__ == "__main__":
    if len(sys.argv[1:]) < 2:
        print("usage: " + sys.argv[0] + "<output> <part1> [<part2> ...]" )
        sys.exit(1)

    main(_getArguments(sys.argv[1:]))

