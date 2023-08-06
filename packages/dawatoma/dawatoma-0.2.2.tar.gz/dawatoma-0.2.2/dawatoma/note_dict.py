def GenNoteDict():
    """
    Generate a dictionary that maps note strings (for example C5) to integer values of notes in
    midutil. For example, 60 is C5 so note_dict['C5'] = 60

    Notes
    -----
    # [60, 62, 64, 65, 67, 69, 71, 72] are the white notes between C5 and C6, inclusive
    # [61, 63, 66, 68, 70] are the black notes are the black notes (sharps) between C5 and C6
    
	"""
    note_dict = {}
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    for octave in range(9):
        for index, note in enumerate(notes):
            note_dict[note+str(octave)] = 12*octave + index

    return note_dict

NoteDict = GenNoteDict()

if __name__ == '__main__':
    print(GenNoteDict())
