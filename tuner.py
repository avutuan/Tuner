import numpy as np

# Trying to make a tuner in Python

A4 = 440
C4 = A4 * 2 ** (-9 / 12)
ALL_NOTES = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']

def nearest_note(examined_pitch):
    i = int(np.round(12 * np.log2(examined_pitch/A4)))
    close_note = ALL_NOTES[i % 12] + f'{4 + (i + 9) // 12}'
    close_pitch = A4 * 2 ** (i / 12)
    return close_note, close_pitch

def distance_from_nearest_note_in_cents(examined_pitch):
    close_tuple = nearest_note(examined_pitch)
    cents = 1200 * np.log2(examined_pitch/close_tuple[1])
    return np.round(cents)
    
close_tuple = nearest_note(300)
print(close_tuple)
print(distance_from_nearest_note_in_cents(300))