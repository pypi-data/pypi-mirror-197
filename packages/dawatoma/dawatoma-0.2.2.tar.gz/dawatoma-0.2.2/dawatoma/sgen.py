"""
This module contains sequence generation routines.

Fingerprint sequences use these routines to generate other derived sequences.
This can be used by artists with writer's block to get ideas for agreeable
melodies to include in their track to make it more complex and layered.
"""
from .sequence import Sequence
from .note_dict import GenNoteDict
import random

running_msg = ("\nGenerating derived sequence from fingerprint sequence via "
               "'{}' function...\n")
complete_msg = ("\nCompleted running {} function. Returning derived sequence "
               "object\n")

def gen_d_string_from_notes(notes, freq=0.5, duration=16, period=0, is_cyclic=True):
    """Generate a .dawa string from a list of notes. If is_cyclic, cycle thru
    the list until the desired duration has been reached

    """
    time = 0.
    periods = 0.
    d_string = ''
    index = 0

    while (periods*period)+time+freq < duration:
        if index >= len(notes):
            if is_cyclic:
                index = 0
            else:
                return d_string

        d_string += '\n'+notes[index]+' '+str((periods*period)+time)+' '+str(freq)

        time += freq

        if time > period and period > 0:
            index = 0
            periods += 1.
            time -= period
        else:
            index += 1

    return d_string

def get_unique_notes(notes, show=False):
    "Get all unique notes in the .dawa sequence. Ignore the octave."
    un = []

    for note in notes:
        if note.split()[0][:-1] not in un:
            un.append(note.split()[0][:-1])

    if show:
        print(f"{len(un)} unique notes : {un}")

    return un

def two_unique_notes(notes):
    """See if a list of notes in .dawa format contains at least 2 unique
    notes. If yes, return True. If no, return False.

    """
    n1 = notes[0].split()[0][:-1]

    for note in notes[1:]:
        if note.split()[0][:-1] != n1:
            return True

    return False

def alt2(name, tempo, notes, freq: "beats", oc1, oc2, duration: "beats") -> Sequence:
    """Return a sequence of two notes alternating at the specified frequency
    in beats. Sample from the notes passed in to the function, and use the
    octaves specified.

    Parameters
    ----------
    name : str
        The corresponding name for a .midi or .dawa file that could be written
        from the generated sequence
    tempo : int
        Tempo in beats/minute
    notes : list
        Notes in .dawa format split by line excluding the header line
    freq : float
        Period between notes in beats
    oc1 : int
        Octave 1
    oc2 : int
        Octave 2
    duration : float
        Length of the desired sequence in beats

    """
    try:
        test = notes[1]
    except:
        raise ValueError("ERROR! There must be more than 1 note in a sequence to use alt2")
        return

    if not two_unique_notes(notes):
        raise ValueError("ERROR! There must be at least two unique notes to use alt2")
        return

    print(running_msg.format("alt2"))

    un = get_unique_notes(notes, True)

    d_string = str(tempo)
    note1 = un.pop(un.index(random.choice(un)))+str(oc1)
    note2 = un.pop(un.index(random.choice(un)))+str(oc2)
    time = 0.
    counter = 0

    # alt2 main algorithm
    while time+freq <= duration:
        if counter % 2 == 0:
            d_string += '\n'+note1+' '+str(time)+' '+str(freq)
        else:
            d_string += '\n'+note2+' '+str(time)+' '+str(freq)
        counter += 1
        time += freq

    print(complete_msg.format("alt2"))

    return Sequence(d_string, name)



def get_ad_note_order(note1, direction = 'asc'):
    """Return an ascending or descending order of notes that starts with
    note1, rather than 'C'

    """
    if direction == 'asc':
        octave = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    else:
        octave = ['B', 'A#', 'A', 'G#', 'G', 'F#', 'F', 'E', 'D#', 'D', 'C#', 'C']

    index = octave.index(note1)
    note_order = []
    for note in octave[octave.index(note1):]:
        note_order.append(note)
    for note in octave[:octave.index(note1)]:
        note_order.append(note)

    return note_order

