
import sys

from enum import Enum
class Symbol(Enum):
    DOT = '.'
    DASH = '-'


MORSE_CODE_DICT = {
    'A':[Symbol.DOT, Symbol.DASH], 
    'B':[Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DOT], 
    'C':[Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DOT],
    'D':[Symbol.DASH, Symbol.DOT, Symbol.DOT], 
    'E':[Symbol.DOT], 
    'F':[Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DOT],
    'G':[Symbol.DASH, Symbol.DASH, Symbol.DOT], 
    'H':[Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT], 
    'I':[Symbol.DOT, Symbol.DOT], 
    'J':[Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DASH], 
    'K':[Symbol.DASH, Symbol.DOT, Symbol.DASH], 
    'L':[Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DOT],
    'M':[Symbol.DASH, Symbol.DASH], 
    'N':[Symbol.DASH, Symbol.DOT], 
    'Ñ':[Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DASH],
    'O':[Symbol.DASH, Symbol.DASH, Symbol.DASH],
    'P':[Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DOT],
    'Q':[Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DASH], 
    'R':[Symbol.DOT, Symbol.DASH, Symbol.DOT], 
    'S':[Symbol.DOT, Symbol.DOT, Symbol.DOT],
    'T':[Symbol.DASH], 
    'U':[Symbol.DOT, Symbol.DOT, Symbol.DASH],
    'V':[Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DASH], 
    'W':[Symbol.DOT, Symbol.DASH, Symbol.DASH], 
    'X':[Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DASH], 
    'Y':[Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DASH], 
    'Z':[Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DOT],
    '0':[Symbol.DASH, Symbol.DASH, Symbol.DASH, Symbol.DASH, Symbol.DASH],  
    '1':[Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DASH, Symbol.DASH], 
    '2':[Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DASH],
    '3':[Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DASH], 
    '4':[Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DASH],
    '5':[Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT], 
    '6':[Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT], 
    '7':[Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DOT], 
    '8':[Symbol.DASH, Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DOT],
    '9':[Symbol.DASH, Symbol.DASH, Symbol.DASH, Symbol.DASH, Symbol.DOT], 
    ', ':[Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DASH],
    '.':[Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DASH], 
    '?':[Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DOT],
    '!':[Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DASH],
    '"':[Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DOT],
    '/':[Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DOT], 
    '-':[Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DASH], 
    '(':[Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DOT], 
    ')':[Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DASH]
} 

def main(arguments):

    format = arguments.get("outputformat")
    words = arguments.get("words")

    message = []
    for word in words:
        message.append(codify(word))

    dumps(format, message)


def codify(word):
    cod = []
    for letter in word: 
        lettercod = MORSE_CODE_DICT.get(letter.upper(), None)
        if lettercod is not None:
            cod.append(lettercod)
    return cod 

def dumps(format, message):
    if format == "A":
        dumpsAudio(message)
    elif format == "T":
        dumpsText(message)


def dumpsText(message):
    
    string = ''
    for word in message:
        for letter in word:
            for symbol in letter:
                string+=symbol.value
            string+=' '
        string+= '     '
    print(string)


def dumpsAudio(message):
    print("TODO")

def _getArguments(args):
    arguments = {}
    arguments["outputformat"] = args[0]
    words = []
    for word in args[1:]:
        words.append(word)
    arguments["words"] = words
    return arguments

if __name__ == "__main__":
    if len(sys.argv[1:]) < 2:
        print("usage: " + sys.argv[0] + " <outputformat> <word1> [word2 ...]" )
        print("outputformat:")
        print("T -> Text")
        print("A -> AudioFile" )
        sys.exit(1)

    main(_getArguments(sys.argv[1:]))

