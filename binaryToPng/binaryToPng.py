from PIL import Image
import sys



def main(arguments):

    input = arguments.get("input")
    output = arguments.get("output", "image")
    sizeX = int(arguments.get("sizeX", 1800))
    sizeY = int(arguments.get("sizeY", 1600))

    img = _newImage(sizeX, sizeY)
    pix = img.load()

    with open(input, "rb") as f:
        byte = f.read(1)
        x = 0
        y = 0
        position = 0
        index=0
        while byte != b"":
            temp = list(pix[x,y])
            temp[position] = byte[0]
            pix[x,y] = tuple(temp)
            position+=1
            if position == 3:
                position=0
                x = x+1
            if x==sizeX:
                x=0
                y=y+1
            if y==sizeY:
                _save(img, output, index)
                index+=1
                img = _newImage(sizeX, sizeY)
                pix = img.load()
                x=0
                y=0
            byte = f.read(1)

        _save(img, output, index)
    
    
def _newImage(X,Y):
    img = Image.new('RGB', (X, Y))
    return img

def _save(img, path, index):
    name = path
    if index!=0:
        name+=str(index)
    name += ".png"
    img.save(name)

def _getArguments(args):
    properties = ['input', 'output', 'sizeX', 'sizeY']
    i = 0
    arguments = {}
    for arg in args:
        arguments[properties[i]] = arg
        i+=1
    return arguments

if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        print("usage: " + sys.argv[0] + " <input> [<ouput>] [sizeX] [sizeY]" )
        sys.exit(1)

    main(_getArguments(sys.argv[1:]))

