import numpy as np
import scipy.io.wavfile as waves
import sys
import scipy.fftpack as fourier
import scipy.stats as stats
from enum import Enum

"""http://blog.espol.edu.ec/estg1003/morse-decodificador-de-sonido/"""

"""Duraciones en unidad universal, todo es en base a la duracion del DOT"""
DOTDURATION = 1
DASHDURATION = DOTDURATION * 3
SYMBOLSPACEDURATION = DOTDURATION
LETTERSPACEDURATION = DOTDURATION * 3
WORDSSPACEDURATION = DOTDURATION * 7
"Hz del tono"
FS = 440
"muestreo .wav:44100,22050,11025"
MUESTREO = 44100
DOTDURATIONSEC = 0.1


class Symbol(Enum):
    DOT = '.'
    DASH = '-'


INVERSE_MORSE_CODE_DICT = {
    '.-': 'A',
    '.--.-': 'Á',
    '-...': 'B',
    '-.-.': 'C',
    '-..': 'D',
    '.': 'E',
    '.,.-..': 'É',
    '..-.': 'F',
    '--.': 'G',
    '....': 'H',
    '..': 'I',
    '.---': 'J',
    '-.-': 'K',
    '.-..': 'L',
    '--': 'M',
    '-.': 'N',
    '--.--': 'Ñ',
    '---': 'O',
    '---.': 'Ó',
    '.--.': 'P',
    '--.-': 'Q',
    '.-.': 'R',
    '...': 'S',
    '-': 'T',
    '..-': 'U',
    '..-,-': 'Ú',
    '...-': 'V',
    '.--': 'W',
    '-..-': 'X',
    '-.--': 'Y',
    '--..': 'Z',
    '-----': '0',
    '.----': '1',
    '..---': '2',
    '...--': '3',
    '....-': '4',
    '.....': '5',
    '-....': '6',
    '--...': '7',
    '---..': '8',
    '----.': '9',
    '.--.-.': '@',
    '--..--': ',',
    '.-.-.-': '.',
    '---...': ':',
    '-.-.-.': ';',
    '..--..': '?',
    '.-..-.': '"',
    '.----.': "'",
    '-..-.': '/',
    '-....-': '-',
    '.-.-.': '+',
    '-...-': '=',
    '..--.-': '_',
    '-.--.': '(',
    '-.--.-': ')',
    '...-..-': '$',
    '.-...': '&'
}


def main(audiofile):
    muestreo, sonido = waves.read(audiofile)

    ventanas = separaventanas(sonido, muestreo)
    marcas = marcasdeventanas(ventanas, muestreo)
    secuencia = secuenciabinaria(marcas)
    conteo = duracionmarcas(secuencia)
    morse = marcasmorse(conteo)

    dump(morse)


def dump(morse):
    for palabra in morse:
        for letra in palabra:
            letrastr = ''
            for symbol in letra:
                letrastr = letrastr + (symbol.value)
            print(INVERSE_MORSE_CODE_DICT.get(letrastr, '?'), end="")
        print(' ', end="")
    print(' ')


def separaventanas(sonido, muestreo):
    # Divide el sonido en partes o ventanas para estudio
    partes = 8  # ventanas para cada punto
    # Extraer ventanas para espectro por partes
    tventana = 0.04 / partes
    mventana = int(muestreo * tventana)  # muestras de una ventana

    # Ajuste de muestras de ventanas para matriz
    anchosonido = int(len(sonido) / mventana) * mventana
    sonidoajuste = np.resize(sonido, anchosonido)
    ventanas = np.reshape(sonidoajuste, (-1, mventana))
    # -1 indica que calcule las filas
    return (ventanas)


def marcasdeventanas(ventanas, muestreo):
    # Analiza con FFT todas las ventanas del sonido
    filas, columnas = np.shape(ventanas)
    marcas = np.zeros(filas, dtype=int)

    # Espectro de Fourier de cada ventana
    # frecuencias para eje frq = fourier.fftfreq(mventana, 1/muestreo)
    frq = fourier.fftfreq(columnas, 1 / muestreo)
    for f in range(0, filas, 1):
        xf = fourier.fft(ventanas[f])
        xf = np.abs(xf)  # magnitud de xf
        tono = np.argmax(xf)  # tono, frecuencia mayor
        marcas[f] = frq[tono]
    return (marcas)


def secuenciabinaria(marcas):
    # Busca el tono frecuente mayor que cero
    tonos, counts = np.unique(marcas, return_counts=True)
    matriz = []
    for i in range (0,len(tonos)):
        matriz.append([tonos[i], counts[i]])
    tonosventana = np.ndarray(shape=(len(tonos), 2), dtype=int, buffer=np.array(matriz))
    donde = np.argmax(tonosventana[1:, 1])
    tonopunto = tonosventana[donde + 1, 0]

    # Convierte los tonos a secuencia binaria
    secuencia = ''
    for valor in marcas:
        if (valor == tonopunto):
            secuencia = secuencia + '1'
        else:
            secuencia = secuencia + '0'
    return (secuencia)


def duracionmarcas(secuencia):
    # Duración de cada marca
    conteo = []
    caracter = '1'
    if (len(secuencia) > 0):
        caracter = secuencia[0]
    i = 0
    k = 0
    while (i < len(secuencia)):
        if (secuencia[i] == caracter):
            k = k + 1
        else:
            conteo.append([int(caracter), k])
            if (caracter == '1'):
                caracter = '0'
            else:
                caracter = '1'
            k = 1
        i = i + 1
    conteo = np.array(conteo)
    return (conteo)


def marcasmorse(conteo):
    # Determina la base de un tono
    marcas, counts = np.unique(conteo[:, 1], return_counts=True)
    matriz = []
    for i in range (0,len(marcas)):
        matriz.append([marcas[i], counts[i]])
    veces = np.ndarray(shape=(len(marcas), 2), dtype=int, buffer=np.array(matriz))


    donde = np.argmax(veces[:, 1])
    base = veces[donde, 0]

    # Genera el código Morse
    tolera = 0.2  # Tolerancia en relacion
    bajo = 1 - tolera
    alto = 1 + tolera
    morse = []
    palabra = []
    letra = []
    for j in range(0, len(conteo)):
        relacion = conteo[j, 1] / base
        simbolo = conteo[j, 0]
        if (simbolo == 1):
            if (relacion > (1 * bajo) and relacion < (1 * alto)):
                letra.append(Symbol.DOT)
            if (relacion > (3 * bajo) and relacion < (3 * alto)):
                letra.append(Symbol.DASH)
        if simbolo == 0:
            if (relacion > (4 * bajo) and relacion < (4 * alto)):
                palabra.append(letra)
                letra = []
            if (relacion > (10 * bajo) and relacion < (10 * alto)):
                palabra.append(letra)
                morse.append(palabra)
                palabra = []
                letra = []
    palabra.append(letra)
    morse.append(palabra)
    return (morse)


if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        print("usage: " + sys.argv[0] + " <audiofile>")
        sys.exit(1)

    main(sys.argv[1])
