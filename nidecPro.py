import time
from machine import Pin, PWM
from chrpy import chrpy

# Construct PWM object
power = PWM(Pin(19))
enable = Pin(17, Pin.OUT)
led = Pin(25, Pin.OUT)
converted_power = 0
percent_power = 50

# Set the PWM frequency.
power.freq(2500)
# power.freq(15625)

converted_power = 65535 * (50 / 100.0) # Set power to 50%

# print(converted_power)

power.duty_u16(int(converted_power))

def beep(hz, duration):
    print(f'beeping at {hz} for {duration}')
    power.freq(hz)
    time.sleep_ms(duration)

def play_chrp(file, track):
    chrp_song = chrpy.from_file(file, single_track = track)

    chrp_track = chrp_song.tracks[0]

    start_tick = time.ticks_ms()
    for note in chrp_track:
        off = True
        while time.ticks_diff(time.ticks_ms(), start_tick) < note.off:
            if off: enable.high()#; print(f'off, will be on in {time.ticks_diff(time.ticks_ms(), start_tick) - note.on}')
            if time.ticks_diff(time.ticks_ms(), start_tick) < note.on:
                #print('on')
                off = False
                enable.low()
                power.freq(note.note)

def play_chrp_directly(file, track):
    with open(file, 'rb') as f:
        data = f.read()
        total_notes = 0

        num_tracks = int.from_bytes(data[4:6], 'little')
        for i in range(num_tracks):
            addr = 6 + i * 2
            track_len = int.from_bytes(data[addr:addr+2], 'little')
            track_addr = total_notes * 12 + 6 + num_tracks * 2

            if i == track:
                start_tick = time.ticks_ms()
                for i in range(track_len):
                    note_addr = track_addr + i * 12

                    note = int.from_bytes(data[note_addr:note_addr+2], 'little')
                    # vel = int.from_bytes(data[i+2:i+4], 'little')
                    on = int.from_bytes(data[note_addr+4:note_addr+8], 'little')
                    off = int.from_bytes(data[note_addr+8:note_addr+12], 'little')

                    mute = True
                    while time.ticks_diff(time.ticks_ms(), start_tick) < off:
                        if mute: enable.high()#; print(f'off, will be on in {time.ticks_diff(time.ticks_ms(), start_tick) - note.on}')
                        if time.ticks_diff(time.ticks_ms(), start_tick) < on:
                            mute = False
                            enable.low()
                            power.freq(note)
                    
            total_notes += track_len



enable.low()
led.high()

try:
    play_chrp_directly('chrp_files/grabbag.chrp', 2)
except KeyboardInterrupt:
    print("Cancelled playback!")

print("song finished")

enable.high()
led.low()