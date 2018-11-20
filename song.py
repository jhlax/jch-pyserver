#!/usr/bin/env python3

"""
song.py: digital audio production utility
"""

import math
import click

KEYS = {
    'C': 0,
    'C#': 1,
    'D': 2,
    'D#': 3,
    'E': 4,
    'F': 5,
    'F#': 6,
    'G': 7,
    'G#': 8,
    'A': 9,
    'A#': 10,
    'B': 11,
}

KEYS_RMAP = {KEYS[v]: v for v in KEYS}


def parse_key(key_str: str):
    key_str = key_str.strip().upper()
    key = KEYS[key_str[0]]

    if len(key_str) > 1:
        if key_str[1] == '#':
            key += 1
            key %= 12
        else:
            key -= 1
            key %= 12

    return key


def repitch(steps: float = 3., rate: float = 128.) -> float:
    return rate / (2. ** (-steps / 12.))


def parse_scale(scale_str: str):
    scale_str = scale_str.strip().lower()
    scale = 'minor' if 'min' in scale_str else 'major'
    return scale


def print_times(rate: float, depth: int, srate: float):
    time_str = ''
    for i in range(depth):
        ms = btoms(rate, i)
        hz = 1. / (ms / 1000.)
        smps = int((ms / 1000.) * srate)
        print(f'\t1/{int(2. ** i)}:\t{round(ms, 2)} ms\t{round(hz, 2)} Hz\t'
              f'{smps} samples')

        time_str += f'\t1/{int(2. ** i)}:\t{round(ms, 2)} ms\t{round(hz, 2)} Hz\t' \
                    f'{smps} samples\n'
    print('-' * 69)
    return time_str


def print_repitches(rate: float, srate: float, depth: int, pbase: int):
    repitches_str = ''
    depth = (2 ** depth) // 2
    z = [-i for i in reversed(range(1, depth))] + [0] + [i for i in range(1, depth)]
    zpb = [(i + pbase) % 12 for i in z]
    zkey = [KEYS_RMAP[i] for i in zpb]
    zrp = [round(repitch(steps=i, rate=rate), 2) for i in z]

    zactual = [{'z': z[i], 'zpb': zpb[i], 'zkey': zkey[i], 'zrp': zrp[i]} for i in range(len(z))]
    for m in zactual:
        print(f'\t{m["z"]} steps:\t{m["zkey"]:3s}  {m["zrp"]}')
        repitches_str += f'\t{m["z"]} steps:\t{m["zkey"]:3s}  {m["zrp"]}\n'
    return repitches_str


def ktos(key: int, octave: int):
    key = KEYS_RMAP[key]
    return f'{key}{octave}'


def ktop(key: int, octave: int):
    return (octave * 12) + key


def ktof(key: int, octave: int):
    return 440. * (2. ** ((ktop(key, octave) - 69.) / 12.))


def ptok(pitch: float):
    key, octave = divmod(int(pitch), 12)


def ftop(freq: float):
    return 69. + (12. * math.log2(freq / 440.))


def btoms(rate: float, depth: int = 0):
    return (60000. / rate) * (1. / 2. ** depth)


@click.command()
@click.argument(
    'rate',
    type=float,
    default=128.0,
)
@click.argument(
    'key',
    type=str,
    default='C',
)
@click.option(
    '-S', '--scale',
    type=str,
    default='major',
)
@click.option(
    '-s', '--srate',
    type=float,
    default=44100.0,
)
@click.option(
    '-d', '--bpm-depth',
    type=int,
    default=8,
)
@click.option(
    '-D', '--repitch-depth',
    type=int,
    default=3,
)
def song(rate, key, scale, srate, bpm_depth, repitch_depth):
    print("-" * 69)
    print("song.py: digital audio production utility\n"
          "2018 (C) John C. Harrington.\n"
          "All rights reserved.")
    print("-" * 69)
    key = list(key)
    key[0] = key[0].upper()
    if len(key) > 1:
        key[1] = key[1].lower()
    key = ''.join(key)
    pbase = parse_key(key)
    scale = parse_scale(scale)

    print(f"""\
KEY:            {key}
SCALE:          {scale}
PITCH_BASE:     {pbase}
{'-' * 69}
SAMPLING_RATE:  {round(srate, 2)} Hz
TEMPO:          {round(rate, 2)} beats per minute
{'-' * 69}
BPM_DEPTH:      {bpm_depth} levels
REPITCH_DEPTH:  magnitude of {repitch_depth}
{'-' * 69}""")
    print("TIMES:")
    print_times(rate, bpm_depth, srate)
    print("PITCHES:")
    print_repitches(rate, srate, repitch_depth, pbase)


if __name__ == '__main__':
    song()
