import os, sys, attr
from .melody import Melody

@attr.s
class Sequence:
    """
    A Sequence is a container that holds all the relevant objects and metadata that
    allow one to work with note sequences.

    Attributes
    ----------
    
    dstring : str
        The .dawa string (the contents of a .dawa file or something that can
        be converted to that).

    name : str
        The corresponding name for a .midi or .dawa file that could be written
        from this sequence

    melody : Melody
        A Melody object containing all the information necessary to create a
        .midi file

    is_fprint : bool
        This is the base class and is not a fingerprint sequence
        (is_fprint = False)
    """
    dstring = attr.ib()
    name = attr.ib()
    melody = attr.ib(init=False)
    is_fprint = False

    def __attrs_post_init__(self):
        self.melody = Melody(self.dstring)

    def gen_midi(self):
        self.melody.gen_midi()

    def write_midi(self):
        with open(self.name+'.mid', "wb") as output_file:
            self.melody.midi.writeFile(output_file)

    def write_dawa(self):
        g = open(self.name+'.dawa','w')
        g.write(self.dstring)
        g.close()

    def __str__(self):
        return self.dstring

if __name__ == '__main__':
    "Make a sequence/melody from a dawa file and write it to .midi"
    seq1 = Sequence(open(sys.argv[1],'r').read(), sys.argv[1].split('.')[0])
    seq1.gen_midi()
    seq1.write_midi()
    print(seq1)
    print(seq1.is_fprint)
    #os.system('fluidsynth -i -a alsa ~/code/python/music/soundfonts/Ultima*/000_Florestan_Piano.sf2 '+sys.argv[1].split('.')[0]+'.mid')