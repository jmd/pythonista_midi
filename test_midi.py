import midi
from time import sleep

mi = midi.MIDIInstrument()

def play(notes, bpm):
    duration = 60 / bpm
    for n in notes:
        if not n:
            sleep(duration)
            continue
        mi.playNote(n)
        sleep(duration)
        mi.stopNote(n)
    
godfather_theme = [
    'g4', 'c5', 'd5#', 'd5', 'c5', 'd5#', 'c5', 'd5', 'c5', 'g4#', 'a4#', 'g4', '',
    'g4', 'c5', 'd5#', 'd5', 'c5', 'd5#', 'c5', 'd5', 'c5', 'g4', 'f4#', 'f4',]

play(godfather_theme, 120)

