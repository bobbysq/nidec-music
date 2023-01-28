import mido

def note_freq(n):
    return 440*2**((n-69)/12)

mid = mido.MidiFile('GrabbagOriginalVer_GM1.1.mid', clip=True)
# print(mid)

def get_tempo(mid):
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                # print(msg)
                return msg.tempo
    else:
        # Default tempo.
        return 500000

# for track in mid.tracks:
#     print(track)

# print(get_tempo(mid))

for track in mid.tracks:
    for msg in track:
        if msg.is_meta:
            print(msg)
        try:
            freq = round(note_freq(msg.note))
            ms = round(mido.tick2second(msg.time,mid.ticks_per_beat,get_tempo(mid))*1000)
            print("(" + str(freq) + "," + str(ms) + "),",end="")
        except:
            continue
    print("\n------\n")
        