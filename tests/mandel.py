import sys
sys.path.append('../ansiTerm')

from ansiCommander import AnsiCommander as Ansi
import time

widthInChars = 80
heightInChars = 40

widthInPixels = widthInChars * 2
heightInPixels = heightInChars * 4

escapes = [[0 for col in range(0, widthInPixels)]
           for row in range(0, heightInPixels)]

def makeMandel(c0, c1):
    halfWidth = (c1.real - c0.real) / widthInPixels
    halfHeight = (c1.imag - c0.imag) / heightInPixels
    for row in range(0, heightInPixels):
        for col in range(0, widthInPixels):
            re =  c0.real + (col) * halfWidth
            imb = c0.imag + (row) * halfHeight
            for im in [imb, imb + 2 * halfHeight]:
                # run mandel on z = z + c
                c = complex(re, im)
                z = complex(0, 0)
                for iter in range(0, 6*6*6):
                    z = z * z + c
                    if abs(z) > 2.0:
                        break
                escapes[row][col] = 6*6*6 - iter - 1

def printEscapes(getColorFn):
    screen = ''
    seqs = []

    states = [
        ('fg-color', 'rgb-000'),
        ('bg-color', 'rgb-000')
    ]
    seqs.append('{}{}'.format(
        Ansi.makeCommandFromStates(states),
        ' ' * widthInPixels))

    for row in range(0, heightInPixels, 4):
        for col in range(0, widthInPixels, 2):
            topEsc0 = escapes[row + 0][col]
            botEsc0 = escapes[row + 1][col]
            topEsc1 = escapes[row + 0][col + 1]
            botEsc1 = escapes[row + 1][col + 1]
            topEsc2 = escapes[row + 2][col]
            botEsc2 = escapes[row + 3][col]
            topEsc3 = escapes[row + 2][col + 1]
            botEsc3 = escapes[row + 3][col + 1]

            states = [
                ('fg-color', avgColor(getColorFn, topEsc0, botEsc0, topEsc1, botEsc1)),
                ('bg-color', avgColor(getColorFn, topEsc2, botEsc2, topEsc3, botEsc3))
            ]
            seqs.append('{}{}'.format(
                Ansi.makeCommandFromStates(states),
                '▀'
            ))
        seqs.append('\n')

    states = [
        ('fg-color', 'rgb-000'),
        ('bg-color', 'rgb-000')
    ]
    seqs.append('{}{}'.format(
        Ansi.makeCommandFromStates(states),
        ' ' * widthInPixels))

    print(''.join(seqs))


def avgColor(colorizer, e0, e1, e2, e3):
    c0 = colorizer(e0)
    c1 = colorizer(e1)
    c2 = colorizer(e2)
    c3 = colorizer(e3)
    if len(c0) == 1:
        return 'gs-{}'.format(
            int((c0[0] + c1[0] + c2[0] + c3[0]) / 4))
    else:
        return 'rgb-{}{}{}'.format(
            int((c0[0] + c1[0] + c2[0] + c3[0]) / 4),
            int((c0[1] + c1[1] + c2[1] + c3[1]) / 4),
            int((c0[2] + c1[2] + c2[2] + c3[2]) / 4))


def getEscapeColor0(escape):
    return (
        escape % 6, int(escape / 6) % 6, int(escape / 36) % 6
    )

def getEscapeColor1(escape):
    return (
        int(escape / 6) % 6, int(escape / 36) % 6, escape % 6
    )

def getEscapeColor2(escape):
    return (
        int(escape / 36) % 6, escape % 6, int(escape / 6) % 6
    )

def getEscapeColor3(escape):
    return tuple([escape % 24])

center = complex(0, 1)
center = complex(-1.5, 0)
center = complex(-.5525, -.55)
#center = complex(-0.761574, -0.0847596)
#center = complex(-0.1528, -1.0397)
scale = 4.0
while (scale > 0.000001):
    makeMandel(complex(-scale / 2, -scale / 2) + center,
               complex( scale / 2,  scale / 2) + center)
    printEscapes(getEscapeColor2)
    scale *= .9
