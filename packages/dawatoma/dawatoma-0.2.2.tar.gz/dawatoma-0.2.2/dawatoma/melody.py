from .note_dict import NoteDict
from midiutil import MIDIFile

class Melody:
    """
    A Melody is an object that implements the functionality of converting a .dawa string
    into a .midi file.

    .dawa strings have the following format containing all note sequence information:
    tempo_in_BPM # Commment
    note1 time duration
    note2 time duration
    ...
    noteN time duration
    Time and duration are in beats. The note is a string like C5 which will be interpreted with the NoteDict

    A Melody is generated in __attrs_post_init__ in the Sequence class as one of its
    member objects, where it receives the .dawa string "self.dstring" here.
    
    """
    def gen_midi(self) -> 'MIDIFile':
        "Generate the midiutil object that stores everything needed to write a midi file with the melody."
        notes = self.dstring[1:]
        self.midi = MIDIFile(1)
        self.midi.addTempo(self.track, 0, self.tempo)

        for i, note in enumerate(notes):
            pitch = NoteDict[note.split()[0]]
            time = float(note.split()[1])
            duration = float(note.split()[2])
            self.midi.addNote(self.track, self.channel, pitch, time, duration, self.volume)

    def __init__(self, dstring):
        "Setup the melody parameters"
        self.dstring = dstring.split('\n')
        self.track    = 0
        self.channel  = 0
        self.volume   = 100  # 0-127, as per the MIDI standard
        self.tempo = int(self.dstring[0].split()[0])   # In BPM
