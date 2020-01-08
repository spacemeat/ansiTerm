import sys
sys.path.append('../ansiTerm')

from ansiTerm import AnsiTerm
from ansiCommander import AnsiCommander as Ansi

t = AnsiTerm()

def grads():
    print ('░▒▓█', end = '')

def square(grad = 4):
    if grad == 0:
        print ('  ', end = '')
    elif grad == 1:
        print ('░░', end = '')
    elif grad == 2:
        print ('▒▒', end = '')
    elif grad == 3:
        print ('▓▓', end = '')
    elif grad == 4:
        print ('██', end = '')

print ("Default text looks like this.")

def printBgColor(color):
    st = Ansi.makeCommandFromStates(
        [ #('fg-color', 'system-dk-blue'),
          ('bg-color', 'system-{}'.format(color)) ] )
    print ('{}{}{}{}'.format(st, st[1:], '  ' * 20, Ansi.all_off))

def printFgColor(color):
    st = Ansi.makeCommandFromStates(
        [ #('fg-color', 'system-dk-blue'),
          ('fg-color', 'system-{}'.format(color)) ] )
    print ('{}{}{}{}'.format(st, st[1:], '██' * 20, Ansi.all_off))

def printColors(dklt, color, foreground, bold):
    if foreground:
        stateType = 'fg-color'
        fill = '██'
    else:
        stateType = 'bg-color'
        fill = '  '
    colorWord = 'system-{}-{}'.format(dklt, color)
    states = [ (stateType, colorWord) ]
    if bold:
        states.append( ('bold', 'on') )

    st = Ansi.makeCommandFromStates(states)
    print ('{}{}{} Color: {color}; Foreground: {fg}; Bold: {bold}{end}'.format(
        st, st[1:], fill * 5,
        color = colorWord,
        fg = foreground,
        bold = bold,
        end = Ansi.all_off))

colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

for bold in [False, True]:
    for foreground in [False, True]:
        for dklt in ['dk', 'lt']:
            for color in colors:
                printColors(dklt, color, foreground, bold)

print ('Grayscales:')

for i in range(0, 25):
    print (Ansi.makeCommandFromStates( [ ('fg-color', 'gs-{}'.format(i) ) ] ) , end = '')
    square()
print (Ansi.all_off)
print ("Grayscale backgrounds:")

for i in range(0, 25):
    print (Ansi.makeCommandFromStates( [ ('bg-color', 'gs-{}'.format(i) ) ] ) , end = '')
    square(0)
print (Ansi.all_off)

print ("Grayscale gradients using gradient blocks ( ░░ ▒▒ ▓▓ ██ ):")
for i in range(1, 25):
    print (Ansi.makeCommandFromStates(
        [ ('fg-color', 'gs-{}'.format(i) ),
          ('bg-color', 'gs-{}'.format(i - 1) ) ]
    ), end = '')

    for j in range (1, 5):
        square(j)

    if i % 6 == 0:
        print(Ansi.all_off)

print ("Color gradients:")
for b in range(0, 6):
    for g in range(0, 6):
        for r in range(0, 6):
            print (Ansi.makeCommandFromStates(
                [ ('fg-color', 'rgb-{}{}{}'.format(r, g, b) ) ]
            ) , end = '')
            square()
    print (Ansi.all_off)

for g in range(0, 6):
    for r in range(0, 6):
        for b in range(0, 6):
            print (Ansi.makeCommandFromStates(
                [ ('fg-color', 'rgb-{}{}{}'.format(r, g, b) ) ]
            ) , end = '')
            square()
    print (Ansi.all_off)

for r in range(0, 6):
    for b in range(0, 6):
        for g in range(0, 6):
            print (Ansi.makeCommandFromStates(
                [ ('fg-color', 'rgb-{}{}{}'.format(r, g, b) ) ]
            ) , end = '')
            square()
    print (Ansi.all_off)

print (Ansi.all_off)

t.setStyle('red-on-black', {
    'fg-color' : 'system-lt-red',
    'bg-color' : 'gs-0'
})

t.setStyle('blue-on-green', {
    'fg-color' : 'system-lt-blue',
    'bg-color' : 'system-dk-green'
})

t.setStyle('username', {
    'fg-color' : 'system-lt-yellow'
})

print ('{}{}{}{}{}{}{}{}{}{}{}'.format(
    t.pushState('red-on-black'),
    ' red on black ',
    t.pushState('blue-on-green'),
    ' blue on green ',
    t.pushState('username'),
    'username',
    t.popStates(),
    ' blue on green ',
    t.popStates(),
    ' red on black ',
    t.popStates()
))


t.setStyle('warning', {
    'fg-color' : 'system-lt-yellow',
    'bg-color' : 'rgb-000'
})

t.setStyle('warnLabel', {
    'bold' : 'on'
})

t.setStyle('pathdir', {
    'fg-color' : 'system-lt-blue'
})

t.setStyle('pathname', {
    'fg-color' : 'system-dk-blue'
})

print (Ansi.all_off)


import os

path = '/home/users/fink/.bashrc'

pr = '{warn}{warnLabel} Could not open {dir}{name}: Not found.{pop}'.format(
    warn = t.pushState('warning'),
    warnLabel = t.fmt('Warning:', 'warnLabel'),
    dir = t.fmt(os.path.dirname(path) + '/', 'pathdir'),
    name = t.fmt(os.path.basename(path), 'pathname'),
    pop = t.popStates()
)

print (pr)
print (Ansi.all_off)
