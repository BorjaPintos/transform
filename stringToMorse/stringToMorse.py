import numpy as np
import scipy.io.wavfile as waves
import sys

"""http://blog.espol.edu.ec/estg1003/morse-generador-de-tonos/"""

from enum import Enum

"""Duraciones en unidad universal, todo es en base a la duracion del DOT"""
DOTDURATION = 1 
DASHDURATION = DOTDURATION*3
SYMBOLSPACEDURATION = DOTDURATION
LETTERSPACEDURATION = DOTDURATION*3
WORDSSPACEDURATION = DOTDURATION*7
FS = 440
MUESTREO = 11025
DOTDURATIONSEC = 0.1

class Symbol(Enum):
    DOT = '.'
    DASH = '-'

    def getDuration(self):
        if self == Symbol.DOT:
            return DOTDURATION
        elif self == Symbol.DASH:
            return DASHDURATION


START_SIGNAL = [Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DASH]
ERROR = [Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT,]




MORSE_CODE_DICT = {
    'A':[Symbol.DOT, Symbol.DASH], 
    'Á':[Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DASH],
    'B':[Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DOT], 
    'C':[Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DOT],
    'D':[Symbol.DASH, Symbol.DOT, Symbol.DOT], 
    'E':[Symbol.DOT], 
    'É':[Symbol.DOT,Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DOT],
    'F':[Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DOT],
    'G':[Symbol.DASH, Symbol.DASH, Symbol.DOT], 
    'H':[Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT], 
    'I':[Symbol.DOT, Symbol.DOT], 
    'Í':[Symbol.DOT, Symbol.DOT], """no encontre como se pone la i con tilde"""
    'J':[Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DASH], 
    'K':[Symbol.DASH, Symbol.DOT, Symbol.DASH], 
    'L':[Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DOT],
    'M':[Symbol.DASH, Symbol.DASH], 
    'N':[Symbol.DASH, Symbol.DOT], 
    'Ñ':[Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DASH],
    'O':[Symbol.DASH, Symbol.DASH, Symbol.DASH],
    'Ó':[Symbol.DASH, Symbol.DASH, Symbol.DASH, Symbol.DOT],
    'P':[Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DOT],
    'Q':[Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DASH], 
    'R':[Symbol.DOT, Symbol.DASH, Symbol.DOT], 
    'S':[Symbol.DOT, Symbol.DOT, Symbol.DOT],
    'T':[Symbol.DASH], 
    'U':[Symbol.DOT, Symbol.DOT, Symbol.DASH],
    'Ú':[Symbol.DOT, Symbol.DOT, Symbol.DASH,Symbol.DASH],
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
    '@':[Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DOT],
    ',':[Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DASH],
    '.':[Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DASH],
    ':':[Symbol.DASH, Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DOT],
    ';':[Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DOT],
    '?':[Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DOT],
    '!':[Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DASH],
    '"':[Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DOT],
    "'":[Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DASH, Symbol.DASH, Symbol.DOT],
    '/':[Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DOT], 
    '-':[Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DASH],
    '+':[Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DOT],
    '*':[Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DASH],
    '=':[Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DASH], 
    '_':[Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DASH],
    '(':[Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DOT], 
    ')':[Symbol.DASH, Symbol.DOT, Symbol.DASH, Symbol.DASH, Symbol.DOT, Symbol.DASH],
    '$':[Symbol.DOT, Symbol.DOT, Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DASH],
    '&':[Symbol.DOT, Symbol.DASH, Symbol.DOT, Symbol.DOT, Symbol.DOT]
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
        string+= '       '
    print(string)

def dumpsAudio(message):
    tono = np.zeros(0, dtype='int16')
    for word in message:
        for letter in word:
            for symbol in letter:
                tono = np.hstack([tono,pitido(symbol.getDuration())])
                tono = np.hstack([tono,silence(SYMBOLSPACEDURATION)])
            tono = np.hstack([tono,silence(LETTERSPACEDURATION)])
        tono = np.hstack([tono,silence(WORDSSPACEDURATION)])
    waves.write('output.wav', MUESTREO, tono)

def pitido(duracion):
    durationsec = DOTDURATIONSEC*duracion
    dt = 1/MUESTREO
    t = np.arange(0,durationsec,dt)
    tono = np.zeros(len(t), dtype='int16') #tono vacio
    volumen = 0.8      # rango [0,1)
    amplitud = int((2**15)*volumen)  #wav 16 bits
    w = 2*np.pi*FS     #frecuencia en radianes
    suena = int(durationsec*MUESTREO)
    for i in range(0,suena):
        tono[i] = amplitud*(np.sin(w*t[i]))
    return tono

def silence(duracion):
    durationsec = DOTDURATIONSEC*duracion
    dt = 1/MUESTREO
    t = np.arange(0,durationsec,dt)
    tono = np.zeros(len(t), dtype='int16') #tono vacio
    return tono

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

