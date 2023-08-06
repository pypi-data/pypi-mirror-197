import sys, os
from .sgen import alt2, asc, desc, rsamp
from .sequence import Sequence

def seq_constructor_args_from_file(filename):
    """Create the two arguments for a sequence constructor (.dawa string,
    filename without extension) given only a .dawa filename"""

    with open(filename, 'r') as f:
        dstring = f.read()

    if dstring[-1] == '\n':
        return dstring[:-1], os.path.basename(os.path.splitext(filename)[0])
        #return dstring[:-1], filename.split('.')[0]
    else:
        return dstring, os.path.basename(os.path.splittext(filename)[0])


class FPSequence(Sequence):
    """
    A fingerprint sequence is a sequence from which other sequences may be
    derived using the various sequence derivation protocols available in this
    package.

    For example, a fingerprint might be your main melody from which
    you wish to derive additional melodies that could be overlayed at various
    points in the song. This is the child of the base class "Sequence", and
    has the additional functionality that allows for sequences to be derived
    from itself. 

    Attributes
    ----------
    is_fprint : is_frpint (bool)
        True. This allows a developer to probe whether a sequence is a fingerprint
        sequence or not. This variable is set to False for base class "Sequence".

    d_dict : d_dict (dict)
        A dictionary with keys corresponding to the different types of
        derivations that are possible, and values corresponding the current
        total number of derived sequences of that type.

    derseq : derseq (dict)
        Dictionary of derived sequences. Keys are names. Values are the
        Sequence objects.
        
    """

    # Using NumPy style docstrings
    #TO DO:
    #1.) Make it so you can combine all (or 16 at a time) derived sequences into a single midi, with each derived
    #sequence on its own channel.
    #2.) Add functionality to convert a derived sequence into a fingerprint sequence. That is, write a function
    #that makes a copy of a derived sequence, but returns that copy as a fingerprint sequence.

    is_fprint = True
    d_dict = {'rsamp':0, 'alt2':0, 'asc':0, 'desc':0}
    derseq = {}

    def gen_all_midi(self):
        """Generate midiutil objects for all derived sequences that store everything needed to write a midi
        file with the melody."""
        for name in self.derseq.keys():
            self.derseq[name].gen_midi()

    def write_all_midi(self):
        """Write a .midi file for all derived sequences. They will all be called '<name>.mid'"""
        for name in self.derseq.keys():
            self.derseq[name].write_midi()

    def write_all_dawa(self):
        """Write a .dawa file for all derived sequences. They will all be called '<name>.mid'"""
        for name in self.derseq.keys():
            self.derseq[name].write_dawa()

    def rsamp_s(self, freq=0.5, oc1=4, oc2=6, duration=32., period=0, maxdist=8, length=8):
        """Create a sequence of notes randomly sampled from the notes in this fingerprint sequence
        in the octave range specified"""
        name = 'rsamp_'+str(self.d_dict['rsamp'])
        notes = self.dstring.split('\n')[1:]
        self.derseq[name] = rsamp(name, self.melody.tempo, notes, freq=freq, oc1=oc1, oc2=oc2, duration=duration, period=period, maxdist=maxdist, length=length)
        self.d_dict['rsamp'] += 1

    def alt2_s(self, freq=1, oc1=5, oc2=5, duration=12):
        """Create a sequence of two notes alternating at the specified frequency in beats.
        Sample from the notes in this fingerprint sequence, and use the octaves specified."""
        name = 'alt2_'+str(self.d_dict['alt2'])
        notes = self.dstring.split('\n')[1:]
        self.derseq[name] = alt2(name, self.melody.tempo, notes, freq, oc1, oc2, duration)
        self.d_dict['alt2'] += 1

    def asc_s(self, freq=0.5, oc=4, duration=16., period=4., note1=None, dec_prob=0.):
        name = 'asc_'+str(self.d_dict['asc'])
        notes = self.dstring.split('\n')[1:]
        self.derseq[name] = asc(name, self.melody.tempo, notes, freq=freq, oc=oc, duration=duration, period=period, dec_prob=dec_prob)
        self.d_dict['asc'] += 1

    def desc_s(self, freq=0.5, oc=4, duration=16., period=4., note1=None, asc_prob=0.):
        name = 'desc_'+str(self.d_dict['desc'])
        notes = self.dstring.split('\n')[1:]
        self.derseq[name] = desc(name, self.melody.tempo, notes, freq=freq, oc=oc, duration=duration, period=period, asc_prob=asc_prob)
        self.d_dict['desc'] += 1

if __name__ == '__main__':
    "Make a fingerprint sequence/melody from a dawa file, write it to .midi, and derive additional melodies from it."
    fps_args = seq_constructor_args_from_file(sys.argv[1])
    seq1 = FPSequence(fps_args[0], fps_args[1])
    seq1.gen_midi()
    seq1.write_midi()
    print(seq1.is_fprint)
    seq1.alt2_s()
    #seq1.derseq['alt2_0'].gen_midi()
    #seq1.derseq['alt2_0'].write_midi()
    seq1.asc_s()
    seq1.desc_s()
    seq1.rsamp_s(length=12)
    seq1.gen_all_midi()
    seq1.write_all_midi()
    seq1.write_all_dawa()
    #os.system('fluidsynth -i -a alsa ~/code/python/music/soundfonts/Ultima*/000_Florestan_Piano.sf2 '+sys.argv[1].split('.')[0]+'.mid')
    # THERE ARE FOUR BEATS IN A NOTE
