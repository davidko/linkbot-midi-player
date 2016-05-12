#!/usr/bin/env python3

import mido
import linkbot
import random
import sys

class Chorus():
    def __init__(self, linkbot_names):
        self._free_linkbots = set(map(linkbot.Linkbot, linkbot_names))
        self._singing_linkbots = {}

    def playNote(self, message):
        try:
            note = message.note
            l = self._free_linkbots.pop()
            l.setBuzzerFrequency(pow(2, (note-61)/12)*440)
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            l.setLedColor(r, g, b)
            self._singing_linkbots[str(message.channel)+" "+str(message.note)] = l
        except Exception as e:
            print(e)

    def stopNote(self, message):
        try:
            key = str(message.channel)+" "+str(message.note)
            l = self._singing_linkbots[key]
            l.setBuzzerFrequency(0)
            del self._singing_linkbots[key]
            self._free_linkbots.add(l)
        except Exception as e:
            print(e)

def main():
    if len(sys.argv) != 2:
        print('Usage: {} <filename.mid>'.format(sys.argv[0]))
        sys.exit(-1)

    chorus = Chorus(['6RW8', 'DGKR', 'ZRG6', 'D247'])
    f = mido.MidiFile(sys.argv[1])
    f.ticks_per_beat = f.ticks_per_beat*3
    #f = mido.MidiFile('bohemian1.mid')
    fswitch = { 'note_on' : chorus.playNote,
                'note_off': chorus.stopNote }
    for message in f.play():
        print(message.type)
        if message.type in ['note_on', 'note_off']:
            fswitch[message.type](message)

if __name__ == '__main__':
    main()