def get_ad_notes(note, un_order, oc, direction = 'asc'):
    """Generate a list of ascending or descending (a/d) notes (i.e. A#4, B4,
    C5, ...) using only the unique notes in un_order, starting at note and
    going no further than B8 (for 'asc') and no further than C0 (for 'desc')

    """
    if direction == 'asc':
        octave = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    elif direction == 'desc':
        octave = ['B', 'A#', 'A', 'G#', 'G', 'F#', 'F', 'E', 'D#', 'D', 'C#', 'C']
    else:
        raise ValueError("ERROR! direction MUST be 'desc' or 'asc'")

    ad_notes = []
    index = 0; prev = -1
    while True:
        ad_notes.append(un_order[index]+str(oc))

        # Manage the current index in the unique ordered note list
        index += 1
        if index >= len(un_order):
            index = 0

        # Mange the octave number. If we pass or land on C, increase it
        if octave.index(un_order[index]) < octave.index(un_order[prev]) and prev != -1:
            if direction == 'asc':
                oc += 1
            if direction == 'desc':
                oc -= 1

        prev = index

        if direction == 'asc' and oc >= 9:
            break
        if direction == 'desc' and oc < 0:
            break

    return ad_notes

def gen_ad_d_string(ad_notes, freq, duration, period, da_prob):
    """Generate a .dawa string (missing the header line) of ascending or
    descending (a/d=ad) notes given the parameters. Parameters are explained
    in the 'asc' and 'desc' function documentation.

    """
    time = 0.
    periods = 0.
    d_string = ''
    index = 0

    while (periods*period)+time+freq < duration:
        d_string += '\n'+ad_notes[index]+' '+str((periods*period)+time)+' '+str(freq)

        time += freq

        if time > period and period > 0:
            index = 0
            periods += 1.
            time -= period
        else:
            if random.random() < da_prob and index > 0:
                index -= 1
            else:
                index += 1

    return d_string

def asc(name, tempo, notes, freq: "beats"=0.5, oc=4, duration: "beats"=16., period: "beats"=4., note1=None, dec_prob=0.) -> Sequence:
    """Return a series of ascending notes as a Sequence to the length of time
    specified (duration).

    Parameters
    ----------
    name : str
        The corresponding name for a .midi or .dawa file that could be written
        from the generated sequence
    tempo : int
        Tempo in beats/minute
    notes : list
        Notes in .dawa format split by line excluding the header line
    freq : float
        The length of each note in the Sequence.
    oc : int
        Octave of the starting note
    duration : float
        Length of the desired sequence in beats
    period : float
        Number of beats per ascending subsequence. Once this is reached, start
        at the bottom again.
    note1 : str
        First note to be used in the sequence. It will ascend from there
    dec_prob : float
        Probability (0 to 1) that the sequence will descend rather than ascend
        from one note to another

    Notes
    -----
        LINEARITY : An idea for a parameter (or two) that determine(s) the
        odds that a note is skipped in a sequence

    """
    print(running_msg.format("asc"))

    asc_notes = [] # All notes to be sampled
    un = get_unique_notes(notes)

    if note1 is None:
        note1 = random.choice(un)

    note_order = get_ad_note_order(note1, direction = 'asc')

    # Unique note order is a list of the unique notes in ascending order, starting with note1
    un_order = [n for n in note_order if n in un]

    # Arrange notes in ascending order starting with note1 at the selected octave
    note = note1
    asc_notes = get_ad_notes(note1, un_order, oc, direction = 'asc')
    d_string = str(tempo)+gen_ad_d_string(asc_notes, freq, duration, period, dec_prob)

    print(complete_msg.format("asc"))

    return Sequence(d_string, name)

def desc(name, tempo, notes, freq: "beats"=0.5, oc=4, duration: "beats"=16., period: "beats"=4., note1=None, asc_prob=0.) -> Sequence:
    """Return a series of descending notes as a Sequence to the length of time
    specified (duration).

    Parameters
    ----------
    name : str
        The corresponding name for a .midi or .dawa file that could be written
        from the generated sequence.
    tempo : int
        Tempo in beats/minute
    notes : list
        Notes in .dawa format split by line excluding the header line
    freq : float
        The length of each note in the Sequence.
    oc : int
        Octave of the starting note
    duration : float
        Length of the desired sequence in beats
    period : float
        Number of beats per descending subsequence. Once this is reached,
        start at the bottom again.
    note1 : str
        First note to be used in the sequence. It will descend from there
    dec_prob : float
        Probability (0 to 1) that the sequence will ascend rather than descend
        from one note to the other

    Notes
    -----
        LINEARITY : An idea for a parameter (or two) that determine(s) the
        odds that a note is skipped in a sequence
        
    """
    print(running_msg.format("desc"))

    desc_notes = [] # All notes to be sampled
    un = get_unique_notes(notes)

    if note1 is None:
        note1 = random.choice(un)

    note_order = get_ad_note_order(note1, direction = 'desc')

    # Unique note order is a list of the unique notes in descending order, starting with note1
    un_order = [n for n in note_order if n in un]

    # Arrange notes in ascending order starting with note1 at the selected octave
    note = note1
    desc_notes = get_ad_notes(note1, un_order, oc, direction = 'desc')
    d_string = str(tempo)+gen_ad_d_string(desc_notes, freq, duration, period, asc_prob)

    print(complete_msg.format("desc"))

    return Sequence(d_string, name)



def sample_random_notes(u_notes, oc1, oc2, maxdist, length):
    """Sample random notes from u_notes (unique notes) using in the range of
    octaves 1 and 2.

    Parameters
    ----------
    u_notes : list
        Unique notes without octaves
    oc1 : int
        Lower octave
    oc2 : int
        Upper octave
    maxdist : int
        Maximum distance between consecutive notes in the sequence.
    length : int
        Number of random notes to generate.

    Returns
    -------
    list
        This will return a list of notes (i.e. [C5, G6, D#5, ...])
        that can later be used. To create a .dawa string.

    """
    # notes = ['B', 'A#', 'A', 'G#', 'G', 'F#', 'F', 'E', 'D#', 'D', 'C#', 'C']

    note_dict = GenNoteDict()
    octaves = list(range(oc1,oc2+1))
    r_notes = [random.choice(u_notes)+str(random.choice(octaves))] # First element added

    while len(r_notes) < length:

        while True:
            note = random.choice(u_notes)
            oc = random.choice(octaves)
            new_note = note+str(oc)

            if abs(note_dict[new_note] - note_dict[r_notes[-1]]) < maxdist:
                break

        r_notes.append(new_note)

    return r_notes

def rsamp(name, tempo, notes, freq: "beats"=0.5, oc1=4, oc2=6, duration: "beats"=16., period: "beats"=0, maxdist=8, length=8):
    """Return a sequence of notes randomly sampled from the notes passed in in
    the octave range specified

    Parameters
    ----------
    name : str
        The corresponding name for a .midi or .dawa file that could be written
        from the generated sequence
    tempo : int
        Tempo in beats/minute
    notes : list
        Notes in .dawa format split by line excluding the header line
    freq : float
        The length of each note in the Sequence.
    oc1 : int
        Lower octave
    oc2 : int
        Upper octave
    duration : float
        Length of the desired sequence in beats
    period : float
        Number of beats per descending subsequence. Once this is reached,
        start at the bottom again.
    maxdist : int
        Maximum distance between consecutive notes in the sequence. You don't
        want the sequence jumping from like D3 to G7 or whatever
    length : int
        Number of random notes to generate. These will be written over and
        over until the duration is reached. Eeach note lasts for 'freq' amount
        of time in beats. The duration is also in beats.

    """
    if oc2 < oc1:
        raise ValueError("ERROR! Octave 2 (oc2) must be greater than or equal to Octave 1 (oc1)")
 
    print(running_msg.format("rsamp"))

    un = get_unique_notes(notes)

    r_notes = sample_random_notes(un, oc1=oc1, oc2=oc2, maxdist=maxdist, length=length)

    d_string = str(tempo)+gen_d_string_from_notes(r_notes, freq=freq, duration=duration, period=period)

    print(complete_msg.format("rsamp"))

    return Sequence(d_string, name)

